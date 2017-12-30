import socket
import threading
import json
#import asyncio

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

	#@asyncio.coroutine
	def sendData(self, data):
		if self.client is None:
			return

		data = json.dumps(data);
		if data is None:
			return
		try:
			self.client.send(data + "\0");
		except Exception as e:
			print e
		return
		
	def processJson(self, jSON):

		jSON = jSON.replace("}{", "}-{");

		for onejSON in jSON.split("-"):
			try:
				data = json.loads(onejSON);
			except Exception as e:
				print "original JSON ", jSON;
				print "Json Error in ", onejSON;
				print e;
				continue;
				
			if self.callbackReceivedData is not None:
				self.callbackReceivedData(data);
