'''
Created on Mar 4, 2014

@author: vance
'''

import json
import subprocess
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
    
def saturneEvaluator(chromosome):
    # Extract points
#     import random
#     time.sleep(random.randint(0,20))
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
    return float(runner.getResults())*100

generationCounter= 0
def generationCallBack(ga_engine):
    print "Cleaning up after a generation:",ga_engine.getCurrentGeneration()
    currentGen = ga_engine.getCurrentGeneration()
    subprocess.call([WINDMC_PATH+'/../cleanUp.sh',str(currentGen)])
    print "Cleaned up!"

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
    Consts.CDefGAPopulationSize = 120
    geneticAlg = GSimpleGA.GSimpleGA(genome)
    csvfile_adapter = DBAdapters.DBSQLite(identify="Mar14_Gen3",frequency=1,commit_freq=1)#DBAdapters.DBFileCSV('output1.csv')
    geneticAlg.setDBAdapter(csvfile_adapter)
    geneticAlg.stepCallback.set(generationCallBack)
    #geneticAlg.setPopulationSize(80)
    geneticAlg.setGenerations(50)
    #geneticAlg.setMinimax(Consts.minimaxType["maximize"])
    geneticAlg.setMultiProcessing(True)
    geneticAlg.evolve(1)
    #geneticAlg.setGenerations(2)
#     print "Preparing to evolve..."
#     geneticAlg.evolve(1)
    print geneticAlg.bestIndividual()
    #geneticAlg.dumpStatsDB()
    #csvfile_adapter.commitAndClose()