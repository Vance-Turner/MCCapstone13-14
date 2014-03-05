'''
Created on Mar 4, 2014

@author: vance
'''

def saturneEvaluator(chromosome):
    # Extract points
    shroudPoints = []
    print "saturneEvaluator, evaluating>"#chromosome
    xpoints = []
    for i in range(0,44,2):
        if not chromosome[i] in xpoints:
            shroudPoints.append([chromosome[i],chromosome[i+1]])  
            xpoints.append(chromosome[i])
    shroudPoints.sort(key=lambda item: item[0])
    from windmc.sim import codesaturnesim
    print "About to start sim!>",shroudPoints
    powerCoeff = codesaturnesim.doSimulation(shroudPoints)
    print "Got power coeff from sim>",powerCoeff
    return powerCoeff

if __name__ == '__main__':
#     from windmc.sim import codesaturnesim
#     codesaturnesim.doSimulation([[60,35],[70,20],[78,28],[82,28],[90,35],[110,30]])
    from pyevolve import GAllele, G1DList, GSimpleGA
    from pyevolve import Mutators, Initializators, DBAdapters
     
    verticalAlleles = GAllele.GAlleleRange(15,50,False)#True)
    horizontalAlleles1 = GAllele.GAlleleRange(52,75,False)#True)
    horizontalAlleles2 = GAllele.GAlleleRange(85,108,False)#$True)
     
    # The alleles for the middle points
    point1XAllele = GAllele.GAlleleList([78])
    point1YAllele = GAllele.GAlleleList([28])
    point2XAllele = GAllele.GAlleleList([82])
    point2YAllele = GAllele.GAlleleList([28])
     
    # Create the allele object
    galleles = GAllele.GAlleles()
    for i in range(10):
        galleles.add(horizontalAlleles1)
        galleles.add(verticalAlleles)
         
    galleles.add(point1XAllele)
    galleles.add(point1YAllele)
    galleles.add(point2XAllele)
    galleles.add(point2YAllele)
     
    for i in range(10):
        galleles.add(horizontalAlleles2)
        galleles.add(verticalAlleles)
         
    genome = G1DList.G1DList(44)
    genome.evaluator.set(saturneEvaluator)
    genome.setParams(allele=galleles)
    genome.mutator.set(Mutators.G1DListMutatorAllele)
    genome.initializator.set(Initializators.G1DListInitializatorAllele)
 
    geneticAlg = GSimpleGA.GSimpleGA(genome)
    csvfile_adapter = DBAdapters.DBFileCSV('output1.csv')
    geneticAlg.setDBAdapter(csvfile_adapter)
    geneticAlg.setMultiProcessing(True)
    geneticAlg.setGenerations(4)
    print "Preparing to evolve..."
    geneticAlg.evolve(1)
    print geneticAlg.bestIndividual()
    csvfile_adapter.commitAndClose()