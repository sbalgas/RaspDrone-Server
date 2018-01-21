#!/usr/bin/env python

import threading

from quadcopter.mpu.mpu import mpu
from quadcopter.control.control import control
from quadcopter.motor.motor_control import motor_control
from quadcopter.utils.pid import pid
from quadcopter.utils.functions import map, constrain
from quadcopter.utils.setting import setting
from quadcopter.network.wifi import wifi
from time import sleep

class quadcopter():

	def __init__(self):

		kpStable = 1;
		kiStable = 0;
		kdStable = 0;

		self.motorFL_val = 0;
		self.motorFR_val = 0;
		self.motorBL_val = 0;
		self.motorBR_val = 0;

		self.wifi = wifi();
		self.control = control();
		self.motor_controller = motor_control(); 
		
		self.pidRollStable 	= pid("pidRollStable", kpStable, kiStable, kdStable)
		self.pidPitchStable = pid("pidPitchStable", kpStable, kiStable, kdStable)

		conf = setting();

		self.RollPitchLimitAngle = conf.getRollPitchLimitAngle();

		kpRoll, kiRoll, kdRoll, maxCorrRoll = conf.getPIDRoll();
		kpPitch, kiPitch, kdPitch, maxCorrPitch = conf.getPIDPitch();
		kpYaw, kiYaw, kdYaw, maxCorrYaw = conf.getPIDYaw();

		self.pidRoll 		= pid("pidRoll", kpRoll, kiRoll, kdRoll, maxCorrRoll)
		self.pidPitch 		= pid("pidPitch", kpPitch, kiPitch, kdPitch, maxCorrPitch)
		self.pidYaw 		= pid("pidYaw", kpYaw, kiYaw, kdYaw, maxCorrYaw)
		
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

		if self.motor_controller.isPowered():
			self.setControl(pidRoll, pidPitch, pidYaw);

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

		self.wifi.sendQuadStatus(objectToSend);

	def callbackReceivedData(self, data):
		if 'Order' in data:
			if data['Order'] == 'CALIBRATE_MPU':
				self.mpu.calibrate();
				conf = setting();
				rollError, pitchError = self.mpu.getGyroError();
				conf.setGyroError(rollError, pitchError);
			return;

		if (data['PIDMode'] > 0):
			self.pidReceivedData(data);
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
			self.pidRoll.reset()
			self.pidPitch.reset()
			self.pidYaw.reset()

	def pidReceivedData(self, data):

		if (data['PIDMode'] == 11 or data['PIDMode'] == 12 ): # P
			self.pidRoll.setKp(data['PIDValue']);
		#elif (data['PIDMode'] == 12 ): 
			self.pidPitch.setKp(data['PIDValue']);
		elif (data['PIDMode'] == 13 ): 
			self.pidYaw.setKp(data['PIDValue']);

		elif (data['PIDMode'] == 21 or data['PIDMode'] == 22 ): # I
			self.pidRoll.setKi(data['PIDValue']);
		#elif (data['PIDMode'] == 22 ): 
			self.pidPitch.setKi(data['PIDValue']);
		elif (data['PIDMode'] == 23 ): 
			self.pidYaw.setKi(data['PIDValue']);

		elif (data['PIDMode'] == 31 or data['PIDMode'] == 32 ): # D
			self.pidRoll.setKd(data['PIDValue']);
		#elif (data['PIDMode'] == 32 ): 
			self.pidPitch.setKd(data['PIDValue']);
		elif (data['PIDMode'] == 33 ): 
			self.pidYaw.setKd(data['PIDValue']);

		elif (data['PIDMode'] == 4): # save
			conf = setting();
			conf.setPIDRoll(self.pidRoll.getKp(), self.pidRoll.getKi(), self.pidRoll.getKd());
			conf.setPIDPitch(self.pidPitch.getKp(), self.pidPitch.getKi(), self.pidPitch.getKd());
			conf.setPIDYaw(self.pidYaw.getKp(), self.pidYaw.getKi(), self.pidYaw.getKd());

		else:
			if (data['PIDMode'] == 1):
				objectToSend = {
				'type'		: 'Roll',
				'KPID'	: self.pidRoll.getKPID()};
			elif (data['PIDMode'] == 2):
				objectToSend = {
				'type'		: 'Pitch',
				'KPID'	: self.pidPitch.getKPID()};
			elif (data['PIDMode'] == 3):
				objectToSend = {
				'type'		: 'Yaw',
				'KPID'	: self.pidYaw.getKPID()};

			self.wifi.sendData(objectToSend);		


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
		conf = setting();
		Roll, Pitch = conf.getGyroError();
		
		self.mpu = mpu(updateoffset=False, errorRoll = Roll, errorPitch = Pitch);
		self.mpu.setCallbackUpdate(self.mpuUpdated)
		self.mpu.run()

quadcopterInstance = quadcopter();
