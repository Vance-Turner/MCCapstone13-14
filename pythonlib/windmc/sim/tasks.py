__author__ = 'vance'

from threading import Thread
import os
from bottle import route
import time
import json
import subprocess
import xml.etree.ElementTree as ET

"""
Holds results of code-saturne jobs. The key is the job id and the value is the energy extracted.
"""
jobResults = {}
energyResults = {}
jobMap = {}

configMap = json.load('config.json')

CODE_SATURNE_DATA_PATH = os.path.join(configMap['serverDataPath'],'code_saturne')
CODE_SATURNE_STUDY_PATH = os.path.join(CODE_SATURNE_DATA_PATH,'STUDIES')
CODE_SATURNE_TEMPLATE_PATH = os.path.join(CODE_SATURNE_DATA_PATH,'TEMPLATES')

CODE_SAT_ACT_XML_NAME = 'actuator_disk_case.xml'
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

codeSatStd = "STANDARD_CODE_SAT_JOB"
codeSatActDisk = "ACT_DISK_CODE_SAT_JOB"

def copyFile(src,dest):
    if os.path.exists(src) and os.path.exists(dest):
        subprocess.call(['cp', src, dest])
        # check to make sure it exists!
        if not os.path.exists(dest):
            raise Exception("File not copied for xml, failing!>"+src+" "+dest)
    else:
        raise Exception("Src or Destingion does not exist!")

def postProcessCodSatActDisk(resultsPath):
    pass


def codeSaturneSim(name,headLoss,meshType=meshTypes_COPY,meshCode='',codeSatType=codeSatActDisk):
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
        xmlFilePath = os.path.join(casePath, "DATA", CODE_SAT_STD_PATH)
    elif codeSatType==codeSatActDisk:
        # copy the template xml to this case
        print "Copying the xml file for an actuator disk code-sat sim."
        copyFile(CODE_SAT_ACT_DISK_PATH,os.path.join(casePath,'DATA',CODE_SAT_ACT_XML_NAME))
        xmlFilePath = os.path.join(casePath, "DATA", CODE_SAT_ACT_DISK_PATH)
    else:
        print "Invalid code-saturen job type!>",codeSatType
        return -1
    print "Ok, created the code-saturne study, now doing xml file..."

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
    # Set the mesh file name
    # TODO: This needs to be updated to set the mesh file name when building a mesh.
    root.findall(".solution_domain/meshes_list/mesh")[0].attrib['name']=meshCode

    print "Set xml files, now getting or building mesh."
    # TODO: Need to write for code that calls whatever module will actually build the mesh, for now we just copy it from the standard location...
    if meshType==meshTypes_COPY:
        copyFile(os.path.join(CODE_SAT_MESH_TEMPLATES,meshCode),os.path.join(studyPath,'MESH',meshCode))
    elif meshType==meshTypes_BUILD:
        raise Exception("Cannot build a mesh yet!!")
        return -1
    # write out the file, we are done, time to process!
    print "Got or built mesh, now writing xml file out."
    tree.write(xmlFilePath)

    # TODO: Now we run the service, using SLURM, well actually we can't for now at least...
    subprocess.call(["code_saturne", "run", "--param", xmlFilePath])
    # Now do the post-processing
    if codeSatType==codeSatActDisk:
        postProcessCodSatActDisk(os.path.join(casePath,'RESU'))

@route('/currentResults')
def getCurrentResults():
    return "We don't have results getting implemented yet..."

class AxialInductionTask(Thread):

    def __init__(self,lowerHeadLoss,upperHeadLoss,taskId):
        Thread.__init__(self)
        self._lowerHeadLoss = lowerHeadLoss
        self._upperHeadLoss = upperHeadLoss
        self._taskId = taskId

    def run(self):
        self.doSim(self._lowerHeadLoss)

    def doSim(self,headLoss):




class MainControllerTask(Thread):

    def run(self):
        for i in xrange(0,40):
            task = AxialInductionTask(float(i)/10.0,1,'task_'+str(float(i)/10.0))
            task.start()


if __name__ == '__main__':
    MainControllerTask().start()
    run(host='atlacamani.marietta.edu', port=1990, debug=True)