from PlantyLib import PlantyConnect as con
from PlantyLib import PlantyCommands as command
from PlantyLib import TempOption

#print("Test PlantyCommand")
#Open port
#plantyConnect = con("/dev/ttyACM0",57600,0.1)
#Send data
#testMessage = "PLANT=1"
#plantyConnect.write(testMessage)
#Rec data
#recMessage = plantyConnect.read()
#print(str(recMessage))
#Close port
#plantyConnect.closePort()

print("Test PlantyCommand")
plantycommand = command("",57600,0.1)
plantycommand.readTemp(TempOption.TEMP)
print(plantycommand.recMessage)
plantycommand.readPlant()
print(plantycommand.recMessage)
plantycommand.readTemp(TempOption.HUMIDITY)
print(plantycommand.recMessage)
plantycommand.readMoisture(5)
print(plantycommand.recMessage)
