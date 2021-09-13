#!/usr/bin/env python

#PlantyConnect
import serial
import serial.tools.list_ports
from time import sleep
#PlantyCommands
from enum import Enum
from enum import IntEnum

class PlantyConnect:
	#Port to access Arduino. Baudrate 57600 default. Delay in ms between send and recieved messages
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
	
	#Get connected port from arduino if no port has been specified		
	def __getPort(self):
		portlist = serial.tools.list_ports.comports(include_links=False)
		arduinoport = ""
		
		for port in portlist:
			if "Genuino" in port.description:
				arduinoport = port.device
			
		if arduinoport == "":
			raise Exception("Could not find any arduino")
			
		return arduinoport
	
	#Close port
	def closePort(self):
		self.ser.flush()
		self.ser.close()
	
	#Send message
	def write(self, message):
		message = message + '\n'
		self.ser.write(message.encode('utf-8'))
		sleep(self.delay)
	
	#Read incoming message
	def read(self):	
		if self.ser.in_waiting > 0:
			while self.ser.in_waiting > 0:
				rec = self.ser.readline()
			return rec
		else:
			raise Exception("No incoming message")
	
	#Set delay between send and recieve
	def setDelay(self,newDelay):
		self.delay = newDelay

#Temperature sensor options
class TempOption(Enum):
	TEMP = 1
	HUMIDITY = 2

#LED color option
class ColorOption(IntEnum):
	PURPLE = 1
	WHITE = 2
	RED = 3
	GREEN = 4
	BLUE = 5
			
#Class containing all commads
class PlantyCommands:
	#Port to access Arduino. Baudrate 57600 default. Delay in ms between send and recieve
	def __init__(self, port, baudrate, delay):
		self.port = port
		self.baudrate = baudrate
		self.delay = delay
		self.connect = None
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
			
	def connectToPlant(self):
		self.connect = PlantyConnect(self.port,self.baudrate,self.delay)
	
	#Read plant name from NVM	
	def readPlant(self):
		self.sendMessage = "PLANT=1"
		self.__sendMessage()
		self.__recMessage()
	
	#Write plant name to NVM	
	def writePlant(self, plant):
		oldDelay = self.connect.delay
		self.connect.setDelay(0.5)
		self.sendMessage = "PLANT=2," + plant
		self.__sendMessage()
		self.__recMessage()
		self.connect.setDelay(oldDelay)
	
	#Read temperature or humidity
	def readTemp(self, TempOption):
		if TempOption == TempOption.TEMP:
			self.sendMessage = "TEMP=1"
			self.__sendMessage()
			self.__recMessage()
		elif TempOption == TempOption.HUMIDITY:
			self.sendMessage = "TEMP=2"
			self.__sendMessage()
			self.__recMessage()
	
	#Read moisture sensor. Average value from n samples		
	def readMoisture(self, samples):
		oldDelay = self.connect.delay
		newDelay = oldDelay + (samples*400)/1000
		self.connect.setDelay(newDelay)
		self.sendMessage = "MOIS=" + str(samples)
		self.__sendMessage()
		self.__recMessage()
		self.connect.setDelay(oldDelay)
	
	#Read light sensor
	def readALS(self):
		self.sendMessage = "ALS"
		self.__sendMessage()
		self.__recMessage()
	
	#Start or stop motor. Duration [ms]
	def setMotor(self, start, power, duration):
		if start:
			self.sendMessage = "MOTR=1," + str(power) + "," + str(duration)
		else:
			self.sendMessage = "MOTR=0," + str(power) + "," + str(duration)
	
	#Set LED
	def setLight(self, write, ColorOption, power):
		if write:
			self.sendMessage = "LED=1," + str(int(ColorOption)) + "," + str(power)
		else:
			self.sendMessage = "LED=2"
	
	#Read/write light PI parameters
	def setPI(self, write, kp, ki, t, maxControl):
		if write:
			self.sendMessage = "PISET=2," + str(kp) + "," + str(ki) + "," + str(t) + "," + str(maxControl) 
		else:
			self.sendMessage = "PISET=1"
	
	#Start liht PI
	def startPI(self, on, setPoint):
		if on:
			self.sendMessage = "PI=2,1," + str(setPoint)
		else:
			self.sendMessage = "PI=2,0,0"
	
	#Read light PI parameters
	def readPI(self):
		self.sendMessage = "PI=1"
	
			
	
			
					
