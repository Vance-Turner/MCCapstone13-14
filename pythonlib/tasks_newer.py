__author__ = 'vance'

from threading import Thread
import os
import time
import json
import subprocess
import xml.etree.ElementTree as ET
from processors.codesaturne import getInletOutletVelocity
from bottle import route, run, static_file, get

"""
Holds results of code-saturne jobs. The key is the job id and the value is the energy extracted.
"""
jobTypeMap = {}
coeffMap = {}
resultsMap = {}
velResMap = {}

jsonFile = open('config.json')
configMap = json.load(jsonFile)
jsonFile.close()

SERVER_PORT = 2000

CODE_SATURNE_DATA_PATH = os.path.join(configMap['serverDataPath'],'code_saturne')
CODE_SATURNE_STUDY_PATH = os.path.join(CODE_SATURNE_DATA_PATH,'STUDIES')
CODE_SATURNE_TEMPLATE_PATH = os.path.join(CODE_SATURNE_DATA_PATH,'TEMPLATES')

CODE_SAT_ACT_XML_NAME = 'actuator_disk_case_3.xml'#'actuator_disk_case.xml'
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

'''
This is used by the bisection to tell when a job has completed...
'''
bisectionTaskDone = True

def copyFile(src,dest):
    if os.path.exists(src):
        subprocess.call(['cp', src, dest])
        # check to make sure it exists!
        if not os.path.exists(dest):
            raise Exception("File not copied for xml, failing!>"+src+" "+dest)
    else:
        raise Exception("Src or Destination does not exist!"+src+" "+dest)

def postProcessCodSatActDisk(study,case,resultsPath):
    print "Post process code saturne!!"
    global bisectionTaskDone
    bisectionTaskDone = True
    '''
    result = getInletOutletVelocity(resultsPath)
    inletVel = result['probe1']
    outletVel = result['probe4']
    energyExtracted = ((outletVel**3-inletVel**3)/inletVel**3)
    print "Inlet:",inletVel,"Outlet:",outletVel,"Energy Extracted:",((outletVel**3-inletVel**3)/inletVel**3)
    resultsMap[coeffMap[study+'-'+case]]=energyExtracted
    velResMap[coeffMap[study+'-'+case]]=result
    '''


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
        xmlFilePath = os.path.join(casePath, "DATA", CODE_SAT_STD_XML_NAME)
    elif codeSatType==codeSatActDisk:
        # copy the template xml to this case
        print "Copying the xml file for an actuator disk code-sat sim."
        copyFile(CODE_SAT_ACT_DISK_PATH,os.path.join(casePath,'DATA',CODE_SAT_ACT_XML_NAME))
        xmlFilePath = os.path.join(casePath, "DATA", CODE_SAT_ACT_XML_NAME)
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
    print "Got or built mesh, now writing xml file out.:",xmlFilePath
    tree.write(xmlFilePath)

    coeffMap[studyName+'-'+caseName]=headLoss

    jobTypeMap[studyName+'-'+caseName] = codeSatType
    # Now create the bash file that will run the code-saturne script and the python module for announcing completion
    bash = open(os.path.join(casePath,'DATA','doSaturne.sh'),'w')
    bash.write('#!/bin/sh \n')
    bash.write('code_saturne run --param '+xmlFilePath+'\n')
    #bash.write('python ' + os.path.join(CODE_SATURNE_TEMPLATE_PATH,'codeSatComplete.py')+ ' ' + str(SERVER_PORT)+' ' + studyName +' '+caseName)
    bash.write('wget http://atlacamani.marietta.edu:'+str(SERVER_PORT)+'/'+'jobcompleted/'+studyName+'/'+caseName)
    bash.close()
    subprocess.call(['chmod','a+x',os.path.join(casePath,'DATA','doSaturne.sh')])
    subprocess.call(['sbatch',os.path.join(casePath,'DATA','doSaturne.sh')])
    return casePath

