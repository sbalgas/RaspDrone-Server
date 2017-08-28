#!/usr/bin/env python

import threading

from quadcopter.mpu.mpu import mpu
from quadcopter.control.control import control
from quadcopter.motor.motor_control import motor_control
from quadcopter.utils.pid import pid
from quadcopter.utils.functions import map, constrain
from quadcopter.network.wifi import wifi
from time import sleep

class quadcopter():

	def __init__(self):

		kpStable = 1;
		kiStable = 0;
		kdStable = 0;
		kp = 3;
		ki = 0;
		kd = 0;
		kp_yaw = 5;
		ki_yaw = 0;
		kd_yaw = 0;

		self.motorFL_val = 0;
		self.motorFR_val = 0;
		self.motorBL_val = 0;
		self.motorBR_val = 0;

		self.wifi = wifi();
		self.control = control();
		self.motor_controller = motor_control(True); 
		
		self.pidRollStable 	= pid("pidRollStable", kpStable, kiStable, kdStable)
		self.pidPitchStable = pid("pidPitchStable", kpStable, kiStable, kdStable)
		self.pidRoll 		= pid("pidRoll", kp, ki, kd)
		self.pidPitch 		= pid("pidPitch", kp, ki, kd)
		self.pidYaw 		= pid("pidYaw", kp_yaw, ki_yaw, kd_yaw)
		
		t1 = threading.Thread(target = self.startMPU);
		t1.daemon = True;
		t1.start();

		self.wifi.setCallbackReceivedFata(self.callbackReceivedData);
		self.wifi.startSocket()
		
	def mpuUpdated(self, rollAcc, pitchAcc, yawAcc, roll, pitch, yaw):
		pidRoll		= self.pidRollStable.calc(self.control.getRoll() - rollAcc);
		pidPitch	= self.pidPitchStable.calc(self.control.getPitch() - pitchAcc);

		pidRoll 	= self.pidRoll.calc(roll - pidRoll);
		pidPitch 	= self.pidPitch.calc(pitch - pidPitch);
		pidYaw		= self.pidYaw.calc(yaw - self.control.getYaw());

		self.setControl(pidRoll, pidPitch, pidYaw);

		objectToSend = { 
			'MotorFL': self.motorFL_val,
			'MotorFR': self.motorFR_val,
			'MotorBL': self.motorBL_val,
			'MotorBR': self.motorBR_val,
			'Yaw'	 : yaw,
			'Pitch'	 : pitch,
			'Roll'	 : roll
		};

		self.wifi.sendData(objectToSend);

	def callbackReceivedData(self, axis):
		self.control.setThrottle(axis['Throttle']);
		self.control.setYaw(axis['Yaw']);
		self.control.setRoll(axis['Roll']);
		self.control.setPitch(axis['Pitch']);


	def setControl(self, roll, pitch, yaw):

		self.motorFL_val = constrain(self.control.getThrottle() - roll - pitch + yaw, 1200, 2000);
		self.motorBL_val = constrain(self.control.getThrottle() - roll + pitch - yaw, 1200, 2000);
		self.motorFR_val = constrain(self.control.getThrottle() + roll - pitch - yaw, 1200, 2000);
		self.motorBR_val = constrain(self.control.getThrottle() + roll + pitch + yaw, 1200, 2000);
		
		self.motor_controller.setW_FR(self.motorFR_val);
		self.motor_controller.setW_FL(self.motorFL_val);
		self.motor_controller.setW_BL(self.motorBL_val);
		self.motor_controller.setW_BR(self.motorBR_val);
		print "-----------------";

	def startMPU(self):
		self.mpu = mpu()
		self.mpu.setCallbackUpdate(self.mpuUpdated)
		self.mpu.run()

quadcopterInstance = quadcopter();