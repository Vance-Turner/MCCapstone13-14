'''
This runs on the cluster machines and responds to 
orders to run code-saturne
'''

from SocketServer import BaseRequestHandler, TCPServer

class EchoHandler(BaseRequestHandler):
	def handle(self):
		print("Got connection from",self.client_address)
		order = self.request.recv(8192)
		# The order should be in the format: xHeadLoss:yHeadLoss:zHeadLoss:requestID:basePath:xmlStudyName:portToSendResponse
		if not order:
			print "Failed to get data!!"
		elif not order=="PROBING":
			# now parse the message
			parts = order.split(":")
			if len(parts)==8:
				print "Just killed original request socket!"
				print "Got a good message!"
				from calculationManager import startCalc
				ipAddress = self.client_address 
				self.request.send("START_CALC")
				self.request.send("CLOSE")
				self.request.close()
				results = startCalc(parts[5],parts[6],float(parts[0]),float(parts[1]),float(parts[2]))
				from socket import socket, AF_INET, SOCK_STREAM
				sock = socket(AF_INET,SOCK_STREAM)
				print "Trying to send results to>",str(ipAddress),":",int(parts[7])
				sock.connect((str(ipAddress[0]),int(parts[7])))
				sock.send(str(results[0])+":"+str(results[1])+":"+str(parts[4]))
				sock.close()
				print "Sent CLOSE and killed response socket!"
			else:
				print "Failed to get a good message!"
		'''	
		while True:
			msg = self.request.recv(8192)
			if not msg:
				break
			self.request.send(msg)
		'''

if __name__=='__main__':
	
	ports = [20000,20001,20002,20003,20004,20005,20006,20008,20009]
	foundPort = False
	index = 0
	from socket import socket
	for i in range(20000,20080):
		try:
			serv = TCPServer(('',i),EchoHandler)
			print "Serving on:",i
			serv.serve_forever()
			foundPart = True
		except Exception:
			foundPort = False
			

