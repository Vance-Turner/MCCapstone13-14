# This serves as a cluster which can do processing for the simulations. Run this file on computers that should
# be doing simulations. It uses the bottle framework to serve requests as an HTTP server.

#Update the config.json for each machine and server you want to run!

from bottle import route, run, post, request
import xml.etree.ElementTree as ET
import subprocess
from processors import codesaturne
import json
from windmc.config import serverDataPath, JOB_TYPE_CODE_SATURNE, JOB_TYPE_CODE_SATURNE_ACT_DISK, windmcPath
from windmc.config import CODE_SAT_STD_ACT_DISK, CODE_SAT_STD_CASE
import shutil
import requests
from windmc.sim.clusters import clustermanager
from threading import Thread
import os, time

# Load info from config.json
import json
f = open(os.path.join(serverDataPath,'config.json'),'r')
config = json.load(f)
f.close()
machineIP = config['ip']
machinePort = config['port']
machineCores = config['cores']
machineSatVer = config['sat_ver']
machineID = config['id']


processorsMap = {"axialInductionFactor": codesaturne.getInletOutletVelocity}

# set up the study directory, creating it if necessary
import os

currentDir = os.getcwd()
studyDir = os.path.join(serverDataPath, "code_saturne", "studies")
if not os.path.exists(studyDir):
    os.makedirs(studyDir)

currentJobCount = 0


@route('/info')
def info():
    # create info page
    map = {'IP': machineIP, 'PORT': machinePort, 'ID': machineID, 'CORES': machineCores, 'SAT_VER': machineSatVer,
           'JOB_COUNT': currentJobCount,'STATUS':'READY'}
    return json.dumps(map)


@post('/job/<jobid>')
def startJob(jobid):
    jobMap = json.loads(request.forms.get('JOB_DATA'))
    type = jobMap['JOB_TYPE']
    print "Got order on a cluster, args>",jobMap

    if type == JOB_TYPE_CODE_SATURNE or type == JOB_TYPE_CODE_SATURNE_ACT_DISK:
        print "Cluster>calling runCodeSatJob"
        Thread(target=runCodeSatJob,args=(jobMap,)).start()
        return "1"


def copyCaseXMLTemplate(casePath,xmlName=CODE_SAT_STD_CASE):
    # copy the template xml to this case
    template = os.path.join(serverDataPath, 'code_saturne', 'templates', xmlName)
    if os.path.exists(template):
        subprocess.call(['cp', template, os.path.join(casePath, 'DATA')])
        # check to make sure it exists!
        if not os.path.exists(os.path.join(casePath, 'DATA', xmlName)):
            raise Exception("File not copied for xml, failing!>"+template+" "+casePath)


def getMeshFile(respIP,respPort,meshFileName,studyPath):
    # Thanks to: http://stackoverflow.com/questions/13137817/how-to-download-image-using-requests
    # for the following method
    req = requests.get('http://' + str(respIP) + ":" + str(respPort) + '/files/mesh/' + meshFileName)
    with open(os.path.join(studyPath, 'MESH', meshFileName),'wb') as code:
        code.write(req.content)
    # if req.status_code == 200:
    #     with open(os.path.join(studyPath, 'MESH', meshFileName), 'wb') as f:
    #         for chunk in req.iter_content():
    #             f.write(chunk)
    #print "Got mesh response:",str(req),"saving to:"
    #with open(os.path.join(studyPath, 'MESH', meshFileName), 'wb') as out_file:
    #    shutil.copyfileobj(req.raw, out_file)
    #del req


