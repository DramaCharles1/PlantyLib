from PlantyLib import PlantyConnect as con
from PlantyLib import PlantyCommands as command
from PlantyLib import TempOption

class TestLib:
	def __init__(self):
		#self.plantyConnect = con("",57600,0.1)		
		self.planty = command("",57600,0.1)
		
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

if __name__ == "__main__":
	test = TestLib()
	print("Plant: " + test.read_plant())
	print("Temp: " + test.read_temp())
	print("Moisture: " + test.read_moisture())
	print("ALS: " + test.read_ALS())
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



