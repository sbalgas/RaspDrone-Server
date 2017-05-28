import socket
import threading
import json

class wifi():


	def __init__(self):
		self.client = None;
		self.callbackReceivedData = None;

	def setCallbackReceivedFata(self, callbackReceivedData):
		self.callbackReceivedData = callbackReceivedData;


	def startSocket(self, hostname = "0.0.0.0", port = 5000):
		print "Starting server"
		self.s = socket.socket()
		try:
			self.s.bind((hostname, port))
			self.s.listen(5)
			print "Server Started!!"
			self.loopConection()
		except Exception as e:
			print "Fail Server"
			print e
			self.s = None

	def loopConection(self):
		if not self.s:
			return

		while True:
			print "wait for connection"
			self.client, address = self.s.accept()
			print 'Got connection from', address

			t = threading.Thread(target = self.listenToClient);
			t.daemon = True;
			t.start();

	def listenToClient(self):
		while True:
			try:
				data = self.client.recv(1024)
				#print data
			except Exception as e:
				print "Client close: " + str(e)
				break

			if not data:
				print 'Client disconnected'
				break

			self.processJson(data)

		self.client.close()
		self.client = None;
		print "exit listen loop"


	def sendData(self, data):
		if not self.client:
			return
		data = json.dumps(data);
		#print data;
		if data is None:
			return;
		try:
			self.client.send(data);
		except Exception as e:
			print e

	def processJson(self, jSON):
		try:
			axis = json.loads(jSON)
		except Exception as e:
			print "Json Error in ", jSON
			print e 
			return
			
		if self.callbackReceivedData is not None:
			self.callbackReceivedData(axis);
