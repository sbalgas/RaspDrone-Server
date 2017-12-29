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
		kp = 5;
		ki = 0.5;
		kd = 2	;
		kp_yaw = 5;
		ki_yaw = 0.5;
		kd_yaw = 2;

		self.RollPitchLimitAngle = 35;

		self.motorFL_val = 0;
		self.motorFR_val = 0;
		self.motorBL_val = 0;
		self.motorBR_val = 0;

		self.wifi = wifi();
		self.control = control();
		self.motor_controller = motor_control(); 
		
		self.pidRollStable 	= pid("pidRollStable", kpStable, kiStable, kdStable)
		self.pidPitchStable = pid("pidPitchStable", kpStable, kiStable, kdStable)
		self.pidRoll 		= pid("pidRoll", kp, ki, kd, 30)
		self.pidPitch 		= pid("pidPitch", kp, ki, kd, 30)
		self.pidYaw 		= pid("pidYaw", kp_yaw, ki_yaw, kd_yaw, 30)
		
		t1 = threading.Thread(target = self.startMPU);
		t1.daemon = True;
		t1.start();

		self.wifi.setCallbackReceivedFata(self.callbackReceivedData);
		self.wifi.startSocket()
		
	def mpuUpdated(self, rollAcc, pitchAcc, yawAcc, roll, pitch, yaw):

		#pidRoll	= self.pidRollStable.calc(self.control.getRoll() - rollAcc);
		#pidPitch	= self.pidPitchStable.calc(self.control.getPitch() - pitchAcc);

		errorRoll = constrain(roll - self.control.getRoll(), self.RollPitchLimitAngle*-1, self.RollPitchLimitAngle);
		errorPith = constrain(pitch - self.control.getPitch(), self.RollPitchLimitAngle*-1, self.RollPitchLimitAngle);


		pidRoll		= self.pidRoll.calc(errorRoll);
		pidPitch	= self.pidPitch.calc(errorPith);
		pidYaw		= self.pidYaw.calc(yaw - self.control.getYaw());

		objectToSend = { 
			'MotorFL'		: int(self.motorFL_val),
			'MotorFR'		: int(self.motorFR_val),
			'MotorBL'		: int(self.motorBL_val),
			'MotorBR'		: int(self.motorBR_val),
			'Yaw'			: int(yaw),
			'Pitch'			: int(pitch),
			'Roll'			: int(roll),
			'PidRollError'	: float(self.control.getRoll()),
			'PidPitchError'	: float(self.control.getPitch()),
			'PidYawError'	: float(self.control.getYaw())
		};

		self.wifi.sendData(objectToSend);

		if self.motor_controller.isPowered():
			self.setControl(pidRoll, pidPitch, pidYaw);

	def callbackReceivedData(self, data):
		if (data['PIDMode'] > 0):
			print data['PIDMode'];
			if (data['PIDMode'] == 11 or data['PIDMode'] == 12): # P
				self.pidRoll.setKp(data['PIDValue']);
			#if (data['PIDMode'] == 12 ): 
				self.pidPitch.setKp(data['PIDValue']);
			if (data['PIDMode'] == 13 ): 
				self.pidYaw.setKp(data['PIDValue']);

			if (data['PIDMode'] == 21 or data['PIDMode'] == 22): # I
				self.pidRoll.setKi(data['PIDValue']);
			#if (data['PIDMode'] == 22 ): 
				self.pidPitch.setKi(data['PIDValue']);
			if (data['PIDMode'] == 23 ): 
				self.pidYaw.setKi(data['PIDValue']);

			if (data['PIDMode'] == 31 or data['PIDMode'] == 32): # D
				self.pidRoll.setKd(data['PIDValue']);
			#if (data['PIDMode'] == 32 ): 
				self.pidPitch.setKd(data['PIDValue']);
			if (data['PIDMode'] == 33 ): 
				self.pidYaw.setKd(data['PIDValue']);

			return;

		if self.motor_controller.isPowered():
			self.control.setThrottle(data['Throttle']);
			self.control.setYaw(data['Yaw']);
			self.control.setRoll(data['Roll']);
			self.control.setPitch(data['Pitch']);
			if data['Throttle'] < 1050 and data['Yaw'] > 1950:
				self.motor_controller.stop();	
		elif data['Throttle'] < 1050 and data['Yaw'] < 1050:
			self.motor_controller.start();


	def setControl(self, roll, pitch, yaw):
		self.motorFL_val = constrain(self.control.getThrottle() - roll - pitch + yaw, 1200, 2000);
		self.motorBL_val = constrain(self.control.getThrottle() - roll + pitch - yaw, 1200, 2000);
		self.motorFR_val = constrain(self.control.getThrottle() + roll - pitch - yaw, 1200, 2000);
		self.motorBR_val = constrain(self.control.getThrottle() + roll + pitch + yaw, 1200, 2000);

		self.motor_controller.setW_FL(self.motorFL_val);
		self.motor_controller.setW_FR(self.motorFR_val);
		self.motor_controller.setW_BL(self.motorBL_val);
		self.motor_controller.setW_BR(self.motorBR_val);

	def startMPU(self):
		self.mpu = mpu()
		self.mpu.setCallbackUpdate(self.mpuUpdated)
		self.mpu.run()

quadcopterInstance = quadcopter();
