#!/usr/bin/env python

#PlantyConnect
import serial
import serial.tools.list_ports
from time import sleep

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
			if "Genuino" or "Arduino" in port.description:
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
			
		
	
