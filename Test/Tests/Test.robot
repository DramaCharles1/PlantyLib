*** Settings ***
Documentation  Test robotframework
Library  ../Resources/TestLib.py
*** Variables ***
${hej}  lol
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
Web page
	test web page
