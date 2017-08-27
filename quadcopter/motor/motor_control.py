
from motor import motor

class motor_control():
	
	def __init__(self, start = False, debug = False):
		self.motorFR = motor('motorFR', 18, simulation=False);
		self.motorFL = motor('motorFL', 24, simulation=False);
		self.motorBL = motor('motorBL', 17, simulation=False);
		self.motorBR = motor('motorBR', 7, simulation=False);

		if (start):
			self.start();

	def start(self):
		print("Start motors");
		self.motorFR.start();
		self.motorFL.start();
		self.motorBL.start();
		self.motorBR.start();

	def stop(self):
		self.motorFR.stop();
		self.motorFL.stop();
		self.motorBL.stop();
		self.motorBR.stop();

	def setW_FR (self, w):
		print "motorFR: ", int(w); 
		self.motorFR.setW(int(w));

	def setW_FL (self, w):
		print "motorFL: ", int(w); 
		self.motorFL.setW(int(w));

	def setW_BR (self, w):
		print "motorBR: ", int(w);
		self.motorBR.setW(int(w));

	def setW_BL (self, w):
		print "motorBL: ", int(w); 
		self.motorBL.setW(int(w));
