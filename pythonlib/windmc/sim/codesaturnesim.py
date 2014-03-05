'''
Created on Mar 4, 2014

@author: vance
@summary: This runs a code saturne simulation, just call doSimulation 
'''

from exceptions import Exception
from threading import Thread
import os
import time
import json
import subprocess
import xml.etree.ElementTree as ET
from processors.codesaturne import getInletOutletVelocity
from bottle import route, run, static_file, get
from windmc.sim.processors import salomescriptbuilder
import uuid

"""
Holds results of code-saturne jobs. The key is the job id and the value is the energy extracted.
"""
jobTypeMap = {}
jobCasePathMap = {}
coeffMap = {}
resultsMap = {}
velResMap = {}

jsonFile = open('config.json')
configMap = json.load(jsonFile)
jsonFile.close()

SERVER_PORT = configMap['serverPort']
SERVER_DATA_PATH = configMap['serverDataPath']
WINDMC_PATH = configMap['windmcPath']

CODE_SATURNE_DATA_PATH = os.path.join(configMap['serverDataPath'],'code_saturne')
CODE_SATURNE_STUDY_PATH = os.path.join(CODE_SATURNE_DATA_PATH,'STUDIES')
CODE_SATURNE_TEMPLATE_PATH = os.path.join(CODE_SATURNE_DATA_PATH,'TEMPLATES')

CODE_SAT_ACT_XML_NAME = 'code_saturne_case.xml'#'actuator_disk_case.xml'
CODE_SAT_STD_XML_NAME = 'case.xml'
"""
The path to the template file for a code-saturne axial induction finder case.
"""
CODE_SAT_ACT_DISK_PATH = os.path.join(CODE_SATURNE_TEMPLATE_PATH,CODE_SAT_ACT_XML_NAME)

"""
The path to the template file for a standard code-saturne simulation.
"""
CODE_SAT_STD_PATH = os.path.join(CODE_SATURNE_TEMPLATE_PATH,CODE_SAT_STD_XML_NAME)

CODE_SAT_MESH_TEMPLATES = os.path.join(CODE_SATURNE_DATA_PATH,'MESHES')

meshTypes_COPY = 'COPY_MESH'
meshTypes_BUILD = 'BUILD_MESH'

MESH_GENERATED = False

codeSatStd = "STANDARD_CODE_SAT_JOB"
codeSatActDisk = "ACT_DISK_CODE_SAT_JOB"

salomeInstallLocation = configMap["salomeInstallLoc"]

'''
This is used by the bisection to tell when a job has completed...
'''
bisectionTaskDone = True

# Physical constants
AIR_DENSITY = configMap['airDensity']

INLET_VEL = configMap['inletVel']

TUNNEL_RADIUS = configMap['tunnelRadius']

from windmc.modelling.tunnelscript import ACTUATOR_TUNNEL_GEN

class MeshGenerationTask(Thread):
    def __init__(self, generationType, generationID, generationDirectory,**genParams):
        Thread.__init__(self)
        self.genType = generationType
        self.genParams = genParams
        self.genID = generationID
        self.genDir = generationDirectory

    def run(self):
        if self.genType == ACTUATOR_TUNNEL_GEN:
            commandList = []
            commandList.append(os.path.join(salomeInstallLocation, 'runAppli'))
            commandList.append('-t')
            commandList.append(os.path.join(self.genDir, 'tunnelscript.py'))
            # Copy the mesh generation script into the study MESH directory
            copyFile(os.path.join(WINDMC_PATH,'modelling','tunnelscript.py'),\
                      os.path.join(self.genDir,'tunnelscript.py'))
            # Copy the json file into the MESh directory
            copyFile(os.path.join(WINDMC_PATH,'modelling','actuator.json'),\
                     os.path.join(self.genDir,'actuator.json'))
            '''
            commandList.append(ACTUATOR_TUNNEL_GEN)
            commandList.append(self.genPath)
            for key in self.genParams.keys():
                commandList.append(str(key)+':'+self.genParams[key]
            '''
            actuatorPath = os.path.join(self.genDir,'actuator.json')
            actFile = open(actuatorPath,'r')
            actMap = json.load(actFile)
            actFile.close()
            for key in self.genParams.keys():
                actMap[str(key)] = self.genParams[key]
            actFile = open(actuatorPath,'w')
            json.dump(actMap,actFile)
            actFile.close()
            print "MeshGenerationTask, calling generation command>",commandList
            output = open(os.path.join(self.genDir,'meshing.info'),'w')
            
            # Now create the bash file that will run the code-saturne script and the python module for meshing
            meshSh = os.path.join(self.genDir,'doMeshing.sh')
            bash = open(meshSh,'w')
            bash.write('#!/bin/sh \n')
            bash.write(os.path.join(salomeInstallLocation, 'runAppli')+' -t '+os.path.join(self.genDir, 'tunnelscript.py')+'\n')
            #bash.write('python ' + os.path.join(CODE_SATURNE_TEMPLATE_PATH,'codeSatComplete.py')+ ' ' + str(SERVER_PORT)+' ' + studyName +' '+caseName)
            bash.write('wget http://atlacamani.marietta.edu:'+str(SERVER_PORT)+'/'+'jobcompleted/meshfinished')
            bash.close()
            global MESH_GENERATED
            MESH_GENERATED = False
            subprocess.call(['chmod','a+x',meshSh])
            #subprocess.call(['sbatch',meshSh])
            subprocess.call([os.path.join(self.genDir,'doMeshing.sh')],stdout=output)    
            #subprocess.call(commandList,stdout=output)
            output.close()
            print "MeshGenerationTask, mesh gen command finished!"
           
