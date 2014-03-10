'''
Created on Mar 6, 2014

@author: vance
'''

import uuid
meshingJobs = {}
from threading import Thread
import os, subprocess, time, json
from multiprocessing import Queue, Process

class MeshingService(Thread):

    def __init__(self):
        Thread.__init__(self)
        print "Creating a new MeshingService!"
        self.meshTaskQueue = Queue(300)
        self.alive=True

    def run(self):
        print "MeshingService...running"
        while(self.alive):
            print "MeshingService, checking the task queue..."
            if not self.meshTaskQueue.empty():
                print "MeshingService, got a job!"
                lst = self.meshTaskQueue.get()
                print "MeshingService, starting a job!"
                lst[0].start()
            else:
                print "MeshingService...sleeping"
                time.sleep(30)
        print "MeshingService...exiting"
        
    def kill(self):
        self.alive = False

    def submitJob(self,task):
        print "MeshingService, received a meshing task job!"
        _id = uuid.uuid1()
        self.meshTaskQueue.put([task,_id])
        print "MeshingService...added job to task queue"
        return _id       

def copyFile(src,dest):
    if os.path.exists(src):
        subprocess.call(['cp', src, dest])
        # check to make sure it exists!
        if not os.path.exists(dest):
            raise Exception("File not copied for xml, failing!>"+src+" "+dest)
    else:
        raise Exception("Src or Destination does not exist!"+src+" "+dest)

class MeshGenerationTask(Thread):
    def __init__(self, serverPort, salomeInstall, WIND_MC, generationID, generationDirectory,**genParams):
        Thread.__init__(self)
        self.genParams = genParams
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
        subprocess.call(['sbatch',meshSh])
        #subprocess.call([os.path.join(self.genDir,'doMeshing.sh')],stdout=output)    
        #subprocess.call(commandList,stdout=output)
        output.close()
        print "MeshGenerationTask, mesh gen command finished!"