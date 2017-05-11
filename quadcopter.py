import threading

from quadcopter.mpu.mpu import mpu
from quadcopter.control.control import control
from quadcopter.motor.motor_control import motor_control
from quadcopter.utils.pid import pid
from quadcopter.utils.functions import map, constrain
from time import sleep

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
		self.motor_controller = motor_control(True); 
		
		self.pidRollStable 	= pid(kpStable, kiStable, kdStable)
		self.pidPitchStable = pid(kpStable, kiStable, kdStable)
		self.pidRoll 		= pid(kp, ki, kd)
		self.pidPitch 		= pid(kp, ki, kd)
		self.pidYaw 		= pid(kp_yaw, ki_yaw, kd_yaw)
		
		t2 = threading.Thread(target = self.startMPU);
		t2.daemon = True;
		t2.start();
		while True:
			sleep(1);
			self.control.increaseThrottle();

	def mpuUpdated(self, rollAcc, pitchAcc, yawAcc, roll, pitch, yaw):
		pidRoll		= self.pidRollStable.calc(self.control.getRoll() - rollAcc);
		pidPitch	= self.pidPitchStable.calc(self.control.getPitch() - pitchAcc);

		pidRoll 	= self.pidRoll.calc(roll - pidRoll);
		pidPitch 	= self.pidPitch.calc(pitch - pidPitch);
		pidYaw		= self.pidYaw.calc(yaw - self.control.getYaw());

		self.setControl(pidRoll, pidPitch, pidYaw);

	def setControl(self, roll, pitch, yaw):
		motorFL_val = map(constrain(self.control.getThrottle() - (roll/2) - (pitch/2) + yaw, 1000, 2000), 1000, 2000, 0, 100)
		motorBL_val = map(constrain(self.control.getThrottle() - (roll/2) + (pitch/2) - yaw, 1000, 2000), 1000, 2000, 0, 100)
		motorFR_val = map(constrain(self.control.getThrottle() + (roll/2) - (pitch/2) - yaw, 1000, 2000), 1000, 2000, 0, 100)
		motorBR_val = map(constrain(self.control.getThrottle() + (roll/2) + (pitch/2) + yaw, 1000, 2000), 1000, 2000, 0, 100)
		
		self.motor_controller.setW_FR(motorFR_val);
		self.motor_controller.setW_FL(motorFL_val);
		self.motor_controller.setW_BL(motorBL_val);
		self.motor_controller.setW_BR(motorBR_val);

	def startMPU(self):
		self.mpu = mpu()
		self.mpu.setCallbackUpdate(self.mpuUpdated)
		self.mpu.run()

quadcopterInstance = quadcopter();