@get('/jobcompleted/<study>/<case>')
def jobCompleted(study,case):
    codeSatType = jobTypeMap[study+'-'+case]
    # Now do the post-processing
    print "Job Completed..."
    if codeSatType==codeSatActDisk:
        print "Doing post-processing..."
        postProcessCodSatActDisk(study,case,os.path.join(CODE_SATURNE_STUDY_PATH,study,case,'RESU'))
    else:
        print "Job completed was not a code-sat-act-disk type!"

@route('/currentResults')
def getCurrentResults():
    csvFile = open(os.path.join(CODE_SATURNE_DATA_PATH,'temp.csv'),'w')
    import csv
    writer = csv.writer(csvFile)
    keys = resultsMap.keys()
    for key in keys:
        veloc = velResMap[key]
        writer.writerow([key,veloc['probe1'],veloc['probe2'],veloc['probe3'],\
                         veloc['probe4'],veloc['probe5'],veloc['probe6'],veloc['probe7'],resultsMap[key]])
    csvFile.close()
    return static_file('temp.csv',CODE_SATURNE_DATA_PATH,download=True)


class AxialInductionTask(Thread):

    def __init__(self,lowerHeadLoss,upperHeadLoss,taskId):
        Thread.__init__(self)
        self._lowerHeadLoss = lowerHeadLoss
        self._upperHeadLoss = upperHeadLoss
        self._taskId = taskId

    def run(self):
        self.doSim(self._lowerHeadLoss)

    def doSim(self,headLoss):
        #codeSaturneSim('sim_'+str(self._lowerHeadLoss),self._lowerHeadLoss,meshTypes_COPY,'actuator_disk_tunnel.med',codeSatActDisk)
        codeSaturneSim('sim_'+str(self._lowerHeadLoss),self._lowerHeadLoss,meshTypes_COPY,'WindTunnel_HD.med',codeSatActDisk)



class MainControllerTask(Thread):

    def run(self):
        for i in xrange(0,500):
            task = AxialInductionTask(float(i),1,'task_'+str(float(i)))
            task.start()
        # task = AxialInductionTask(0.5,0.5,'task_0.5')
        # task.start()

import pandas as pd
import os
import time

