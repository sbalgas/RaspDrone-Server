
#from motor_rpio import motor
from motor_pigpio import motor
from time import sleep

class motor_control():
	
	def __init__(self, start = False, debug = False):
		self.motorBL = motor('motorBL', 18, simulation=False); 
		self.motorBR = motor('motorBR', 13, simulation=False); # horario ok
		self.motorFR = motor('motorFR', 12, simulation=False); 
		self.motorFL = motor('motorFL', 19, simulation=False); # horario ok

		self.powered = False;

		if (start):
			self.start();

	def isPowered(self):
		return self.powered;

	def start(self):
		print("Start motors");
		self.motorFR.start();
		self.motorFL.start();
		self.motorBL.start();
		self.motorBR.start();
		print "*** Wait 5"
		sleep(1);
		print "*** Wait 4"
		sleep(1);
		print "*** Wait 3"
		sleep(1);
		print "*** Wait 2"
		sleep(1);
		print "*** Wait 1"
		sleep(1);
		self.powered = True;

	def stop(self):
		print("Stop motors");
		self.powered = False;
		self.motorFR.stop();
		self.motorFL.stop();
		self.motorBR.stop();
		self.motorBL.stop();

	def setW_FR (self, w):
		#print "motorFR: ", int(w); 
		self.motorFR.setW(int(w));

	def setW_FL (self, w):
		#print "motorFL: ", int(w); 
		self.motorFL.setW(int(w));

	def setW_BR (self, w):
		#print "motorBR: ", int(w);
		self.motorBR.setW(int(w));

	def setW_BL (self, w):
		#print "motorBL: ", int(w); 
		self.motorBL.setW(int(w));