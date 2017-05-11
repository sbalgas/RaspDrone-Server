
class wifi():


	def __init__(self):
		self.client = None;
		self.callbackReceivedData = None;

		self.prepareSocket()
		self.loopConection()

	def setCallbackReceivedFata(self, callbackReceivedData):
		self.callbackReceivedData = callbackReceivedData;


	def prepareSocket(self, hostname = "0.0.0.0", port = 5000):
		print "Starting server"
		self.s = socket.socket()
		try:
			self.s.bind((hostname, port))
			self.s.listen(5)
			print "Server Started!!"
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
			except Exception as e:
				print "Client close: " + str(e)
				break

			if not data:
				print 'Client disconnected'
				break

			self.processJson(data)

		self.client.close()
		print "exit listen loop"


	def sendData(self, data):
		print data;
		if data is None:
			return;
		try:
			self.client.send(data+"\n");
		except Exception as e:
			print e

	def processJson(self, jSON):
		try:
			jSON = jSON.split()[0]
			axis = json.loads(jSON)
		except Exception as e:
			print "Json Error in ", jSON
			print e 
			return
			
		if self.callbackReceivedData is not None:
			self.callbackReceivedData(axis);
