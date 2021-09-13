import sys
sys.path.insert(0,"/home/pi/Repos/PlantyLib")
from PlantyLib import PlantyConnect as con
from PlantyLib import PlantyCommands as command
from PlantyLib import TempOption
from PlantyLib import ColorOption


class TestLib:
	def __init__(self):
		#self.plantyConnect = con("",57600,0.1)	
		
		self.planty = command("",57600,0.1)
		
	def connect(self):
		self.planty.connectToPlant()
		return True
		
	def port_to_planty(self):
		#print("Test PlantyCommand")
		#Open port
		port = self.planty.connect.port
		return port
	
	def read_plant(self):
		self.planty.readPlant()
		recPlant = self.planty.recMessage
		return recPlant
		
	def read_temp(self):
		self.planty.readTemp(TempOption.TEMP)
		temp = self.planty.recMessage
		return temp
		
	def read_moisture(self):
		self.planty.readMoisture(5)
		mois = self.planty.recMessage
		return mois
		
	def read_ALS(self):
		self.planty.readALS()
		light = self.planty.recMessage
		return light
		
	def start_motor(self):
		self.planty.setMotor(True, 100, 5000)
		return self.planty.sendMessage
		
	def white_light(self):
		self.planty.setLight(True, ColorOption.WHITE, 255)
		return self.planty.sendMessage
		
	def set_PI(self):
		self.planty.setPI(True, 1, 1, 200, 20000)
		return self.planty.sendMessage
		
	def read_PI(self):
		self.planty.readPI()
		return self.planty.sendMessage
		
	def start_PI(self):
		self.planty.startPI(True,5000)
		return self.planty.sendMessage

if __name__ == "__main__":
	test = TestLib()
	test.connect()
	print("Plant: " + test.read_plant())
	#print("Temp: " + test.read_temp())
	#print("Moisture: " + test.read_moisture())
	#print("ALS: " + test.read_ALS())
	#print("Motor: " + test.start_motor())
	#print("LED: " + test.white_light())
	#print("Write PI parameters: " + test.set_PI())
	#print("Read PI parameters: " + test.read_PI())
	#print("Start PI: " + test.start_PI())
#Send data
#testMessage = "PLANT=1"
#plantyConnect.write(testMessage)
#Rec data
#recMessage = plantyConnect.read()
#print(str(recMessage))
#Close port
#plantyConnect.closePort()

#print("Test PlantyCommand")
#plantycommand = command("",57600,0.1)
#plantycommand.readTemp(TempOption.TEMP)
#print(plantycommand.recMessage)
#plantycommand.readPlant()
#print(plantycommand.recMessage)
#plantycommand.readTemp(TempOption.HUMIDITY)
#print(plantycommand.recMessage)
#plantycommand.readMoisture(5)
#print(plantycommand.recMessage)



