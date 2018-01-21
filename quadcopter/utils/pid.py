from time import time

class pid():

	def __init__(self,name,kp,ki,kd,maxCorr=5):
		self.kp = kp
		self.ki = ki
		self.kd = kd
		self.P = 0
		self.I = 0
		self.D = 0
		self.previousTime = 0.0
		self.previousError = 0.0
		self.init=True
		self.name=name
		self.maxCorr=maxCorr

	def getName(self):
		return self.name;

	def getPID(self):
		return {'P' : self.P, 'I' : self.I, 'D' : self.D};

	def getKPID(self):
		return {'P' : self.kp, 'I' : self.ki, 'D' : self.kd};

	def setKp(self, kp):
		self.kp = kp;

	def setKi(self, ki):
		self.ki = ki;

	def setKd(self, kd):
		self.kd = kd;

	def getKp(self):
		return self.kp;

	def getKi(self):
		return self.ki;

	def getKd(self):
		return self.kd;

	def calc(self, error):
		if self.init:
			self.reset();
			self.init=False
			print "Initializing ", self.name;
			return 0
		else:
			currentTime = time()
			stepTime = currentTime - self.previousTime

			self.P = error * self.kp
			self.I += (error * stepTime) * self.ki
			self.D = (error - self.previousError) / stepTime * self.kd

			self.correction = self.P + self.I + self.D
			self.previousTime = currentTime
			self.previousError = error

			if self.correction>self.maxCorr:
				self.correction=self.maxCorr
			if self.correction<-self.maxCorr:
				self.correction=-self.maxCorr
			return round(self.correction)

	def reset(self):
		self.P = 0
		self.I = 0
		self.D = 0
		self.previousTime = time()
