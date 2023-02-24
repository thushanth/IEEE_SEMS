# About the program

Smart Environment Monitoring System (SEMS project)
Main.py is the final script runs on startup and loops infinitely

## Objective

Client
- Read temperature, humidity and magnetic door sensor pin state.
- Report to led ring if back door was left open to user before locking the main lab door.
- Post to status values to dB.

Broker
Scripts thereafter with appropriate key can access the data and build specific functions without affect SEMS device. (Fragmentation)
	- Script written to deploy on discord for users to type and request door sensor status.
	- Script written to deploy on IEEE Website to post lab status.

This script depends on the following python modules:
i. rpi.GPIO (comes with raspi) for magnetic sensor and indicator lights
ii. requests  for REST API
iii. time (comes with raspi) for time delays
iv. hdc_1080 library for temperature and Humidity sensor
v. neopixel adafruit library for led ring

---

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
- After wiring sudo nano /boot/config.txt
- Remove # to uncomment dtparam=spi=on
- Add dtoverlay=enc28j60
- sudo reboot now
- sudo nano /lib/systemd/system/setmac.service
- Add the following

```
[Unit]
Description=Set MAC address for ENC28J60 module
Wants=network-pre.target
Before=network-pre.target
BindsTo=sys-subsystem-net-devices-eth0.device
After=sys-subsystem-net-devices-eth0.device
[Service]
Type=oneshot
ExecStart=/sbin/ip link set dev eth0 address b8:27:eb:00:00:01
ExecStart=/sbin/ip link set dev eth0 up
[Install]
WantedBy=multi-user.target
```
  

After saving:

- sudo chmod 644 /lib/systemd/system/setmac.service
- sudo systemctl daemon-reload
- sudo systemctl enable setmac.service
- Sudo reboot
- Connect ethernet cable and use ifconfig to see its new ip address without usb

```
[https://www.raspberrypi-spy.co.uk/2020/05/adding-ethernet-to-a-pi-zero/](https://www.raspberrypi-spy.co.uk/2020/05/adding-ethernet-to-a-pi-zero/)
```
  

Disable WIFI:

- Sudo apt install rfkill
- Sudo rfkill block wifi
To undo sudo rfkill unblock wifi

Add gateway:

- Sudo route -n
- Sudo route add default gw 192.168.2.1
