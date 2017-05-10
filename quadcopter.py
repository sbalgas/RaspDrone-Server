import threading

from quadcopter.mpu.mpu import mpu
from quadcopter.control.control import control
from quadcopter.pid import pid

class quadcopter():

	def __init__(self):

		kpStable = 0;
		kiStable = 0;
		kdStable = 0;
		kp = 3;
		ki = 0;
		kd = 0;
		kp_yaw = 0;
		ki_yaw = 0;
		kd_yaw = 0;

		self.control = control();

		self.pidRollStable 	= pid(kpStable, kiStable, kdStable)
		self.pidPitchStable = pid(kpStable, kiStable, kdStable)
		self.pidRoll 		= pid(kp, ki, kd)
		self.pidPitch 		= pid(kp, ki, kd)
		self.pidYaw 		= pid(kp_yaw, ki_yaw, kd_yaw)
		
		t2 = threading.Thread(target = self.startMPU);
		t2.daemon = True;
		t2.start();

	def mpuUpdated(self, rollAcc, pitchAcc, yawAcc, roll, pitch, yaw):

		pidRoll		= self.pidRollStable.calc(self.control.getRoll() - rollAcc);
		pidPitch	= self.pidPitchStable.calc(self.control.getPitch() - pitchAcc);

		pidRoll 	= self.pidRoll.calc(roll - pidRoll);
		pidPitch 	= self.pidPitch.calc(pitch - pidPitch);
		pidYaw		= self.pidYaw.calc(yaw - self.control.getYaw());


	def startMPU(self):
		self.mpu = mpu()
		self.mpu.setCallbackUpdate(self.mpuUpdated)
		self.mpu.run()

quadcopterInstance = quadcopter();