from SocketServer import TCPServer
from SocketServer import BaseRequestHandler
from threading import Thread
import time
from socket import socket, AF_INET, SOCK_STREAM
import xml.etree.ElementTree as ET

headLossManagerMain = None

class ResponseHandler(BaseRequestHandler):

	def handle(self):
		global headLossManagerMain
		print "Got a response from a cluster?"
		response = self.request.recv(8192)
		parts = response.split(":")
		if len(parts)==3:
			print "Got a good response>",parts
			headLossManagerMain.responses[parts[2]]=[float(parts[0]),float(parts[1])]
			print "Trying to remove requestid:",parts[2]," from ",headLossManagerMain.pendingRequests
			try:
				headLossManagerMain.pendingRequests.remove(parts[2])
				print "Pending requests is now>",headLossManagerMain.pendingRequests
				print "Just stored for:",parts[2],">",headLossManagerMain.responses[parts[2]]
			except Exception:
				print "Some error..."
		else:
			print "Got a bad response!>",parts
		print "Stored response from cluster"

class HeadLossManager:

	def __init__(self):
		self.xmlTree = ET.parse("config.xml")
		self.xmlRoot = self.xmlTree.getroot()
		self.clusterCount = self.xmlRoot[0].attrib["count"]
		self.xmlClusters = self.xmlRoot[0]
		self.clusters = []
		for i in range(int(self.clusterCount)):
			cluster = {}
			xmlCluster = self.xmlClusters[i]
			attrs = self.xmlClusters[i].attrib
			cluster["id"]=attrs["id"]
			cluster["ip"]=attrs["ip"]
			cluster["port"]=int(attrs["port"])
			cluster["basepath"]=xmlCluster[0].text
			cluster["studyname"]=xmlCluster[1].text
			self.clusters.append(cluster)
		print "Processed xml>",self.clusters
		self.port = int(self.xmlRoot[1].attrib["port"])
		self.startFresh = True
		self.responses = {}
		self.pendingRequests = []
		self.startingFresh = True
		self.foundPort = False
	
	def findCluster(self):
		i = 0
		foundCluster = False
		while not foundCluster:
			sock = socket(AF_INET,SOCK_STREAM)
			try:
				print "Trying to reach cluster:",self.clusters[i]
				sock.connect((self.clusters[i]["ip"],self.clusters[i]["port"]))
				sock.send("PROBING")
				sock.close()
				foundCluster = True
				return self.clusters[i]
			except Exception:
				print self.clusters
				print "Failed to connect to:",str(i),self.clusters[i]
			i+=1
			if i==len(self.clusters):
				break
		return None

	def foundServerPort(self,port):
		self.foundPort = True	
		self.port =port

	class SimpleServer:
	
		def __init__(self,port,headLossMan):
			self.port = port
			self.headLossMan = headLossMan

		def __call__(self):
			foundPort = False
			while not foundPort:
				try:
					self.server = TCPServer(('', self.port), ResponseHandler)
					self.headLossMan.foundServerPort(self.port)
					print "Got a port to respond on!>",self.port
					self.server.serve_forever()
					break
				except Exception:
					print "Failed to get open port to respond>",self.port
					self.port+=1
	'''
	Manages the headlossmanager
	'''
	def __call__(self):
		self.simpServ = HeadLossManager.SimpleServer(self.port,self)
		th2 = Thread(target=self.simpServ)
		th2.start()
		print "Waiting to find a port..."
		while not self.foundPort:
			print "Sleep...",self.foundPort
			time.sleep(1)
		print "Apparently found a port."
		alive = True
		print "Now starting run of HeadLossManager..."
		if self.startingFresh == True:
			self.generateOrder(0.66,0.66,0.66,60)
			self.generateOrder(0.33,0.33,0.33,60)
			self.generateOrder(0.11,0.11,0.11,60)
			print "sent order!"
		counter = 20
		i = 0
		while len(self.pendingRequests)>0:
			time.sleep(0.5)
		print "ALL DONE, DATA IS>",self.responses
		self.simpServ.server.shutdown()
		#for(pendingRequests		

	def generateOrder(self,xHL,yHL,zHL,timeSteps):
		cluster = self.findCluster()
		if cluster == None:
			print "Could not find a cluster!!"
		else:
			basePath = cluster["basepath"]
			xmlStudyName = cluster["studyname"]
			reqId = time.time()
			self.pendingRequests.append(str(reqId))
			order = str(xHL)+":"+str(yHL)+":"+str(zHL)+":"+str(timeSteps)+":"+str(reqId)+":"+basePath+":"+xmlStudyName+":"+str(self.port)
			sock = socket(AF_INET,SOCK_STREAM)
			cluster = self.findCluster()
			sock.connect((cluster["ip"],cluster["port"]))
			print "Sending order:",order
			sock.send(order)
			msg = sock.recv(8192)
			print msg
			sock.close()

if __name__ == '__main__':
	import sys
	headLossMan = HeadLossManager()
	headLossManagerMain = headLossMan
	th = Thread(target=headLossMan)
	th.start()

