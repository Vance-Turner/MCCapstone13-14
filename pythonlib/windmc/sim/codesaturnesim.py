'''
Created on Mar 4, 2014

@author: vance
@summary: This runs a code saturne simulation, just call doSimulation 
'''

from exceptions import Exception
from threading import Thread, Event
import os
import time
import json
import subprocess
import xml.etree.ElementTree as ET
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from windmc.sim.processors import salomescriptbuilder
import uuid

meshTypes_COPY = 'COPY_MESH'
meshTypes_BUILD = 'BUILD_MESH'

codeSatStd = "STANDARD_CODE_SAT_JOB"
codeSatActDisk = "ACT_DISK_CODE_SAT_JOB"

WIND_MC_PATH = None

class CodeSaturneSim():
    
    def __init__(self,meshingMethod, shroudPoints,dataMap):
        """
        Holds results of code-saturne jobs. The key is the job id and the value is the energy extracted.
        """
        self.meshingMethod = meshingMethod
        self.shroudPoints = shroudPoints
        self.dataMap = dataMap
        
        self.jobTypeMap = {}
        self.jobCasePathMap = {}
        self.coeffMap = {}
        self.resultsMap = {}
        self.velResMap = {}
        
        self.jsonFile = open('config.json')
        self.configMap = json.load(self.jsonFile)
        self.jsonFile.close()
        
        self.SERVER_PORT = self.configMap['serverPort']
        self.SERVER_DATA_PATH = self.configMap['serverDataPath']
        self.WINDMC_PATH = self.configMap['windmcPath']
        global WIND_MC_PATH
        WIND_MC_PATH =self.WINDMC_PATH
        
        self.CODE_SATURNE_DATA_PATH = os.path.join(self.configMap['serverDataPath'],'code_saturne')
        self.CODE_SATURNE_STUDY_PATH = os.path.join(self.CODE_SATURNE_DATA_PATH,'STUDIES')
        self.CODE_SATURNE_TEMPLATE_PATH = os.path.join(self.CODE_SATURNE_DATA_PATH,'TEMPLATES')
        
        self.CODE_SAT_ACT_XML_NAME = 'code_saturne_case.xml'#'actuator_disk_case.xml'
        self.CODE_SAT_STD_XML_NAME = 'case.xml'
        """
        The path to the template file for a code-saturne axial induction finder case.
        """
        self.CODE_SAT_ACT_DISK_PATH = os.path.join(self.CODE_SATURNE_TEMPLATE_PATH,self.CODE_SAT_ACT_XML_NAME)
        
        """
        The path to the template file for a standard code-saturne simulation.
        """
        self.CODE_SAT_STD_PATH = os.path.join(self.CODE_SATURNE_TEMPLATE_PATH,self.CODE_SAT_STD_XML_NAME)
        
        self.CODE_SAT_MESH_TEMPLATES = os.path.join(self.CODE_SATURNE_DATA_PATH,'MESHES')
        
        self.MESH_GENERATED = False
        
        self.salomeInstallLocation = self.configMap["salomeInstallLoc"]
        
        # Used to keep the server alive until all things are finished
        self.ALL_JOBS_COMPLETED = False
        
        # The globally available path to where the case is for this simulation
        self.CASE_PATH = None
        
        '''
        This is used by the bisection to tell when a job has completed...
        '''
        self.bisectionTaskDone = True
        
        # Physical constants
        self.AIR_DENSITY = self.configMap['airDensity']
        
        self.INLET_VEL = self.configMap['inletVel']
        
        self.TUNNEL_RADIUS = self.configMap['tunnelRadius']
        
        # Event for killing the server
        self.stopServerEvent = Event()
    
    def copyFile(self,src,dest):
        if os.path.exists(src):
            subprocess.call(['cp', src, dest])
            # check to make sure it exists!
            if not os.path.exists(dest):
                raise Exception("File not copied for xml, failing!>"+src+" "+dest)
        else:
            raise Exception("Src or Destination does not exist!"+src+" "+dest)
        
    def codeSaturneSim(self,name,shroudRawPoints,headLoss=0.25,meshType=meshTypes_BUILD,meshCode='',codeSatType=codeSatActDisk):
        """
        Runs a code-saturne simulation. Note this function does not work yet for standard code-saturne simulations!
        It only works for actuator disk simulations.
        """
        studyName = name+"_STUDY"
        caseName = name+"_CASE"
        studyPath = os.path.join(self.CODE_SATURNE_STUDY_PATH,studyName)
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
            self.copyFile(self.CODE_SAT_STD_PATH,os.path.join(casePath,'DATA',self.CODE_SAT_STD_XML_NAME))
            xmlFilePath = os.path.join(casePath, "DATA", self.CODE_SAT_STD_XML_NAME)
        elif codeSatType==codeSatActDisk:
            # copy the template xml to this case
            print "Copying the xml file for an actuator disk code-sat sim."
            self.copyFile(self.CODE_SAT_ACT_DISK_PATH,os.path.join(casePath,'DATA',self.CODE_SAT_ACT_XML_NAME))
            xmlFilePath = os.path.join(casePath, "DATA", self.CODE_SAT_ACT_XML_NAME)
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
    
        # Set the density of the fluid in the xml file
        density = root.findall("./physical_properties/fluid_properties/property[@label='Density']/initial_value")[0]
        density.text = str(self.AIR_DENSITY)
    
        # Set the inlet velocity
        inn = root.findall("./boundary_conditions/inlet[@label='inlet']/velocity_pressure/norm")[0]
        inn.text = self.INLET_VEL
    
        print "Set xml files, now getting or building mesh."
        meshGenDir = os.path.join(studyPath,'MESH')
        meshFileName = name+'_MESH.med'
        meshFilePath = os.path.join(meshGenDir,meshFileName)
        if meshType==meshTypes_COPY:
            self.copyFile(os.path.join(self.CODE_SAT_MESH_TEMPLATES,meshCode),os.path.join(studyPath,'MESH',meshCode))
        elif meshType==meshTypes_BUILD:
            print "Generating mesh..."
            from windmc.sim.GeneticAlgorithm import MeshGenerationTask
            #serverPort, salomeInstall, WIND_MC, generationID, generationDirectory,**genParams
            meshGenTask = MeshGenerationTask(self.SERVER_PORT,self.salomeInstallLocation,\
                                             self.WINDMC_PATH,\
                                             name, meshGenDir,\
                                             shroudPoints=shroudRawPoints,outputPath=meshFilePath)
            waitTime = self.meshingMethod.getMeshWaitTime()
            print 'codesaturnesim, got mesh wait time!>',waitTime
            time.sleep(waitTime)
            meshGenTask.run()
            print "Waiting for mesh to generate..."
            while not self.MESH_GENERATED:
                time.sleep(5)
            print "Mesh generated apparently!"
        # Set the mesh file name
        root.findall(".solution_domain/meshes_list/mesh")[0].attrib['name']=meshFileName
        
        # write out the file, we are done, time to process!
        print "Got or built mesh, now writing xml file out.:",xmlFilePath
        tree.write(xmlFilePath)
    
        self.coeffMap[studyName+'-'+caseName]=headLoss
    
        self.jobTypeMap[studyName+'-'+caseName] = codeSatType
        self.jobCasePathMap[studyName+'-'+caseName] = casePath
        # Now create the bash file that will run the code-saturne script and the python module for announcing completion
        bash = open(os.path.join(casePath,'DATA','doSaturne.sh'),'w')
        bash.write('#!/bin/sh \n')
        bash.write('code_saturne run --param '+xmlFilePath+'\n')
        #bash.write('python ' + os.path.join(CODE_SATURNE_TEMPLATE_PATH,'codeSatComplete.py')+ ' ' + str(SERVER_PORT)+' ' + studyName +' '+caseName)
        bash.write('wget http://atlacamani.marietta.edu:'+str(self.SERVER_PORT)+'/'+'jobcompleted/'+studyName+'/'+caseName)
        bash.close()
        subprocess.call(['chmod','a+x',os.path.join(casePath,'DATA','doSaturne.sh')])
        subprocess.call(['sbatch',os.path.join(casePath,'DATA','doSaturne.sh')])
        return casePath
    
    def keepServerAlive(self):
        return not self.ALL_JOBS_COMPLETED
    
    # This is so that simulations don't start simultaneously, specifically we don't want
    # salome-meca starting up concurrently with another process of salome.
    def main(self):
        import random
        sleepTime = random.randint(1,120)
        print "codesaturnesim, sleeping for ",sleepTime," before starting simulations..."
        #time.sleep(sleepTime)
        print "codesaturnesim, done sleeping!"

        #args = sys.argv[1]
        #dataMap = self.dataMap#json.loads(args)
        #shroudPoints = dataMap['shroudPoints']
        shroudPoints = self.shroudPoints
        print "codesaturnesime, the shroud points>",shroudPoints
        
        startedServer = False
        server_address = ('atlacamani.marietta.edu',int(self.SERVER_PORT))
        while not startedServer:
            print "\n---Trying to start on>",self.SERVER_PORT
            try:
                httpd_server = CodeSatHTTPServer(server_address,CodeSatServerHandler,self)
                startedServer = True
            except Exception:
                print "Failed to start on:",self.SERVER_PORT
                self.SERVER_PORT = int(self.SERVER_PORT)
                self.SERVER_PORT += 1
                self.SERVER_PORT = str(self.SERVER_PORT)
                server_address = ('atlacamani.marietta.edu',int(self.SERVER_PORT))  
                
        _id = uuid.uuid1()
                
        starter = Starter(self,_id,shroudPoints)
        starter.start()