class AxialBisectionTask(Thread):

    def __init__(self,lowerGuess,upperGuess):
        Thread.__init__(self)
        self.a = lowerGuess
        self.b = upperGuess
        # Holds information from process: a, b, p, powerCoeff(a), powerCoeff(b), powerCoeff(p),
        self.data = []

    def run(self):
        global bisectionTaskDone
        #mesh = #'actuator_disk_tunnel.med'#'WindTunnel_HD.med'
        mesh = 'WindTunnel_HD.med'
        row = []
        row.append(self.a)
        row.append(self.b)
        row.append(self.a+(self.b-self.a)/2.0)
        print "Starting up code-sat for initial guess a:",self.a
        bisectionTaskDone = False
        casePath = codeSaturneSim('sim_'+str(self.a),self.a,meshTypes_COPY,mesh,codeSatActDisk)
        print "Got back casePath from sim>",casePath
        while bisectionTaskDone == False:
            time.sleep(1)
        resuPath = os.path.join(casePath,'RESU',os.listdir(os.path.join(casePath,'RESU'))[0])
        print "Searching for results in>",resuPath
        row.append(self.getPowerCoeff(resuPath))

        print "Starting up code-sat for initial guess b:",self.b
        bisectionTaskDone = False
        casePath = codeSaturneSim('sim_'+str(self.b),self.b,meshTypes_COPY,mesh,codeSatActDisk)
        while bisectionTaskDone == False:
            time.sleep(1)
        resuPath = os.path.join(casePath,'RESU',os.listdir(os.path.join(casePath,'RESU'))[0])
        print "Searching for results in>",resuPath
        row.append(self.getPowerCoeff(resuPath))

        print "Starting up code-sat for initial guess p:",row[2]
        bisectionTaskDone = False
        casePath = codeSaturneSim('sim_'+str(row[2]),row[2],meshTypes_COPY,mesh,codeSatActDisk)
        while bisectionTaskDone == False:
            time.sleep(1)
        resuPath = os.path.join(casePath,'RESU',os.listdir(os.path.join(casePath,'RESU'))[0])
        print "Searching for results in>",resuPath
        row.append(self.getPowerCoeff(resuPath))

        seriesLabels = ['a','b','p','Cp(a)','Cp(b)','Cp(p)']
        self.data.append(row)

        #Now let's start bisecting
        currentPowerCoeff = row[5]
        iterations = 1
        while abs(currentPowerCoeff-0.593) > 0.001:
            currentRow = self.data[-1]
            newRow = [0,0,0,0,0,0]
            if currentRow[3] < 0.593 and currentRow[5] > 0.593:
                # The headloss we seek is between the left bound and the middle guess
                # Set the new left bound as the old one
                newRow[0] = currentRow[0]
                # Set the new right bound as the guess of the old row
                newRow[1] = currentRow[2]
                # Set the new guess location
                newRow[2] = newRow[0] + (newRow[1]-newRow[0])/2.0
                # Set the value at our left bound as the value of at the old left bound since they are the same
                newRow[3] = currentRow[3]
                # Set the value at the right bound as the value at the old guess since that location is now our right bound
                newRow[4] = currentRow[5]
            else:
                # The headloss we seek is between the guess and the right bound
                # Set the left bound as the guess location of the old
                newRow[0] = currentRow[2]
                # Set the right bound as the right bound of the old
                newRow[1] = currentRow[1]
                # Set the new guess
                newRow[2] = newRow[0] + (newRow[1]-newRow[0])/2.0
                # Set the value at the left bound as the value at the old guess
                newRow[3] = currentRow[5]
                # Set the value at the right bound as the value at the old right bound
                newRow[4] = currentRow[4]
            bisectionTaskDone = False
            casePath = codeSaturneSim('sim_'+str(newRow[2]),newRow[2],meshTypes_COPY,mesh,codeSatActDisk)
            while bisectionTaskDone == False:
                time.sleep(1)
            resuPath = os.path.join(casePath,'RESU',os.listdir(os.path.join(casePath,'RESU'))[0])
            newRow[5]=self.getPowerCoeff(resuPath)
            print "Adding row:",newRow
            print "Current before Pandas>\n",self.data
            self.data.append(newRow)
            mp = {}
            for i in range(len(self.data)):
                print "Creating series:",self.data[i]
                mp[str(i)]=pd.Series(self.data[i],seriesLabels)
                print "Created series>",mp[str(i)]
            labels = ['a','b','p','Cp_a','Cp_b','Cp_p']
            df = pd.DataFrame(mp,seriesLabels)
            iterations+=1
            print "After iteration ",(iterations)
            print df
            ff = open('Bisection_'+str(time.time())+'.log','w')
            ff.write(df.__str__())
            ff.close()
            csvOut = 'Bisection_'+str(time.time())+'_.csv'
            df.to_csv(csvOut)
            currentPowerCoeff = self.data[-1][5]

        mp = {}
        for i in range(len(self.data)):
            print "Creating series:",self.data[i]
            mp[str(i)]=pd.Series(self.data[i],seriesLabels)
            print "Created series>",mp[str(i)]
        labels = ['a','b','p','Cp_a','Cp_b','Cp_p']
        df = pd.DataFrame(mp,seriesLabels)
        iterations+=1
        print "After iteration ",(iterations)
        print df

        ff = open('Bisection_'+str(time.time())+'.log','w')
        ff.write(df.__str__())
        ff.close()
        csvOut = 'Bisection_'+str(time.time())+'_.csv'
        df.to_csv(csvOut)
        print "Final head loss>",self.data[-1][2],' Cp>',self.data[-1][5]


    def getPowerCoeff(self,path):
        print "Get Power Coeff, path>",path
        monPath = os.path.join(path,'monitoring')
        print "Monitoring path>",monPath
        dfx = pd.read_csv(os.path.join(monPath,'probes_VelocityX.csv'))
        dfy = pd.read_csv(os.path.join(monPath,'probes_VelocityY.csv'))
        dfz = pd.read_csv(os.path.join(monPath,'probes_VelocityZ.csv'))
        press = pd.read_csv(os.path.join(monPath,'probes_Pressure.csv'))

        col = ['t']
        for i in range(1,97):
            col.append(i)
        dfx.columns = col
        dfy.columns = col
        dfz.columns = col
        press.columns = col
        means_x = []
        means_y = []
        means_z = []
        pressure = []
        labels = ['5','30','49','50.05','51']
        for i in range(1,6):
            (mnx,mny,mnz) = self.getMeanFromProbe(dfx,dfy,dfz,i)
            means_x.append(mnx)
            means_y.append(mny)
            means_z.append(mnz)
            pressure.append(self.getProbePressure(press,i))
        # Calculate the efficiency
        rho = 1.17862
        powerCoeff = 2.0 *(pressure[2]-pressure[4])*means_x[2]/(rho*means_x[0]**3)
        print "AxialBisectionTask.getPowerCoeff>",path,powerCoeff
        return float(powerCoeff)

    def vel(self,df,positions):
        '''
        Get's the row we are interested in the data frame.
        '''
        return df[positions][9:10]

    def getMean(self,dfx,dfy,dfz,positions):
        #return (vel(dfx,pos[0],pos[1],pos[2],pos[3])**2 + vel(dfy,pos[0],pos[1],pos[2],pos[3])**2 + vel(dfz,pos[0],pos[1],pos[2],pos[3])**2).apply(np.sqrt).mean(axis=1)[9]
        means = []
        means.append(self.vel(dfx,positions).mean(axis=1)[9])
        means.append(self.vel(dfy,positions).mean(axis=1)[9])
        means.append(self.vel(dfz,positions).mean(axis=1)[9])
        return means

    def getMeanFromProbe(self,dfx,dfy,dfz,probe):
        lst = []
        if probe==1:
            for i in range(1,25):
                lst.append(i)
            return self.getMean(dfx,dfy,dfz,lst)
        elif probe==2:
            for i in range(25,49):
                lst.append(i)
            return self.getMean(dfx,dfy,dfz,lst)
        elif probe==3:
            for i in range(49,65):
                lst.append(i)
            return self.getMean(dfx,dfy,dfz,lst)
        elif probe == 4:
            for i in range(65,81):
                lst.append(i)
            return self.getMean(dfx,dfy,dfz,lst)
        elif probe == 5:
            for i in range(81,97):
                lst.append(i)
            return self.getMean(dfx,dfy,dfz,lst)

    def getMeanPressure(self,pressure,positions):
        p = self.vel(pressure,positions).mean(axis=1)[9]
        #print "Got pressure for positions:",positions,':',p
        return p

    def getProbePressure(self,pressure,probe):
        lst = []
        if probe==1:
            for i in range(1,25):
                lst.append(i)
            return self.getMeanPressure(pressure,lst)
        elif probe==2:
            for i in range(25,49):
                lst.append(i)
            return self.getMeanPressure(pressure,lst)
        elif probe==3:
            for i in range(49,65):
                lst.append(i)
            return self.getMeanPressure(pressure,lst)
        elif probe == 4:
            for i in range(65,81):
                lst.append(i)
            return self.getMeanPressure(pressure,lst)
        elif probe == 5:
            for i in range(81,97):
                lst.append(i)
            return self.getMeanPressure(pressure,lst)




if __name__ == '__main__':
    #MainControllerTask().start()
    AxialBisectionTask(780,810).start()
    import socket
    run(host='atlacamani.marietta.edu', port=SERVER_PORT)