def runCodeSatJob(jobMap):
    """
    Runs a code_saturne simulation. Blocks until code_saturne completes.
    """
    respIP = jobMap["respIP"]
    respPort = jobMap["respPort"]
    processorModule = jobMap["processorModule"]
    study = jobMap["STUDY"]
    case = jobMap["CASE"]

    studyPath = os.path.join(studyDir, study)
    casePath = os.path.join(studyPath, case)
    # first test if we have this study
    if not os.path.exists(studyPath):
        # Make the study
        print "Creating the study:",studyPath
        subprocess.call(['code_saturne', 'create', '-s', studyPath, '-c', case])
    elif not os.path.exists(os.path.join(studyPath, case)):
        # Create the case
        print "Creating the case:",casePath
        subprocess.call(['code_saturne', 'create', '-c', os.path.join(casePath)])
        print "Created the case, now testing job tpe."
    else:
        print "The study already exists:",studyPath
    # Now we should have the study and case and can proceed
    # Get the xml file currently in the case directory
    if jobMap['JOB_TYPE']==JOB_TYPE_CODE_SATURNE:
        # copy the template xml to this case
        print "Copying the xml file for a standard code-sat sim."
        copyCaseXMLTemplate(casePath)
        xmlFilePath = os.path.join(casePath, "DATA", CODE_SAT_STD_CASE)
    elif jobMap['JOB_TYPE']==JOB_TYPE_CODE_SATURNE_ACT_DISK:
        # copy the template xml to this case
        print "Copying the xml file for an actuator disk code-sat sim."
        copyCaseXMLTemplate(casePath,CODE_SAT_STD_ACT_DISK)
        xmlFilePath = os.path.join(casePath, "DATA", CODE_SAT_STD_ACT_DISK)
    else:
        print "The JOB_TYPE provided is invalid!>",jobMap['JOB_TYPE']
    print "Ok, created the code-saturne study, now doing xml file..."

    tree = ET.parse(xmlFilePath)
    root = tree.getroot()
    # Put in the head loss coefficients
    # Head loss coefficients
    headLossX = jobMap['HLXX']
    headLossY = jobMap['HLYY']
    headLossZ = jobMap['HLZZ']
    print "HeadLossXX>",root.findall("./thermophysical_models/heads_losses/head_loss[@zone='2']/kxx")
    xx = root.findall("./thermophysical_models/heads_losses/head_loss[@zone_id='2']/kxx")[0]
    yy = root.findall("./thermophysical_models/heads_losses/head_loss[@zone_id='2']/kyy")[0]
    zz = root.findall("./thermophysical_models/heads_losses/head_loss[@zone_id='2']/kzz")[0]
    xx.text = str(headLossX)
    yy.text = str(headLossY)
    zz.text = str(headLossZ)

    if jobMap['JOB_TYPE']==JOB_TYPE_CODE_SATURNE:
        # Now set the probe locations
        # Set the location for probe 5, the shroud inlet probe
        root.findall("./analysis_control/output/probe[@name='50']/probe_x")[0].text = str(jobMap["SHROUD_IN_X"])
        root.findall("./analysis_control/output/probe[@name='50']/probe_y")[0].text = str(jobMap["SHROUD_IN_Y"])
        root.findall("./analysis_control/output/probe[@name='50']/probe_z")[0].text = str(jobMap["SHROUD_IN_Z"])
        # Set the location for probe 6, the shroud outlet probe
        root.findall("./analysis_control/output/probe[@name='51']/probe_x")[0].text = str(jobMap["SHROUD_OUT_X"])
        root.findall("./analysis_control/output/probe[@name='51']/probe_y")[0].text = str(jobMap["SHROUD_OUT_Y"])
        root.findall("./analysis_control/output/probe[@name='51']/probe_z")[0].text = str(jobMap["SHROUD_OUT_Z"])

    # Set the mesh file name
    root.findall(".solution_domain/meshes_list/mesh")[0].attrib['name']=jobMap['MESH_CODE']
    print "Set xml files, now getting or building mesh."
    # Now we need to build the mesh file.
    if jobMap['MESH_CREATE']=="DOWNLOAD":
        # Only download we don't have it already.
        if not os.path.exists(os.path.join(studyPath,'MESH',jobMap['MESH_CODE'])):
            # Download the mesh file
            print "Downloading the mesh file...:",jobMap['MESH_CODE']
            getMeshFile(jobMap['respIP'],jobMap['respPort'],jobMap['MESH_CODE'],studyPath)
        else:
            print "The mesh",jobMap['MESH_CODE'],"is already downloaded."
    elif jobMap['MESH_CREATE']=='BUILD':
        # Build the mesh file...
        buildMeshFile(jobMap['MESH_CODE'])
    # Do some more processing here...
    # write out the file, we are done, time to process!
    print "Got or built mesh, now writing xml file out."
    tree.write(xmlFilePath)

    print "Running code-saturne"
    # Now starting up code_saturne
    time0 = time.time()
    subprocess.call(["code_saturne", "run", "--param", xmlFilePath])
    print "Code-saturne finished!"
    print "Now doing post-processing"
    result = doCodeSatResultsProcessing(jobMap['processorModule'],casePath)
    print "Total calculation time:",str(time.time()-time0)
    print "Now posting results:",result,"to",("http://"+str(respIP)+":"+str(respPort)+"/results/"+str(jobMap['jobID']))
    requests.post("http://"+str(respIP)+":"+str(respPort)+"/results/"+str(jobMap['jobID']),data={'RESULTS_DATA':result})

def buildMeshFile(code):
    pass

def doCodeSatResultsProcessing(processorFunction, casePath):
    """
    Does processing of results after a code_saturne simulation
    processorModule -- The function that needs to be run in codesaturne.py
    study -- The name of the study that results are to be processed from
    case -- The name of the case in the study from which results are to be processed
    """
    result = processorsMap[processorFunction](os.path.join(casePath, "RESU"))
    print "Got results from post processing>", str(result)
    return result


run(host=machineIP, port=machinePort)