def copyFile(src,dest):
    if os.path.exists(src):
        subprocess.call(['cp', src, dest])
        # check to make sure it exists!
        if not os.path.exists(dest):
            raise Exception("File not copied for xml, failing!>"+src+" "+dest)
    else:
        raise Exception("Src or Destination does not exist!"+src+" "+dest)
    
def codeSaturneSim(name,shroudRawPoints,headLoss=0.25,meshType=meshTypes_BUILD,meshCode='',codeSatType=codeSatActDisk):
    global SERVER_PORT
    """
    Runs a code-saturne simulation. Note this function does not work yet for standard code-saturne simulations!
    It only works for actuator disk simulations.
    """
    studyName = name+"_STUDY"
    caseName = name+"_CASE"
    studyPath = os.path.join(CODE_SATURNE_STUDY_PATH,studyName)
    casePath = os.path.join(studyPath,caseName)
    # Create the study and case directory
    # first test if we have this study
    if not os.path.exists(studyPath):
        # Make the study
        print "Creating the study:",studyPath
        subprocess.call(['code_saturne', 'create', '-s', studyPath, '-c', caseName])
        print "Creating the case:",casePath
        subprocess.call(['code_saturne', 'create', '-c', os.path.join(casePath)])
    else:
        print "The study already exists:",studyPath
        return -1

    # Now do xml stuff
    # Get the xml file currently in the case directory
    if codeSatType==codeSatStd:
        # copy the template xml to this case
        print "Copying the xml file for a standard code-sat sim."
        copyFile(CODE_SAT_STD_PATH,os.path.join(casePath,'DATA',CODE_SAT_STD_XML_NAME))
        xmlFilePath = os.path.join(casePath, "DATA", CODE_SAT_STD_XML_NAME)
    elif codeSatType==codeSatActDisk:
        # copy the template xml to this case
        print "Copying the xml file for an actuator disk code-sat sim."
        copyFile(CODE_SAT_ACT_DISK_PATH,os.path.join(casePath,'DATA',CODE_SAT_ACT_XML_NAME))
        xmlFilePath = os.path.join(casePath, "DATA", CODE_SAT_ACT_XML_NAME)
    else:
        print "Invalid code-saturen job type!>",codeSatType
        return -1
    print "Ok, created the code-saturne study, now doing xml file...:",xmlFilePath
    tree = ET.parse(xmlFilePath)
    root = tree.getroot()
    # Put in the head loss coefficients
    # Head loss coefficients
    headLossX = headLoss
    headLossY = '0'
    headLossZ = '0'
    print "HeadLossXX>",root.findall("./thermophysical_models/heads_losses/head_loss[@zone='2']/kxx")
    xx = root.findall("./thermophysical_models/heads_losses/head_loss[@zone_id='2']/kxx")[0]
    yy = root.findall("./thermophysical_models/heads_losses/head_loss[@zone_id='2']/kyy")[0]
    zz = root.findall("./thermophysical_models/heads_losses/head_loss[@zone_id='2']/kzz")[0]
    xx.text = str(headLossX)
    yy.text = str(headLossY)
    zz.text = str(headLossZ)

    # TODO: This code only runs for a standard code-saturne simuatlion; and is incorrect currently.
    '''
    if codeSatType==codeSatStd:
        # Now set the probe locations
        # Set the location for probe 5, the shroud inlet probe
        root.findall("./analysis_control/output/probe[@name='50']/probe_x")[0].text = str(jobMap["SHROUD_IN_X"])
        root.findall("./analysis_control/output/probe[@name='50']/probe_y")[0].text = str(jobMap["SHROUD_IN_Y"])
        root.findall("./analysis_control/output/probe[@name='50']/probe_z")[0].text = str(jobMap["SHROUD_IN_Z"])
        # Set the location for probe 6, the shroud outlet probe
        root.findall("./analysis_control/output/probe[@name='51']/probe_x")[0].text = str(jobMap["SHROUD_OUT_X"])
        root.findall("./analysis_control/output/probe[@name='51']/probe_y")[0].text = str(jobMap["SHROUD_OUT_Y"])
        root.findall("./analysis_control/output/probe[@name='51']/probe_z")[0].text = str(jobMap["SHROUD_OUT_Z"])
    '''

    # Set the density of the fluid in the xml file
    density = root.findall("./physical_properties/fluid_properties/property[@label='Density']/initial_value")[0]
    density.text = str(AIR_DENSITY)

    # Set the inlet velocity
    inn = root.findall("./boundary_conditions/inlet[@label='inlet']/velocity_pressure/norm")[0]
    inn.text = INLET_VEL

    print "Set xml files, now getting or building mesh."
    meshGenDir = os.path.join(studyPath,'MESH')
    meshFileName = name+'_MESH.med'
    meshFilePath = os.path.join(meshGenDir,meshFileName)
    if meshType==meshTypes_COPY:
        copyFile(os.path.join(CODE_SAT_MESH_TEMPLATES,meshCode),os.path.join(studyPath,'MESH',meshCode))
    elif meshType==meshTypes_BUILD:
        print "Generating mesh..."
        meshGenTask = MeshGenerationTask(ACTUATOR_TUNNEL_GEN, name, meshGenDir,\
                                         shroudPoints=shroudRawPoints,outputPath=meshFilePath)
        meshGenTask.run()
        global MESH_GENERATED
        print "Waiting for mesh to generate..."
        while not MESH_GENERATED:
            time.sleep(5)
        print "Mesh generated apparently!"
    # Set the mesh file name
    root.findall(".solution_domain/meshes_list/mesh")[0].attrib['name']=meshFileName
    
    # write out the file, we are done, time to process!
    print "Got or built mesh, now writing xml file out.:",xmlFilePath
    tree.write(xmlFilePath)

    coeffMap[studyName+'-'+caseName]=headLoss

    jobTypeMap[studyName+'-'+caseName] = codeSatType
    jobCasePathMap[studyName+'-'+caseName] = casePath
    # Now create the bash file that will run the code-saturne script and the python module for announcing completion
    bash = open(os.path.join(casePath,'DATA','doSaturne.sh'),'w')
    bash.write('#!/bin/sh \n')
    bash.write('code_saturne run --param '+xmlFilePath+'\n')
    #bash.write('python ' + os.path.join(CODE_SATURNE_TEMPLATE_PATH,'codeSatComplete.py')+ ' ' + str(SERVER_PORT)+' ' + studyName +' '+caseName)
    bash.write('wget http://atlacamani.marietta.edu:'+str(SERVER_PORT)+'/'+'jobcompleted/'+studyName+'/'+caseName)
    bash.close()
    subprocess.call(['chmod','a+x',os.path.join(casePath,'DATA','doSaturne.sh')])
    subprocess.call(['sbatch',os.path.join(casePath,'DATA','doSaturne.sh')])
    return casePath

