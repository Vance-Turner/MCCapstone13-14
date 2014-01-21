__author__ = 'vance'

import xml.etree.ElementTree as ET
import requests
import csv
from bottle import get, post, request
from windmc.config import serverDataPath,windmcPath,JOB_TYPE_CODE_SATURNE, JOB_TYPE_CODE_SATURNE_ACT_DISK
import json, os

import json
# Load the config from the json file.
print "Loading config data for cluster from:",os.path.join(serverDataPath,'config.json')
f = open(os.path.join(serverDataPath,'config.json'),'r')
config = json.load(f)
f.close()
CONTROLLER_IP = config['ip']
CONTROLLER_PORT = config['port']

class ClusterManager:

    ORDER_TYPE_INFO = 1990
    ORDER_TYPE_JOB = 1991

    STATUS_BUSY = "BUSY"
    STATUS_READY = "READY"
    STATUS_ERROR = "ERROR"

    def __init__(self):
        self.loadClusterDefs()

    def loadClusterDefs(self):
        print "Loading cluster definitions from xml..."
        import os
        print "Local path>",windmcPath
        self.clusterDefTree = ET.parse(os.path.join(windmcPath,'sim','clusters',"clusters.xml"))
        self.clusterDefTreeRoot = self.clusterDefTree.getroot()

        self._clustersMap = {}
        self._clusters = []
        for cluster in self.clusterDefTreeRoot:
            attrs = cluster.attrib
            # See clusters.xml for what is in each child cluster definition
            newCluster = Cluster(attrs["ip"],attrs["port"],attrs["id"],attrs["sat_ver"],attrs["corecount"])
            self._clustersMap[newCluster.ip]=newCluster
            self._clustersMap[newCluster.id]=newCluster
            self._clusters.append(newCluster)
        print "Loaded clusters>",str(self._clusters[0])

    def putCodeSaturneOrder(self,study,case,processorModule, meshMethod,meshCode,\
                            headLossXX,headLossYY,headLossZZ,\
                            shroudInX, shroudInY, shroudInZ, \
                            shroudOutX, shroudOutY, shroudOutZ, jobID,\
                            doAxialJob = False
                            ):
        # Do processing first, put together the form data that will be sent
        cluster = self.__findCluster__();
        jobData = {}
        jobData['respIP']=CONTROLLER_IP
        jobData['respPort']=CONTROLLER_PORT
        jobData['processorModule']=processorModule
        jobData['jobID']=jobID
        jobData['STUDY']=study
        jobData['CASE']=case
        jobData['MESH_CREATE']=meshMethod
        jobData['MESH_CODE']=meshCode
        jobData['HLXX']=headLossXX
        jobData['HLYY']=headLossYY
        jobData['HLZZ']=headLossZZ
        jobData['SHROUD_IN_X']=shroudInX
        jobData['SHROUD_IN_Y']=shroudInY
        jobData['SHROUD_IN_Z']=shroudInZ
        jobData['SHROUD_OUT_X']=shroudOutX
        jobData['SHROUD_OUT_Y']=shroudOutY
        jobData['SHROUD_OUT_Z']=shroudOutZ
        if doAxialJob:
            jobData['JOB_TYPE']=JOB_TYPE_CODE_SATURNE_ACT_DISK
        else:
            jobData['JOB_TYPE']=JOB_TYPE_CODE_SATURNE
        aMap = {'JOB_DATA':json.dumps(jobData)}
        resp = requests.post("http://"+cluster.ip+":"+cluster.port+"/job/"+jobID,data=aMap)

    def getInfo(self,ip,port):
        #print "Getting info from:" + 'http://'+str(ip)+':'+str(port)+'/info'
        req = requests.get('http://'+str(ip)+':'+str(port)+'/info')
        #print "Got back response:",req,req.text
        infoMap = json.loads(req.text)
        #print "Parsed info map and got:",infoMap
        return infoMap

    def getInfoByID(self,id):
        cluster = self._clustersMap[id]
        return self.getInfo(cluster.ip,cluster.port)

    def __findCluster__(self):
        for cluster in self._clusters:
            req = requests.get('http://'+cluster.ip+":"+cluster.port+"/info")
            infoMap = json.loads(req.text)
            if infoMap['STATUS']=='READY':
                print "Found ready cluster:",cluster
                break
        return cluster


class Cluster:

    def __init__(self,ip,port,id,sat_ver,cores):
        self._ip = ip
        self._sat_ver = sat_ver
        self._id = id
        self._cores = cores
        self._port = port

    def __str__(self):
        return "Cluster:"+str(self._ip)+","+str(self._id)+","+str(self._port)

    @property
    def ip(self):
        return self._ip

    @property
    def sat_ver(self):
        return self._sat_ver

    @property
    def id(self):
        return self._id

    @property
    def cores(self):
        return self._cores

    @property
    def port(self):
        return self._port