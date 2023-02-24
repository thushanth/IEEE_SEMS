# About the program

Smart Indoor Monitoring System project (SIMS project)
This is the final script runs on startup and loops infinitely

This script depends on the following python modules:
i. rpi.GPIO (comes with raspi)        for magnetic sensor and indicator lights
ii. requests  for REST API
ii. time (comes with raspi) for time delays
ii. adafruit_DHT for temperature and Humidity sensor


## Handling the concurren

# Hardware Wiring

### RGB LED

connected to port D18 or pin 12 on the board physically for data.


### ENC28J60 - Ethernet

| Gpio pinout | Physical Pin | ENC28J60 Pinout |
|----|----| ----|
| GPIO25 | PIN 22| INT |
| GPIO9 | PIN 21 | MISO |
| GPIO10 | PIN 19 | MOSI |
| GPIO11 | PIN23 | SCK |
| GPIO8 | PIN24 | CS |
| N/A | PIN 1 | 3.3V |
| N/A | PIN 6-9 | GND |


### HDC1080 - Temperature, Humidity

| Gpio pinout | Physical Pin | HDC1080 Pinout |
|----|----| ----|
| N/A | PIN 1 | 3.3V |
| N/A | PIN 6-9 | GND |
| GPIO2 | PIN 3 | SDA |
| GPIO3 | PIN 5 | SCL |


### RGB Ring 8-LED WS2812B

| Gpio pinout | Physical Pin | WS2812B Pinout |
|----|----| ----|
| GPIO25 | PIN 2-4 | 5V |
| GPIO9 | PIN 12 | Data |
| GPIO10 | PIN 6-9 | GND |

### Magnetic Switch

| Gpio pinout | Physical Pin | Reed Pinout |
|----|----| ----|
| N/A | N/A | VCC |
| GPIO23 | PIN 16 | FD |
| GPIO24 | PIN 18 | BD |

# RGB LED Script

Custom script

```

import board
import neopixel
import time
pixels = neopixel.NeoPixel(board.D18, 8)

for x in range(0, 255, 5):
	pixels.fill((0,0,x))
	print(x)
	time.sleep(.1)

for y in range(255, -5, -5):
	pixels.fill((0,0,y))
	print(y)
	time.sleep(.1)

for x in range(0, 255, 5):
	pixels.fill((0,x,0))
	print(x)
	time.sleep(.1)

for y in range(255, -5, -5):
	pixels.fill((0,y,0))
	print(y)
	time.sleep(.1)

for x in range(0, 255, 5):
	pixels.fill((x,0,0))
	print(x)
	time.sleep(.1)

for y in range(255, -5, -5):
	pixels.fill((y,0,0))
	print(y)
	time.sleep(.1)

```

# Magnetic Switch

If door is closed or power is not detected, the door is considered closed 0.
If door is open it is 1

```
import time, sys
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

in1 = 23
in2 = 24
GPIO.setup(in1, GPIO.IN)
GPIO.setuo(in2, GPIO.IN)

while True:
	print("Front Door:")
	print(GPIO.input(in1))
	print("Back Door:")
	print(GPIO.input(in2))
	time.sleep(3)
	
```

# Temperature and Humidity

git clone https://github.com/switchdoclabs/SDL_Pi_HDC1080_Python3.git 

import to have access or locate the SDL_Pi_HDC1080 Library.


```
import sys
import time
import datetime
import SDL_Pi_HDC1080

hdc1080 = SDL_Pi_HDC1080.SDL_Pi_HDC1080()

#turn on heater
hdc1080.turnHeaterOn()

#turn of heater
hdc1080.turnHeaterOff()

# change temperature resolution
hdc1080.setTemperatureResolution(SDL_Pi_HDC1080.HDC1080_CONFIG_TEMPERATURE_RESOLUTION_14BIT)

# change humdity resolution
hdc1080.setHumidityResolution(SDL_Pi_HDC1080.HDC1080_CONFIG_HUMIDITY_RESOLUTION_14BIT)

while True:
	print ("-----------------")
	print ("Temperature = %3.1f C" % hdc1080.readTemperature())
	print ("Humidity = %3.1f %%" % hdc1080.readHumidity())
	print ("-----------------")
	time.sleep(3.0)
```

# Ethernet
