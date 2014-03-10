'''
Created on Mar 4, 2014

@author: vance
'''
import pandas as pd
import os

if __name__ == '__main__':
    import sys
    postProcPath = sys.argv[1]
    caseName = sys.argv[2]
    output = open(os.path.join(postProcPath,'pandasout.txt'),'w')
    output.write("Doing pandas post proc!!")
        
    pressureFile = os.path.join(postProcPath,caseName+'_pressure_.csv')
    df = pd.read_csv(pressureFile)
    #print df
    # This adapts to the number of columns post-processed. Salome sometimes messes up and can't read a value.
    columns = []
    for i in range(len(df.columns)):
        columns.append(str(i))    
    df.columns = columns
    pressureInlet = df[0:1].mean(axis=1)[0]
    
    pressureOutletFile = os.path.join(postProcPath,caseName+'_outlet_pressure_.csv')
    df = pd.read_csv(pressureOutletFile)
    # This adapts to the number of columns post-processed. Salome sometimes messes up and can't read a value.
    columns = []
    for i in range(len(df.columns)):
        columns.append(str(i)) 
    df.columns = columns
    pressureOutlet = df[0:1].mean(axis=1)[0]
        
    diskVelocityFile = os.path.join(postProcPath,caseName+'_diskInlet_velocity_.csv')
    df = pd.read_csv(diskVelocityFile)
    # This adapts to the number of columns post-processed. Salome sometimes messes up and can't read a value.
    columns = []
    for i in range(len(df.columns)):
        columns.append(str(i)) 
    df.columns = columns
    diskVelocity = df[0:1].mean(axis=1)[0]        
    
    inletVelocityFile = os.path.join(postProcPath,caseName+'_velocity_.csv')
    df = pd.read_csv(inletVelocityFile)
    # This adapts to the number of columns post-processed. Salome sometimes messes up and can't read a value.
    columns = []
    for i in range(len(df.columns)):
        columns.append(str(i)) 
    df.columns = columns
    velocityInlet = df[0:1].mean(axis=1)[0]
    
    output.write("Finished pandas!!>")
    output.close()
    with open(os.path.join(postProcPath,'powerCoefficient.txt'),'wb') as output:
        output.write(str((pressureInlet-pressureOutlet)*diskVelocity/(0.5*1.2929*(velocityInlet**3))))    
    print "Finished pandas processing, found power coeff>",((pressureInlet-pressureOutlet)*diskVelocity/(0.5*1.2929*(velocityInlet**3)))