#         httpd_server.serve_forever()
        while not self.stopServerEvent.isSet():
            httpd_server.handle_request()
#               
#         print "Shutting down http server in codesaturnesim..."
#         #httpd_server.shutdown()  
#         print "Server shut down!"
        print "The server was shut down!, is the starter thread still running?>",starter.is_alive()
        self.CASE_PATH = starter.CASE_PATH
        
        print "CodeSatSim, got a post processing finished!"
        if self.CASE_PATH == None:
            print "Didn't get a valid case path after simulation!"
            self.RETURN_CODE=0
        else:
            try:
                resultsDir = os.path.join(self.CASE_PATH,'RESU')
                resultsDir = os.listdir(resultsDir)[0]
                resultsDir = os.path.join(self.CASE_PATH,'RESU',resultsDir,'postprocessing','powerCoefficient.txt')
                powerCoeffFile = open(resultsDir,'r')
                powerCoeff = float(powerCoeffFile.readline())
                print "Returning powerCoeff>",powerCoeff
                if powerCoeff > 0.98 or powerCoeff < 0:
                    print "powerCoeff is too high or too low, exiting with zero..."
                    self.RETURN_CODE=0
                else:
                    print "Trying to exit with good powerCoeff"
                    self.RETURN_CODE = powerCoeff
            except:
                print "Failed to get a power coefficient..."
                self.RETURN_CODE=0   
                    
    def getSimResults(self):
        return self.RETURN_CODE
    
    #print doSimulation([[60,35],[70,20],[78,28],[82,28],[90,35],[110,30]])
    
        
