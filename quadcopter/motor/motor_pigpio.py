
class motor(object):

	def __init__(self, name, pin, WMin=1000, WMax=2000, debug=True, simulation=True):
		self.name = name
		self.powered = False
		self.simulation = simulation
		self.__pin = pin
		self.setWLimits(WMin, WMax)
		self.setDebug(debug)

		self.__W = self.__WMin

	def setDebug(self, debug):
		self.__debug = debug

	def getDebug(self):
		return self.__debug

	def setWLimits(self, WMin, WMax):
		"set the pin for each motor"
		if WMin < 1000:
			WMin = 1000
		self.__WMin = WMin
		if WMax > 2000:
			WMax = 2000
		self.__WMax = WMax

	def start(self):
		"Run the procedure to init the PWM"
		if not self.simulation:
			try:
				import pigpio

				#GPIO.setmode(GPIO.BCM)
				
				self.__IO = pigpio.pi()
				self.powered = True
				print "Motor ", self.name, " Started";
				self.setW(1000)
			except ImportError:
				print "MOTOR ERROR ", self.name;
				self.simulation = True
				self.powered = False

		if self.simulation:
			print "SIMULATION MODE FOR ", self.name

	def stop(self):
		"Stop PWM signal"

		self.setW(1000)
		if self.powered:
			self.__IO.stop()
			self.powered = False

	def increaseW(self, step=1):
		"increases W% for the motor"

		self.setW(self.__W + int(step))

	def decreaseW(self, step=1):
		"decreases W% for the motor"
		
		self.setW(self.__W - int(step))

	def setW(self, W):
		"Checks W% is between limits than sets it"

		W = int(round(float(W) / 10)) * 10
		if W < self.__WMin:
			W = self.__WMin
		if W > self.__WMax:
			W = self.__WMax

		#print self.name, self.__W;
		if (W != self.__W and self.powered):
			self.__W = W;
			self.__IO.set_servo_pulsewidth(self.__pin, self.__W)

