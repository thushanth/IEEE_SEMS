#------------------------
#       Libraries
#------------------------
import time
import RPi.GPIO as GPIO

#------------------------
#       Variables
#------------------------



#------------------------
#       Pin Setup
#------------------------
GPIO.setmode(GPIO.BCM)


#------------------------
#       Aux. Functions
#------------------------
def doorStatus():
    return null

def postToDB():
    return null


#------------------------
#       Main Function
#------------------------
def mainControl():
    # status of back door, if front door is open check back door. If backdoor is open show X else show Check Mark. 
    # For every 5 minutes collect the data {Temperature, Humidity, Front Door Status}
    while True:
        print("Test")

mainControl()