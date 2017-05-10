


class motor(object):
    """Manages the currect Angular rotation
    Implements the IO interface using the RPIO lib
    __init_(self, name, pin, kv=1000, RPMMin=1, RPMMax=100, debug=True, simulation=True):
    More info on RPIO in http://pythonhosted.org/RPIO/index.html"""


    def __init__(self, name, pin, WMin=0, WMax=100, debug=True, simulation=True):
        self.name = name
        self.powered = False
        self.simulation = simulation
        self.__pin = pin
        self.setWLimits(WMin, WMax)
        self.setDebug(debug)

        self.__W = self.__WMin
        self.__Wh = 10

        try:
            from RPIO import PWM
            self.__IO = PWM.Servo()
        except ImportError:
            print("ERROR");
            self.simulation = True

    def setDebug(self, debug):
        self.__debug = debug

    def getDebug(self):
        return self.__debug

    def setWLimits(self, WMin, WMax):
        "set the pin for each motor"
        if WMin < 0:
            WMin = 0
        self.__WMin = WMin
        if WMax > 100:
            WMax = 100
        self.__WMax = WMax

    def start(self):
        "Run the procedure to init the PWM"
        if not self.simulation:
            try:
                from RPIO import PWM
                self.__IO = PWM.Servo()
                self.powered = True
                print "Motor ", self.name, " Started";
                self.setW(0)
            except ImportError:
                self.simulation = True
                self.powered = False

    def stop(self):
        "Stop PWM signal"

        self.setW(0)
        if self.powered:
            self.__IO.stop_servo(self.__pin)
            self.powered = False

    def increaseW(self, step=1):
        "increases W% for the motor"

        self.__W = self.__W + step
        self.setW(self.__W)

    def decreaseW(self, step=1):
        "decreases W% for the motor"

        self.__W = self.__W - step
        self.setW(self.__W)

    def setW(self, W):
        "Checks W% is between limits than sets it"

        PW = 0
        self.__W = W
        if self.__W < self.__WMin:
            self.__W = self.__WMin
        if self.__W > self.__WMax:
            self.__W = self.__WMax
        PW = (1000 + (self.__W) * 10)
        # Set servo to xxx us
        print "PW: ", PW;
        if self.powered:
            self.__IO.set_servo(self.__pin, PW)




