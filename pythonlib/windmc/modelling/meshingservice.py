'''
Created on Mar 6, 2014

@author: vance
'''
from threading import Thread, Lock
from Queue import Queue
import os, subprocess, time, json
from bottle import run, get, post, request
from multiprocessing import Process

# The Queue of meshes we need to make
meshTaskQueue = Queue(300)

# lock to hold mesh task queues
theLock = Lock()

# How often should we clean up after salome?
cleanUpRate = 10

# How long should we wait for a meshing job comes in before starting the group up
pollTime = 5

# What is the max number of mesh jobs to run at a given time.
meshGroupSize = 15

# How long to wait between starting a process
startUpDelay = 15

def runMeshTask(meshtask):
    meshGenTask = MeshGenerationTask(meshtask['serverPort'], meshtask['salomeInstall'], 
                                     meshtask['WIND_MC'], meshtask['generationID'], 
                                     meshtask['generationDirectory'], meshtask['otherData'])
    print "Created mesh generation task!"
    meshGenTask.run()
    print "Mesh gentask finished"

class MeshingService(Thread):
 
    def __init__(self):
        Thread.__init__(self)
        print "Creating a new MeshingService!"
        self.alive=True
        self.counter = 0
 
    def run(self):
        print "MeshingService...running"
        while(self.alive):
            print "MeshingService, checking the task queue..."
            if not meshTaskQueue.empty():
                meshJobs = []
                print "Getting jobs from queue..."
                for i in range(meshGroupSize):
                    print "Waiting to get job:",i
                    try:
                        meshJobs.append(meshTaskQueue.get(True, pollTime))
                    except:
                        pass
                print "Got jobs:",len(meshJobs)
                processes = []
                for job in meshJobs:
                    process = Process(target=runMeshTask, args=(job,))
                    processes.append(process)
                    process.start()
                    time.sleep(startUpDelay)
                # Wait until all are done
                for process in processes:
                    if process.is_alive():
                        process.join()
                        
                print "All done, now killing salome..."
                subprocess.call(['/home/vance/killAllSalome.sh'])
                print 'Killed salome!'
            else:
                print "MeshingService...sleeping"
                time.sleep(3)
        print "MeshingService...exiting"
         
    def kill(self):
        self.alive = False      

def copyFile(src,dest):
    if os.path.exists(src):
        subprocess.call(['cp', src, dest])
        # check to make sure it exists!
        if not os.path.exists(dest):
            raise Exception("File not copied for xml, failing!>"+src+" "+dest)
    else:
        raise Exception("Src or Destination does not exist!"+src+" "+dest)

class MeshGenerationTask(Thread):
    def __init__(self, serverPort, salomeInstall, WIND_MC, generationID, generationDirectory,otherDataMap):
        Thread.__init__(self)
        self.genParams = otherDataMap
        self.genID = generationID
        self.genDir = generationDirectory
        self.salomeInstallLoc = salomeInstall
        self.windMC = WIND_MC
        self.serverPort = serverPort

    def run(self):
        commandList = []
        commandList.append(os.path.join(self.salomeInstallLoc, 'runAppli'))
        commandList.append('-t')
        commandList.append(os.path.join(self.genDir, 'tunnelscript.py'))
        # Copy the mesh generation script into the study MESH directory
        copyFile(os.path.join(self.windMC,'modelling','tunnelscript.py'),\
                  os.path.join(self.genDir,'tunnelscript.py'))
        # Copy the json file into the MESh directory
        copyFile(os.path.join(self.windMC,'modelling','actuator.json'),\
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
        bash.write(os.path.join(self.salomeInstallLoc, 'runAppli')+' -t '+os.path.join(self.genDir, 'tunnelscript.py')+'\n')
        #bash.write('python ' + os.path.join(CODE_SATURNE_TEMPLATE_PATH,'codeSatComplete.py')+ ' ' + str(SERVER_PORT)+' ' + studyName +' '+caseName)
        bash.write('wget http://atlacamani.marietta.edu:'+str(self.serverPort)+'/'+'jobcompleted/meshfinished')
        bash.close()
        subprocess.call(['chmod','a+x',meshSh])
        #subprocess.call(['sbatch',meshSh])
        subprocess.call([os.path.join(self.genDir,'doMeshing.sh')],stdout=output)    
        #subprocess.call(commandList,stdout=output)
        output.close()
#         print "MeshGenerationTask, mesh gen command finished!"
#         with theLock:
#             print "Now testing for more tasks?>",meshTaskQueue.empty()
#             if not meshTaskQueue.empty():
#                 aTask = meshTaskQueue.get(False)
#                 print "Got a task from the queue?>",aTask
#                 if not aTask==None:
#                     aTask.start()
#         print "Finishing our task..."
        
        
@post('/meshrequest/')
def postMeshJob():
    #serverPort, salomeInstall, WIND_MC, generationID, generationDirectory,**genParams
    serverPort = request.forms.get("serverPort")
    salomeInstall = request.forms.get("salomeInstall")
    WIND_MC = request.forms.get("WIND_MC")
    generationID = request.forms.get("generationID")
    generationDirectory = request.forms.get("generationDirectory")
    otherData = json.loads(request.forms.get("otherData"))
    print "meshingservice, got a job and data>",serverPort,salomeInstall,WIND_MC,generationID,generationDirectory,otherData
    with theLock:
        print "Acquired the lock!"
        meshTaskQueue.put({'serverPort':serverPort,'salomeInstall':salomeInstall,'WIND_MC':WIND_MC,
                           'generationID':generationID,'generationDirectory':generationDirectory,
                           'otherData':otherData})
    return "Job submitted!"

@get('/info')
def getInfo():
    return "You have reached the meshing service!"

@get('/jobs')
def getJobCount():
    count = -1
    with theLock:
        count = meshTaskQueue.qsize()
    print "Got the job count?>",count
    return str(count) 

@get('/killSalome')
def killSalome():
    subprocess.call(['/home/vance/killAllSalome.sh'])
    return "Killed salome"

if __name__=="__main__":
    node = input("Enter node number:")
    thePort = input("Enter port:")
    meshingService = MeshingService()
    meshingService.start()
    run(host='atlacamani'+str(node), port=thePort)