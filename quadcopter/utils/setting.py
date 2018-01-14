from ConfigParser import SafeConfigParser

class setting():

	def __init__(self):
		self.config = SafeConfigParser();
		self.config.read('config.ini');


	def setPIDRoll(self, p, i, d):
		self.config.add_section('PIDRoll');
		self.config.set('PIDRoll', 'P', str(p));
		self.config.set('PIDRoll', 'I', str(i));
		self.config.set('PIDRoll', 'D', str(d));
		self.save();

	def setPIDPitch(self, p, i, d):
		self.config.add_section('PIDPitch');
		self.config.set('PIDPitch', 'P', str(p));
		self.config.set('PIDPitch', 'I', str(i));
		self.config.set('PIDPitch', 'D', str(d));
		self.save();

	def setPIDYaw(self, p, i, d):
		self.config.add_section('PIDYaw');
		self.config.set('PIDYaw', 'P', str(p));
		self.config.set('PIDYaw', 'I', str(i));
		self.config.set('PIDYaw', 'D', str(d));
		self.save();

	def setGyroError(self, roll, pitch):
		#self.config.add_section('GyroError');
		self.config.set('GyroError', 'Roll', str(roll));
		self.config.set('GyroError', 'Pitch', str(pitch));
		self.save();

	def getPIDRoll(self):
		return self.config.getfloat('PIDRoll', 'P'), self.config.getfloat('PIDRoll', 'I'), self.config.getfloat('PIDRoll', 'D'), self.config.getfloat('PIDRoll', 'MaxCorrection');

	def getPIDPitch(self):
		return self.config.getfloat('PIDPitch', 'P'), self.config.getfloat('PIDPitch', 'I'), self.config.getfloat('PIDPitch', 'D'), self.config.getfloat('PIDPitch', 'MaxCorrection');

	def getPIDYaw(self):
		return self.config.getfloat('PIDYaw', 'P'), self.config.getfloat('PIDYaw', 'I'), self.config.getfloat('PIDYaw', 'D'), self.config.getfloat('PIDYaw', 'MaxCorrection');

	def getRollPitchLimitAngle(self):
		return self.config.getfloat('LimitAngle', 'RollPitch');

	def getGyroError(self):
		return self.config.getfloat('GyroError', 'Roll'), self.config.getfloat('GyroError', 'Pitch');

	def save(self):
		with open('config.ini', 'w') as f:
			self.config.write(f)

	