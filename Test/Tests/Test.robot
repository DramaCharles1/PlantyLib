*** Settings ***
Documentation  Test robotframework
Library  /home/pi/Repos/PlantyLib/Test/Resources/TestLib.py
*** Test Cases ***
Connect to Planty
	connect
	port to planty
Data
	connect
	read temp
	read plant
Messages
	start motor
