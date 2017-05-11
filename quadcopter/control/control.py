
class control(object):
	
	def __init__(self):
		self.throttle = 0;
		self.roll = 0;
		self.pitch = 0;
		self.yaw = 0;

		self.minThrottle = 1000;
		self.maxThrottle = 2000;
		self.sensitivityThrottle = 10;

		self.minRoll = 1000;
		self.maxRoll = 2000;
		self.sensitivityRoll = 10;

		self.minPitch = 1000;
		self.maxPitch = 2000;
		self.sensitivityPitch = 10;

		self.minYaw = 1000;
		self.maxYaw = 2000;
		self.sensitivityYaw = 10;

	def getThrottle(self):
		return self.throttle;

	def getRoll(self):
		return self.roll;

	def getPitch(self):
		return self.pitch;

	def getYaw(self):
		return self.yaw;

	def increaseThrottle(self, qty = 1):
		self.throttle = self.constrain(self.throttle + qty * self.sensitivityThrottle, self.minThrottle, self.maxThrottle);

	def decreaseThrottle(self, qty = 1):
		self.throttle = self.constrain(self.throttle - qty * self.sensitivityThrottle, self.minThrottle, self.maxThrottle);

	def increaseRoll(self, qty = 1):
		self.roll = self.constrain(self.roll + qty * self.sensitivityRoll, self.minRoll, self.maxRoll);

	def decreaseRoll(self, qty = 1):
		self.roll = self.constrain(self.roll - qty * self.sensitivityRoll, self.minRoll, self.maxRoll);

	def increasePitch(self, qty = 1):
		self.pitch = self.constrain(self.pitch + qty * self.sensitivityPitch, self.minPitch, self.maxPitch);

	def decreasePitch(self, qty = 1):
		self.pitch = self.constrain(self.pitch - qty * self.sensitivityPitch, self.minPitch, self.maxPitch);

	def increaseYaw(self, qty = 1):
		self.yaw = self.constrain(self.yaw + qty * self.sensitivityYaw, self.minYaw, self.maxYaw);

	def decreaseYaw(self, qty = 1):
		self.yaw = self.constrain(self.yaw - qty * self.sensitivityYaw, self.minYaw, self.maxYaw);


	''' Limita number en minNumber y maxNumber'''
	def constrain(self, number, minNumber, maxNumber):
		return max(min(maxNumber, number), minNumber)