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

	def getPIDRoll(self):
		return config.getfloat('PIDRoll', 'P'), config.getfloat('PIDRoll', 'I'), config.getfloat('PIDRoll', 'D');

	def getPIDPitch(self):
		return config.getfloat('PIDPitch', 'P'), config.getfloat('PIDPitch', 'I'), config.getfloat('PIDPitch', 'D');

	def getPIDYaw(self):
		return config.getfloat('PIDYaw', 'P'), config.getfloat('PIDYaw', 'I'), config.getfloat('PIDYaw', 'D');

	def getRollPitchLimitAngle(self):
		return config.getfloat('LimitAngle', 'RollPitch');


	def save(self):
		with open('config.ini', 'w') as f:
			self.config.write(f)

	