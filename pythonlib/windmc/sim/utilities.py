'''
Created on Mar 14, 2014

@author: vance
'''
import requests

'''
URLs at which are running meshing services
'''
meshServicesLocs = ['http://atlacamani308:3000','http://atlacamani309:3000','http://atlacamani310:3000']

'''
URLs at which are running post-processing services.
'''
postProcLocs = ['http://atlacamani305:3000','http://atlacamani306:3000','http://atlacamani307:3000']

def getActiveServices(serviceList):
    # Get the reachable nodes
    reachable = []
    for loc in serviceList:
        try:
            pollReq = requests.get(loc+'/jobs')
            print "Got job count:",pollReq.text
            reachable.append(loc)
        except:
            print "Failed to reach:",loc  
    return reachable  

def getActiveMeshServices():
    return getActiveServices(meshServicesLocs)

def getActivePostProcessingServices():
    return getActiveServices(postProcLocs)