class CodeSatHTTPServer(HTTPServer):
    """
    This class is a special version of the HTTPServer which has a connection to the
    CodeSaturneSim that started it up. This is so that handlers to requests can post
    the results back to the simulation object.
    """
    
    def __init__(self,server_address,handler,codesatsim):
        HTTPServer.__init__(self, server_address, handler)
        self.codesatsim = codesatsim
        
    def getCodeSatSim(self):
        return self.codesatsim 
    
class Starter(Thread):
    """
    This class simply starts up the code-saturne simulation method. Because we have to start
    up the server that listens to request and the method that starts up a simulation
    blocks until the mesh is finished, I created this Thread.
    """
    
    def __init__(self,codesatsim,_id,shroudPoints):
        Thread.__init__(self)
        self.codesatsim = codesatsim
        self.id = _id
        self.shroudPoints = shroudPoints
        
    def run(self):   
        casePath = self.codesatsim.codeSaturneSim(str(self.id), self.shroudPoints, 0.25, meshTypes_BUILD)    
        print "codesaturnesim..starter..run, the casePath gotten>",casePath
        self.CASE_PATH = casePath
    
    
class CodeSatServerHandler(BaseHTTPRequestHandler):
    
    def __init__(self, request, client_address, server):
        BaseHTTPRequestHandler.__init__(self, request, client_address, server)  
        
    def do_GET(self):
        'Do the parsing'
        path = self.path
        pieces = path.split('/')
        print "CodeSatSever, responding to>",path,' pieces>',pieces,(pieces[1] == 'jobcompleted'),(pieces[2]=='meshfinished')
        if pieces[1] == 'jobcompleted' and pieces[2]=='meshfinished':
            self.meshCompleted()
        elif pieces[1] == 'jobcompleted' and pieces[2]=='postprocessing':
            self.postProcessingFinished()
        elif pieces[1] == 'jobcompleted':
            self.jobCompleted(pieces[2], pieces[3])
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()            
        
    #@get('/jobcompleted/<study>/<case>')
    def jobCompleted(self,study,case):
        # Now do the post-processing
        print "Job Completed...calling post-processing."
        # Get the results directory
        global WIND_MC_PATH
        try:
            casePath = self.server.getCodeSatSim().jobCasePathMap[study+'-'+case]
            resultsDir = os.path.join(casePath,'RESU')
            resultsDir = os.listdir(resultsDir)[0]
            resultsDir = os.path.join(casePath,'RESU',resultsDir,'postprocessing')
            salomescriptbuilder.main(WIND_MC_PATH, resultsDir, case, self.server.getCodeSatSim().SERVER_PORT)
        except:
            print "There was a fatal error in the code-saturne simulation, killing server and returning 0!!!"
            self.server.getCodeSatSim().stopServerEvent.set()
            print "CodeSatServerHandler..jobCompleted..KilledServer"
        
    #@get('/jobcompleted/meshfinished')
    def meshCompleted(self):
        print "codesaturnesim.server, meshComplted, setting to TRUE"
        self.server.getCodeSatSim().MESH_GENERATED = True
    
    #@get('/jobcompleted/postprocessing')
    def postProcessingFinished(self):
        print "CodeSatServerHandler..postProcFinished"
        self.server.getCodeSatSim().ALL_JOBS_COMPLETED=True
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers() 
        print "CodeSatServerHandler..Killing server..." 
        #self.server.shutdown()
        self.server.getCodeSatSim().stopServerEvent.set()
        print "CodeSatServerHandler..KilledServer"