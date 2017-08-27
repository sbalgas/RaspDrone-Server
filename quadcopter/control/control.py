
class control(object):
	
	def __init__(self):
		self.throttle = 1000;
		self.roll = 1500;
		self.pitch = 1500;
		self.yaw = 1500;

		self.minThrottle = 1000;
		self.maxThrottle = 2000;

		self.minRoll = 1000;
		self.maxRoll = 2000;

		self.minPitch = 1000;
		self.maxPitch = 2000;

		self.minYaw = 1000;
		self.maxYaw = 2000;

		self.sensitivity = 8;
		self.deadZone = 13;

	def getThrottle(self):
		return self.throttle;

	def getRoll(self):
		roll = 0;
		if (self.throttle > 1100):
			if (self.roll > (1500+self.deadZone)):
				roll = (self.roll - (1500+self.deadZone))/self.sensitivity;
			elif (self.roll < (1500-self.deadZone)):
				roll = (self.roll - (1500-self.deadZone))/self.sensitivity;
		
		return roll;

	def getPitch(self):
		pitch = 0;
		if (self.throttle > 1100):
			if (self.pitch > (1500+self.deadZone)):
				pitch = (self.pitch - (1500+self.deadZone))/self.sensitivity;
			elif (self.pitch < (1500-self.deadZone)):
				pitch = (self.pitch - (1500-self.deadZone))/self.sensitivity;
		
		return pitch;

	def getYaw(self):
		return self.yaw;

	def setThrottle(self, qty = 1000):
		self.throttle = self.constrain(qty, self.minThrottle, self.maxThrottle);

	def setRoll(self, qty = 1500):
		self.roll = self.constrain(qty, self.minRoll, self.maxRoll);

	def setPitch(self, qty = 1500):
		self.pitch = self.constrain(qty, self.minPitch, self.maxPitch);

	def setYaw(self, qty = 1500):
		self.yaw = self.constrain(qty, self.minYaw, self.maxYaw);


	''' Limita number en minNumber y maxNumber'''
	def constrain(self, number, minNumber, maxNumber):
		return max(min(maxNumber, number), minNumber)