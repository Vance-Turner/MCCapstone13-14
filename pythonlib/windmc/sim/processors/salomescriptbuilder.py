'''
Created on Mar 2, 2014

@author: vance
'''
import os

def buildPostProcessScript(inputFile,outputPath,outputID,windMCPath,tunnelWidth=100.0,actuatorX=78.0,actuatorRadius=4.0,\
                           diskPoints=30,radiusPoints=10,\
                           inletRadius=90.0,inletLoc=5.0,inletRadialPoints = 20,inletCircumFerentialPoints=30):
    pyFyName = os.path.join(outputPath,'post_proc_'+str(outputID)+'.py')
    with open(pyFyName,'wb') as pyFy:
        # First read in and write out the code that extracts the information from the MED file
        with open(os.path.join(windMCPath,'sim','processors','medinfoextractor.py'),'r') as medinfo:
            for line in medinfo:
                pyFy.write(line)
        # Now write out the code that will call the appropriate functions
        args = ','.join(map(str,[tunnelWidth,actuatorX,actuatorRadius,'"'+inputFile+'"','"'+outputPath+'"','"'+outputID+'"',diskPoints,radiusPoints]))
        print "Args gotten>",args
        pyFy.write('\n')
        pyFy.write('extractPressure('+args+')\n')
        args = ','.join(map(str,[tunnelWidth,actuatorX+4,actuatorRadius,'"'+inputFile+'"','"'+outputPath+'"','"'+outputID+'_outlet"',diskPoints,radiusPoints]))
        pyFy.write('extractPressure('+args+')\n')
        
        args = ','.join(map(str,[inletRadius,inletLoc,'"'+inputFile+'"','"'+outputPath+'"','"'+outputID+'"'\
                                 ,inletCircumFerentialPoints,inletRadialPoints,0]))
        pyFy.write('extractVelocity('+args+')\n')
        args = ','.join(map(str,[actuatorRadius,actuatorX,'"'+inputFile+'"','"'+outputPath+'"','"'+outputID+'_diskInlet"'\
                                 ,inletCircumFerentialPoints,inletRadialPoints,0]))       
        pyFy.write('extractVelocity('+args+')\n')
        pyFy.write('import runSalome\n')
        '''
        How to kill salome:
        import os
        from killSalomeWithPort import killMyPort
        killMyPort(os.getenv('NSPORT'))
        '''
        pyFy.write('import os\n')
        pyFy.write('from killSalomeWithPort import killMyPort\n')
        pyFy.write('killMyPort(os.getenv(\'NSPORT\'))\n')
        return pyFyName
     
def main(baseDir):
    
    from threading import Thread
    class runner(Thread):
        
        def __init__(self,id_,inputPath):
            Thread.__init__(self)
            self._id = id_
            self._inputPath = inputPath
            
        def run(self):
            outputPath = self._inputPath
            meshFile = os.path.join(outputPath,'resultsMED.med')
            print "Mesh file>",meshFile
            outputID = str(self._id)
            tunnelWidth = 100.0
            actuatorX = 78.0
            actuatorRadius = 3.9
            diskPoints = 10
            radiusPoints = 20
            inletRadialPoints = 30
            inletCircumPoints = 20   
            windMCPath = os.path.join(baseDir,'windmc')         
            pyFy = buildPostProcessScript(meshFile, outputPath, outputID, windMCPath, tunnelWidth, actuatorX, actuatorRadius, diskPoints, radiusPoints,\
                                  inletRadialPoints = inletRadialPoints,inletCircumFerentialPoints=inletCircumPoints)
            print "pyFy>",pyFy
            import subprocess
            salomeLoc = "/home/vance/salome_2014/appli_V7_3_0"
            shFile = os.path.join(outputPath,'doSaturne_'+str(self._id)+'.sh')
            bash = open(shFile,'w')
            bash.write('#!/bin/sh \n')
            bash.write(os.path.join(salomeLoc,'runAppli')+' -t '+os.path.join(outputPath,pyFy))
            bash.close()
            subprocess.call(['chmod','a+x',shFile])
            subprocess.call(['sbatch',shFile])
    
    basePath = os.path.join(baseDir,"cluster","code_saturne","STUDIES")
    simS = os.listdir(basePath)
    import time
    for sim in simS:
        # Get case directory
        dirs = os.listdir(os.path.join(basePath,sim))
        simPath = ''
        for adir in dirs:
            if adir[0]=='s':
                simPath = adir
                break
        print "Got sim path>",simPath
        resuDir = os.path.join(basePath,sim,simPath,'RESU')
        resu = os.listdir(resuDir)[0]
        outputPath = os.path.join(resuDir,resu,'postprocessing')
        runner(sim,outputPath).start()
        time.sleep(5)
        
if __name__ == '__main__':
    # The windmc path must be set!
    baseDir = None
    if baseDir==None:
        raise Exception('Must set the base directory to do salome post-processing!')
    else:
        main(baseDir)
         