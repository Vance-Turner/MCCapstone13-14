'''
Created on Mar 4, 2014

@author: vance
'''

import json
import os
import subprocess
import calendar, time
from multiprocessing import Lock, Value
from threading import Thread
jsonFile = open('config.json')
configMap = json.load(jsonFile)
jsonFile.close()

SERVER_PORT = configMap['serverPort']
SERVER_DATA_PATH = configMap['serverDataPath']
WINDMC_PATH = configMap['windmcPath']

"""
Controls what we do when we find a duplicate
gene in x in a chromosome.
"""
IGNORE_DUPLICATE_GENE = True

class MeshStaller():
    
    def __init__(self):
        self.lastTime = Value('f',calendar.timegm(time.gmtime()))
        self.waitTime = Value('i',0)
        self.meshLock = Lock()
        self.stallTime = 15

    def getMeshWaitTime(self):
        with self.meshLock:
                currentTime = calendar.timegm(time.gmtime())
                print self.lastTime.value,currentTime,(currentTime-self.lastTime.value)
                if (currentTime-self.lastTime.value) > self.stallTime:
                        self.lastTime.value = currentTime
                        self.waitTime.value = 0
                        return self.waitTime.value
                else:
                        self.lastTime.value = currentTime
                        self.waitTime.value += self.stallTime
                        return self.waitTime.value
    
def copyFile(src,dest):
    if os.path.exists(src):
        subprocess.call(['cp', src, dest])
        # check to make sure it exists!
        if not os.path.exists(dest):
            raise Exception("File not copied for xml, failing!>"+src+" "+dest)
    else:
        raise Exception("Src or Destination does not exist!"+src+" "+dest)

meshstaller = MeshStaller()

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
    
def saturneEvaluator(chromosome):
    # Extract points
    shroudPoints = []
    print "saturneEvaluator, evaluating>"#chromosome
    xpoints = []
    for i in range(0,20,2):
        if not chromosome[i] in xpoints:
            if IGNORE_DUPLICATE_GENE:
                shroudPoints.append([chromosome[i],chromosome[i+1]])  
                xpoints.append(chromosome[i])
            else:
                return 0
        else:
            print "Found duplicate chromosome, ignoring!"
    shroudPoints.sort(key=lambda item: item[0])
    print "About to start sim!>",shroudPoints
    global WINDMC_PATH
    jsonData = json.dumps({'shroudPoints':shroudPoints})
    class Runner(Thread):
        
        def __init__(self,shroudPts,jsonData):
            Thread.__init__(self)
            self.shroudPoints = shroudPts
            self.jsonData = jsonData
            
        def run(self):
            from windmc.sim.codesaturnesim import CodeSaturneSim
            codeSatSim = CodeSaturneSim(self.shroudPoints,self.jsonData)
            codeSatSim.main()
            self.result = codeSatSim.getSimResults()
            
        def getResults(self):
            return self.result
    runner = Runner(shroudPoints,jsonData)
    runner.start()
    runner.join()
    #returnCode = subprocess.call(['python','-m','windmc.sim.codesaturnesim',jsonData])
    #powerCoeff = codesaturnesim.doSimulation(shroudPoints)
    print "Got power coeff from sim>",runner.getResults()
    return float(runner.getResults())

if __name__ == '__main__':
#     from windmc.sim import codesaturnesim
#     codesaturnesim.doSimulation([[60,35],[70,20],[78,28],[82,28],[90,35],[110,30]])
    
    from pyevolve import GAllele, G1DList, GSimpleGA
    from pyevolve import Mutators, Initializators, DBAdapters
     
    verticalAlleles = GAllele.GAlleleRange(10,25,False)#True)
    horizontalAlleles1 = GAllele.GAlleleRange(26,38,False)#True)
    horizontalAlleles2 = GAllele.GAlleleRange(43,54,False)#$True)
     
    # The alleles for the middle points
    point1XAllele = GAllele.GAlleleList([39])
    point1YAllele = GAllele.GAlleleList([14])
    point2XAllele = GAllele.GAlleleList([41])
    point2YAllele = GAllele.GAlleleList([14])
     
    # Create the allele object
    galleles = GAllele.GAlleles()
    for i in range(4):
        galleles.add(horizontalAlleles1)
        galleles.add(verticalAlleles)
         
    galleles.add(point1XAllele)
    galleles.add(point1YAllele)
    galleles.add(point2XAllele)
    galleles.add(point2YAllele)
     
    for i in range(4):
        galleles.add(horizontalAlleles2)
        galleles.add(verticalAlleles)
         
    genome = G1DList.G1DList(20)
    genome.evaluator.set(saturneEvaluator)
    genome.setParams(allele=galleles)
    genome.mutator.set(Mutators.G1DListMutatorAllele)
    genome.initializator.set(Initializators.G1DListInitializatorAllele)
 
    from pyevolve import Consts
    Consts.CDefGAPopulationSize = 30
    geneticAlg = GSimpleGA.GSimpleGA(genome)
    csvfile_adapter = DBAdapters.DBFileCSV('output1.csv')
    geneticAlg.setDBAdapter(csvfile_adapter)
    geneticAlg.setMultiProcessing(True)
    geneticAlg.setGenerations(1)
    print "Preparing to evolve..."
    geneticAlg.evolve(1)
    print geneticAlg.bestIndividual()
    csvfile_adapter.commitAndClose()