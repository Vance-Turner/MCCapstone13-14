__author__ = 'vance'

import os, json
f = open('config.json')
print "Loading from windmc.config.py..."
serverType = input("What type of server are you running?:1=cluster 2=controller>")
if serverType==1:
    serverDataPath = os.path.join(os.getcwd(),'cluster')
elif serverType==2:
    serverDataPath = os.path.join(os.getcwd(),'controller')
dataMap = json.load(f)
f.close()
if raw_input("Is this the server data path?>"+serverDataPath) == 'N':
    serverDataPath = raw_input("Enter the absolute path of the server's data directory:")
    while not os.path.exists(serverDataPath):
        print "That path does not exist."
    	serverDataPath = raw_input("Enter the absolute path of the server's data directory:")

windmcPath = os.path.join(os.getcwd(),'windmc')
if raw_input("Is this the windmc path?>"+windmcPath) == 'N':
    windmcPath = raw_input("Enter the absolute path of the windmc library:")
    while not os.path.exists(windmcPath):
        print "That path does not exist."
        windmcPath = raw_input("Enter the absolute path of the windmc library:")


# String to send a cluster
JOB_TYPE_CODE_SATURNE = "code_saturne"
JOB_TYPE_CODE_SATURNE_ACT_DISK = "code_saturne_actuator_disk"

CODE_SAT_STD_CASE = 'case.xml'
CODE_SAT_STD_ACT_DISK = 'actuator_disk_case.xml'
