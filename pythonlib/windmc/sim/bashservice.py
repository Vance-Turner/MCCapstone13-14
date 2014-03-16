'''
Created on Mar 14, 2014

@author: vance
@summary: This module provides a server to which bash jobs can be submitted to be run on 
the machine on which this module is running. The complete path of the bash script must
be submitted to the service for the job to be run.

It assumes the jobs will use the salome-meca platform and cleans up salome meca a certain
number of jobs.
'''

from threading import Thread, Lock
from Queue import Queue
import os, subprocess, time, json
from bottle import run, get, post, request
from multiprocessing import Process

# The Queue of bash jobs we need to make, simply holds the path of bash files to execute
jobQueue = Queue(300)

# lock to hold bash task queues
theLock = Lock()

# How often should we clean up after salome?
cleanUpRate = 10

# How long should we wait for a bash job comes in before starting the group up
pollTime = 10

# What is the max number of bash jobs to run at a given time.
bashGroupSize = 9

# How long to wait sleep between starting a process
startUpDelay = 15


def runBashTask(bashFilePath):
    if os.path.exists(bashFilePath):
        print "About to run task:",bashFilePath
        subprocess.call([bashFilePath])
    else:
        print "A task failed! This path does not exit>",bashFilePath

class BashService(Thread):
 
    def __init__(self):
        Thread.__init__(self)
        print "Creating a new bash Service!"
        self.alive=True
        self.counter = 0
 
    def run(self):
        print "Bash Service...running"
        while(self.alive):
            print "bash Service, checking the task queue..."
            if not jobQueue.empty():
                postProcJobs = []
                print "Getting jobs from queue..."
                for i in range(bashGroupSize):
                    print "Waiting to get job:",i
                    try:
                        postProcJobs.append(jobQueue.get(True, pollTime))
                    except:
                        pass
                print "Got jobs:",len(postProcJobs)
                processes = []
                for job in postProcJobs:
                    process = Process(target=runBashTask, args=(job,))
                    processes.append(process)
                    process.start()
                    time.sleep(startUpDelay)
                # Wait until all are done
                for process in processes:
                    if process.is_alive():
                        process.join()
                        
                print "All done, now killing salome..."
                subprocess.call(['/home/vance/killAllSalome.sh'])
                print 'Killed salome!'
            else:
                print "bash Service...sleeping"
                time.sleep(3)
        print "bash Service...exiting"
         
    def kill(self):
        self.alive = False 

       
@post('/jobrequest/')
def postBashJob():
    bashScriptPath = request.forms.get("bashScriptPath")
    print "bashservice, got a jobs>",bashScriptPath
    with theLock:
        print "Acquired the lock!"
        jobQueue.put(bashScriptPath)
    return "Job submitted!"

@get('/info')
def getInfo():
    return "You have reached the bash service!"

@get('/jobs')
def getJobCount():
    with theLock:
        count = jobQueue.qsize()
    print "Got the job count?>",count
    return str(count) 

@get('/killSalome')
def killSalome():
    subprocess.call(['/home/vance/killAllSalome.sh'])
    return "Killed salome"

if __name__=="__main__":
    node = input("Enter node number:")
    thePort = input("Enter port:")
    bashService = BashService()
    bashService.start()
    run(host='atlacamani'+str(node), port=thePort)
