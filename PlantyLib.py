#!/usr/bin/env python

#PlantyConnect
import serial
import serial.tools.list_ports
from time import sleep
#PlantyCommands
from enum import Enum
from enum import IntEnum

class PlantyConnect:
	'''
	Port to access Arduino. Baudrate 57600 default. Delay in ms between send and recieve
	'''
	def __init__(self, port: str, baudrate: int, delay: float):
		if port == "":
			try:
				self.port = self.__get_connected_port()
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
		print(f"Connected to: {self.port}")

	def __get_connected_port(self):
		'''
		Get connected port from arduino if no port has been specified
		'''
		portlist = serial.tools.list_ports.comports(include_links=False)
		arduinoport = ""

		for port in portlist:
			if "Genuino" in port.description:
				arduinoport = port.device

		if arduinoport == "":
			raise Exception("Could not find any arduino")

		return arduinoport

	def close_port(self):
		'''
		Close serial port
		'''
		self.ser.flush()
		self.ser.close()

	def write(self, message: str):
		'''
		Write to serial port
		'''
		message = message + '\n'
		self.ser.write(message.encode('utf-8'))
		sleep(self.delay)

	def read(self):
		'''
		read from serial port
		'''
		if self.ser.in_waiting > 0:
			while self.ser.in_waiting > 0:
				rec = self.ser.readline()
			return rec
		else:
			raise Exception("No incoming message")

	def set_delay(self, delay: float):
		'''
		Set delay between send and recieve
		'''
		self.delay = delay


class Temp_option(Enum):
	'''
	Temperature sensor options
	'''
	TEMP = 1
	HUMIDITY = 2


class Light_color_option(IntEnum):
	'''
	Light color option
	'''
	PURPLE = 1
	WHITE = 2
	RED = 3
	GREEN = 4
	BLUE = 5

MOIS_DELAY = 500 #ms

class PlantyCommands(PlantyConnect):
	'''
	Class with all commands
	'''
	def __init__(self, port="", baudrate=57600, delay=0.5):
		super().__init__(port, baudrate, delay)

	def __check_command(self, rec):
		'''
		Check command for correct format
		'''
		if "OK" in str(rec):
			return True
		elif "ERR" in str(rec):
			return False
		else:
			raise Exception("Not a valid command recieved" + "rec: " + rec)

	def __get_command_value(self, rec):
		'''
		Get command values
		'''
		separator = ['=',',','\n']
		rec = str(rec).replace('=',',')
		value = str(rec).split(',')

		return value[1]

	def __send_message(self, message: str):
		'''
		Send message to Planty
		'''
		print(f"send: {message}")
		self.write(message)

	def __recieve_message(self):
		'''
		Recieve message from Planty
		'''
		recieve = self.read()
		print(f"Recieve: {recieve}")

		if self.__check_command(recieve):
			return self.__get_command_value(recieve)
		else:
			raise Exception("Error when recieving message: " + str(recieve))

	def read_plant(self):
		'''
		Read what is planted
		'''
		command = "PLANT=1"
		self.__send_message(command)
		return self.__recieve_message()

	def writePlant(self, plant: str):
		'''
		Write what is planted
		'''
		command = f"PLANT=2,{plant}"
		self.__send_message(command)
		self.__recieve_message()

	def read_temp(self, temp_option: Temp_option):
		'''
		Read temperatue or humidity in house
		'''
		if temp_option == Temp_option.TEMP:
			command = "TEMP=1"
			self.__send_message(command)
			return self.__recieve_message()

		elif temp_option == Temp_option.HUMIDITY:
			command = "TEMP=2"
			self.__send_message(command)
			return self.__recieve_message()

		else:
			raise AttributeError("No valid temp sensor option")

	def read_moisture(self, samples: int):
		'''
		Read moisture sensor. Average value from n samples
		samples(int): number of samples
		'''
		command = f"MOIS={str(samples)}"
		self.__send_message(command)
		return self.__recieve_message()

	def read_ALS(self):
		'''
		Read ALS
		'''
		command = "ALS"
		self.__send_message(command)
		return self.__recieve_message()

	def start_pump(self, start: bool, power: int, duration: int):
		'''
		Start or stop pump
		start(bool): start or stop pump
		power(int): pump power in %
		duration(int): duration in ms
		'''
		if start:
			command = f"MOTR=1,{str(power)},{str(duration)}"
		else:
			command = f"MOTR=0,{str(power)},{str(duration)}"
		self.__send_message(command)
		self.__recieve_message()

	def lights(self, write: bool, color_option: Light_color_option, power: int):
		'''
		Set LED lights. 
		write(bool): read or write LED lights
		color_option(Light_color_option): choose color
		power(int): light power in %
		'''
		if write:
			command = f"LED=1,{str(int(color_option))},{str(power)}"
		else:
			command = "LED=2"
		self.__send_message(command)
		self.__recieve_message()

	def light_regulator_values(self, write: bool, kp: float, ki: float, t: int, max_signal: int):
		'''
		Set PI light regulator values
		write(bool): read or write regulator values
		kp(float): p part
		ki(float): i part
		t(int): integral time
		max_signal(int): maximum signal
		'''
		if write:
			command = f"PISET=2,{str(kp)},{str(ki)},{str(t)},{str(max_signal)}"
		else:
			command = "PISET=1"
		self.__send_message(command)
		self.__recieve_message()

	def start_light_regulator(self, start: bool, set_point: int):
		'''
		Start or stop light regulator
		start(bool): start or stop the light regulator
		set_point(int): light set point
		'''
		if start:
			command = f"PI=2,1,{str(set_point)}"
		else:
			command = "PI=2,0,0"
		self.__send_message(command)
		self.__recieve_message()

if __name__ == "__main__":
	print("test program")
	'''	planty_connect = PlantyConnect("",57600,0.1)
	msg = "PLANT=1"
	planty_connect.write(msg)

	rec = planty_connect.read()
	print(f"rec: {rec}")

	planty_connect.close_port()'''

	planty = PlantyCommands()

	'''plant_read = planty.read_plant()
	print(f"Plant: {plant_read}")

	temp_read = planty.read_temp(Temp_option.TEMP)
	print(f"Temperatur: {temp_read}")'''

	'''humidity_read = planty.read_temp(Temp_option.HUMIDITY)
	print(f"Humidity: {humidity_read}")'''

	mois_read = planty.read_moisture(5)
	print(f"Moisture: {mois_read}")

	ALS_read = planty.read_ALS()
	print(f"ALS: {ALS_read}")

	planty.close_port()