@get('/jobcompleted/<study>/<case>')
def jobCompleted(study,case):
    # Now do the post-processing
    print "Job Completed...calling post-processing."
    # Get the results directory
    global jobCasePathMap
    global SERVER_PORT
    casePath = jobCasePathMap[study+'-'+case]
    resultsDir = os.path.join(casePath,'RESU')
    resultsDir = os.listdir(resultsDir)[0]
    resultsDir = os.path.join(casePath,'RESU',resultsDir,'postprocessing')
    salomescriptbuilder.main(WINDMC_PATH, resultsDir, case, SERVER_PORT)
    
@get('/jobcompleted/meshfinished')
def meshCompleted():
    global MESH_GENERATED
    MESH_GENERATED=True
    return 'GOOD'

@get('/jobcompleted/postprocessing')
def postProcessingFinished():
    import sys
    sys.stderr.close()
    return 'GOOD'

def doSimulation(shroudPoints):
    from threading import Thread
    import uuid
    id = uuid.uuid1()
    casePath = None
    class Starter(Thread):
        
        def __init__(self):
            Thread.__init__(self)
            
        def run(self):   
            global SERVER_PORT
            casePath = codeSaturneSim(str(id), shroudPoints, 0.25, meshTypes_BUILD)
            
    Starter().start()
    startedServer = False
    global SERVER_PORT
    while not startedServer:
        print "\n---Trying to start on>",SERVER_PORT
        try:
            run(host='atlacamani.marietta.edu', port=SERVER_PORT,quiet=True)
        except Exception:
            print "Failed to start on:",SERVER_PORT
        SERVER_PORT = int(SERVER_PORT)
        SERVER_PORT += 1
        SERVER_PORT = str(SERVER_PORT)
    if casePath == None:
        print "Didn't get a valid case path after simulation!"
        return 0
    else:
        try:
            resultsDir = os.path.join(casePath,'RESU')
            resultsDir = os.listdir(resultsDir)[0]
            resultsDir = os.path.join(casePath,'RESU',resultsDir,'postprocessing','powerCoefficient.txt')
            powerCoeffFile = open(resultsDir,'r')
            powerCoeff = float(powerCoeffFile.readline())
            print "Returning powerCoeff>",powerCoeff
            powerCoeffFile.close()
            if powerCoeff > 0.98:
                return 0
            else:
                return powerCoeff
        except:
            print "Failed to get a power coefficient..."
            return 0       
            
#print doSimulation([[60,35],[70,20],[78,28],[82,28],[90,35],[110,30]])