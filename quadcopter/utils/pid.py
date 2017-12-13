from time import time,sleep

class pid():

	def __init__(self,name,kp,ki,kd,maxCorr=5):
		self.kp = kp
		self.ki = ki
		self.kd = kd
		self.P =0
		self.I = 0
		self.D = 0
		self.previousTime = 0.0
		self.previousError = 0.0
		self.init=True
		self.name=name
		self.maxCorr=maxCorr

	def getName(self):
		return self.name;

	def getPid(self):
		return {'P' : self.P, 'I' : self.I, 'D' : self.D};

	def calc(self, error):
		if self.init:
			self.previousTime = time()
			self.init=False
			print "Initializing ", self.name;
			return 0
		else:
			currentTime = time()
			stepTime = currentTime - self.previousTime

			self.P = error * self.kp
			self.I += (error * stepTime) * self.ki
			self.D = (error - self.previousError) / stepTime * self.kd


			correction = self.P + self.I + self.D
			self.previousTime = currentTime
			self.previousError = error
			#since W is an integer, correction is rounded
			correction = round(correction)

			if correction>self.maxCorr:
				correction=self.maxCorr
			if correction<-self.maxCorr:
				correction=-self.maxCorr
			return correction
