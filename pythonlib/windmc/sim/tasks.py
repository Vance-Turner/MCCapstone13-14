__author__ = 'vance'

from threading import Thread
from bottle import route, static_file, HTTPError, run, request,post,get
from ..config import serverDataPath,windmcPath
import os
import time
import json
from windmc.sim.clusters.clustermanager import CONTROLLER_IP, CONTROLLER_PORT
import tempfile, csv

"""
Holds results of code-saturne jobs. The key is the job id and the value is the energy extracted.
"""
jobResults = {}
energyResults = {}
jobMap = {}

@route('/files/mesh/<meshfilename>')
def getMeshFile(meshfilename):
    print 'Got request for mesh file...'
    meshPath = os.path.join(serverDataPath,'code_saturne','mesh',meshfilename)
    if os.path.exists(meshPath):
        return static_file(meshfilename,os.path.join(serverDataPath,'code_saturne','mesh'),download=True)
    else:
        return HTTPError()

@post('/results/<jobid>')
def doResultsPost(jobid):
    print "Got results for:",jobid
    reMap = json.loads(request.forms.get('RESULTS_DATA'))
    inVel = reMap["inlet"]
    outVel = reMap["outlet"]
    powerExtracted = ((outVel**3)-(inVel**3))/(inVel**3)
    jobResults[jobid]=powerExtracted
    energyResults[jobMap[jobid]]=powerExtracted
    print "Stored for",jobid,jobResults[jobid]

@route('/currentResults')
def getCurrentResults():
    keys = energyResults.keys()
    keys.sort()
    ff = open(os.path.join(serverDataPath,'currentResults.csv'),'w')
    csvWriter = csv.writer(ff,delimiter=',')
    for key in keys:
        csvWriter.writerow([key,energyResults[key]])
    ff.close()
    return static_file('currentResults.csv',serverDataPath,download=True)

class AxialInductionTask(Thread):

    def __init__(self,lowerHeadLoss,upperHeadLoss,taskId):
        Thread.__init__(self)
        self._lowerHeadLoss = lowerHeadLoss
        self._upperHeadLoss = upperHeadLoss
        self._taskId = taskId

    def run(self):
        self.doSim(self._lowerHeadLoss)

    def doSim(self,headLoss):
        from clusters import clustermanager
        manager = clustermanager.ClusterManager()
        study = self._taskId
        case = self._taskId+"_CASE"+str(time.time())
        processorModule = "axialInductionFactor"
        meshMethod = "DOWNLOAD"
        meshCode = "actuator_disk_tunnel_hd.med"
        headLossXX = headLoss
        headLossYY = 0
        headLossZZ = 0
        # We don't actually use these shroud things...
        shroudInX = 37.5
        shroudInY = 0
        shroudInZ = 0
        shroudOutX = 37.5+25
        shroudOutY = 0
        shroudOutZ = 0
        jobId = str(self._taskId)
        jobMap[jobId] = headLoss
        manager.putCodeSaturneOrder(study,case,processorModule,meshMethod,meshCode,\
                                    headLossXX,headLossYY,headLossZZ,\
                                    shroudInX,shroudInY,shroudInZ,\
                                    shroudOutX,shroudOutY,shroudOutZ,jobId,True)


class MainControllerTask(Thread):

    def run(self):
        for i in xrange(0,40):
            task = AxialInductionTask(float(i)/10.0,1,'task_'+str(float(i)/10.0))
            task.start()


if __name__ == '__main__':
    MainControllerTask().start()
    run(host=CONTROLLER_IP, port=CONTROLLER_PORT, debug=True)