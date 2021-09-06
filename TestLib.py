from PlantyLib import PlantyConnect as con

#Open port
plantyConnect = con("/dev/ttyACM0",57600,0.1)
#Send data
testMessage = "PLANT=1"
plantyConnect.write(testMessage)
#Rec data
recMessage = plantyConnect.read()
print(recMessage)
#Close port
plantyConnect.closePort()
