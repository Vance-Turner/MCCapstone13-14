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
    columns = []
    output = open(os.path.join(postProcPath,'pandasout.txt'),'w')
    output.write("Doing pandas post proc!!")
    for i in range(200):
        columns.append(str(i))
        
    pressureFile = os.path.join(postProcPath,caseName+'_pressure_.csv')
    df = pd.read_csv(pressureFile)
    #print df
    df.columns = columns
    pressureInlet = df[0:1].mean(axis=1)[0]
    
    pressureOutletFile = os.path.join(postProcPath,caseName+'_outlet_pressure_.csv')
    df = pd.read_csv(pressureOutletFile)
    df.columns = columns
    pressureOutlet = df[0:1].mean(axis=1)[0]
    
    columns = []
    for i in range(400):
        columns.append(str(i))
        
    diskVelocityFile = os.path.join(postProcPath,caseName+'_diskInlet_velocity_.csv')
    df = pd.read_csv(diskVelocityFile)
    df.columns = columns
    diskVelocity = df[0:1].mean(axis=1)[0]        
    
    inletVelocityFile = os.path.join(postProcPath,caseName+'_velocity_.csv')
    df = pd.read_csv(inletVelocityFile)
    df.columns = columns
    velocityInlet = df[0:1].mean(axis=1)[0]
    output.write("Finished pandas!!>")
    output.close()
    with open(os.path.join(postProcPath,'powerCoefficient.txt'),'wb') as output:
        output.write(str((pressureInlet-pressureOutlet)*diskVelocity/(0.5*1.2929*(velocityInlet**3))))    
    print "Finished pandas processing, found power coeff>",((pressureInlet-pressureOutlet)*diskVelocity/(0.5*1.2929*(velocityInlet**3)))
