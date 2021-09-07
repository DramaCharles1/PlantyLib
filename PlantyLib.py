#!/usr/bin/env python

#PlantyConnect
import serial
import serial.tools.list_ports
from time import sleep
#PlantyCommands
from enum import Enum

class PlantyConnect:
	def __init__(self, port, baudrate, delay):
		if port == "":
			try:
				self.port = self.__getPort()
			except Exception as e:
				print(e) 
		else:
			self.port = port
		
		self.baudrate = baudrate
		self.delay = delay
		self.ser = None
		
		try:
			self.ser = serial.Serial(self.port, self.baudrate) 
		except serial.SerialException as SerialEx:
			print(str(SerialEx))
			
		sleep(2)
			
	def __getPort(self):
		portlist = serial.tools.list_ports.comports(include_links=False)
		arduinoport = ""
		
		for port in portlist:
			if "Genuino" in port.description:
				arduinoport = port.device
			
		if arduinoport == "":
			raise Exception("Could not find any arduino")
			
		return arduinoport
	
	def closePort(self):
		self.ser.flush()
		self.ser.close()
		
	def write(self, message):
		message = message + '\n'
		self.ser.write(message.encode('utf-8'))
		sleep(self.delay)
		
	def read(self):	
		if self.ser.in_waiting > 0:
			while self.ser.in_waiting > 0:
				rec = self.ser.readline()
			return rec
		else:
			raise Exception("No incoming message")
			
	def setDelay(self,newDelay):
		self.delay = newDelay

class TempOption(Enum):
	TEMP = 1
	HUMIDITY = 2
			
class PlantyCommands:
	def __init__(self, port, baudrate, delay):
		self.connect = PlantyConnect(port,baudrate,delay)
		self.recMessage = ""
		self.sendMessage = ""
		
	def __checkCommand(self, rec):
		ok = "OK"
		err = "ERR"
	
		if("OK" in str(rec)):
			return True
		elif ("ERR" in str(rec)):
			return False
		else:
			raise Exception("Not a valid command recieved" + "rec: " + rec) 
			
	def __getCommandValue(self, rec):
		separator = ['=',',','\n']
		rec = str(rec).replace('=',',')
		value = str(rec).split(',')
	
		return value[1]
		
	def __sendMessage(self):
		self.connect.write(self.sendMessage)
		self.sendMessage = ""
		
	def __recMessage(self):
		rec = self.connect.read()
		if self.__checkCommand(rec):
			self.recMessage = self.__getCommandValue(rec)
		else:
			raise Exception("Error when recieving message: " + str(rec))
		
	def readPlant(self):
		self.sendMessage = "PLANT=1"
		self.__sendMessage()
		self.__recMessage()
		
	def writePlant(self, plant):
		oldDelay = self.connect.delay
		self.connect.setDelay(0.5)
		self.sendMessage = "PLANT=2," + plant
		self.__sendMessage()
		self.__recMessage()
		self.connect.setDelay(oldDelay)
		
	def readTemp(self, TempOption):
		if TempOption == TempOption.TEMP:
			self.sendMessage = "TEMP=1"
			self.__sendMessage()
			self.__recMessage()
		elif TempOption == TempOption.HUMIDITY:
			self.sendMessage = "TEMP=2"
			self.__sendMessage()
			self.__recMessage()
			
	def readMoisture(self, samples):
		oldDelay = self.connect.delay
		newDelay = oldDelay + (samples*400)/1000
		self.connect.setDelay(newDelay)
		self.sendMessage = "MOIS=" + str(samples)
		self.__sendMessage()
		self.__recMessage()
		self.connect.setDelay(oldDelay)
					
