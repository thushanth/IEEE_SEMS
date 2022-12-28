import time
import RPi.GPIO as GPIO
import requests         # importing requests library
import Adafruit_DHT as dht

import datetime

import socket
import fcntl
import struct


# ------------------------
#       Config
# ------------------------
# StatusVar can be  1 for OPEN and 0 for CLOSED
# TemperatureVar can be any numerical values
serverStatus = 1
highOpenGlo = 1
lowClosedGlo = 0

sleepTimeGlo = 5
tempHumidSleeptime = 2


doorStatVarGlo = 1
magnetDoorStatVarGlo = 1

temperatureVarGlo = 0
humidityVarGlo = 0

temperature_calibrate = 2  # Subtract from original Temperature
Humidity_calibrate = 4  # Subtract from original Humidity

ipAddressGLO = "No update"

postKey = "zgVV@l@mC_"
lastStateVarGlo = 'closed'

payload = {}    # Post Request payload declaration
# DO NOT change the name of the key in the payload list
payload['Status'] = doorStatVarGlo
payload['Temperature'] = temperatureVarGlo
payload['PostKey'] = postKey
payload['Humidity'] = humidityVarGlo
payload['IP_eth0'] = ipAddressGLO

postServerURL = 'http://sems.ieeeconcordia.ca/rec_save_pull_cre.php'
getLogURL = 'http://sems.ieeeconcordia.ca/simsLog.txt'
userAgentURL = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 12; SM-S906N Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.119 Mobile Safari/537.36"}
disPayURL = 'https://discord.com/api/webhooks/1020589058109481051/0AeSWY6O1dVYPQwmQS3NEdcCu1Gwn7MHzZYV9iLw5cHXzpEhgUxYggeHX7pZZiOaeNNI'
disLabURL = 'https://discord.com/api/webhooks/1045583811796271114/rb5EJV6YlGwGoVeQvFNGdlAQ1oN9HPlGESTB2jux5TMQUERMthild_djIf3tW2qqpPsP'

LightPinGlo = {
                                        "postLight1": 4,
                                        "magnetLight1": 2
                                }

magnetPinGlo = {
                                        "magnet1": 27
                                }
tempHumidPinGlo = {
                                        "tempHumid1": 3
                                }

# interruptBounceTime = 1
countLimit = 10

# calibConst  =  5

start = datetime.time(8, 0, 0)
end = datetime.time(17, 0, 0)
currentTime = datetime.datetime.now().time()

# ------------------------------
#       Setup & Initialize the pins
# ------------------------------
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(magnetPinGlo["magnet1"], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(tempHumidPinGlo["tempHumid1"], GPIO.IN)
GPIO.setup(LightPinGlo["postLight1"], GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(LightPinGlo["magnetLight1"], GPIO.OUT, initial=GPIO.HIGH)


# ------------------------
#       Functions
# ------------------------

def time_in_range(start, end, current):
	return start <= current <= end


def mainControl():
        # payload['Status'] = 0
        # payload['PostKey'] = postKey
        # payload['Temperature'] = 92
        # w = requests.post(postServerURL, payload, headers=userAgentURL)
        # return
        ####
        # w = requests.get(postServerURL, headers=userAgentURL)
        ####
        # temperature = 999
        # message = "labstatus: "+ str(temperature)
        # disPayURL="https://discord.com/api/webhooks/1020589058109481051/0AeSWY6O1dVYPQwmQS3NEdcCu1Gwn7MHzZYV9iLw5cHXzpEhgUxYggeHX7pZZiOaeNNI"
        # disPayLoad = {"content": message}
        # w = requests.post(disPayURL, data=disPayLoad)
        # print(w)
        # return

        # exitVar = 0
        doorStatOldTemp = GPIO.input(magnetPinGlo["magnet1"])
        doorStatNewTemp = 0
        counter = 0

        # while exitVar != countLimit:
        while True:
                if serverStatus == 1:
                        doorStatNewTemp = GPIO.input(magnetPinGlo["magnet1"])

                        if doorStatOldTemp == doorStatNewTemp:
                                doorStatOldTemp = doorStatNewTemp
                                counter = counter + 1
                                # print("same door Stat" + str(counter))
                        else:
                                counter = 0
                                doorStatOldTemp = doorStatNewTemp
                                # print("different door stat" + str(counter))

                        if counter == countLimit:
                                counter = 0
                                doorIsOpen()
                                readTempHumid()

                                set_ip_address_GLO_write_2_txtfile()

                                post2Server(postServerURL)

                                postLightControl()

                else:
                        err_blink_light_control()

                # get4mServer(getLogURL)
                time.sleep(sleepTimeGlo)


def door_change_event_callback_function(channel_pin):
        # print('Door Status Change function called!')
        global magnetDoorStatVarGlo
        magnetDoorStatVarGlo = GPIO.input(magnetPinGlo["magnet1"])
        magnetIndicatorLightControl()


GPIO.add_event_detect(
    magnetPinGlo["magnet1"], GPIO.BOTH, callback=door_change_event_callback_function)


def magnetIndicatorLightControl():

        if magnetDoorStatVarGlo == highOpenGlo:
                GPIO.output(LightPinGlo["magnetLight1"], highOpenGlo)
        else:
                GPIO.output(LightPinGlo["magnetLight1"], lowClosedGlo)


def doorIsOpen():
        global doorStatVarGlo
        doorStatVarGlo = GPIO.input(magnetPinGlo["magnet1"])
        payload['Status'] = doorStatVarGlo
        # print("status: " + str(payload['Status']))


def postLightControl():
        if doorStatVarGlo == highOpenGlo:
                GPIO.output(LightPinGlo["postLight1"], highOpenGlo)
        else:
                GPIO.output(LightPinGlo["postLight1"], lowClosedGlo)


def readTempHumid():
        time.sleep(tempHumidSleeptime)
        global temperatureVarGlo
        global humidityVarGlo

        temperatureVar_Origin = 999
        humidityVarGlo_Origin = 999

        h, t = dht.read_retry(dht.DHT22, tempHumidPinGlo["tempHumid1"])

        # if (h is not None and t is not None):
        if (h is not None and t is not None):
                temperatureVar_Origin = t
                humidityVarGlo_Origin = h
        else:
                temperatureVar_Origin = 999
                humidityVarGlo_Origin = 999

        # if (temperatureVar_Origin == int(temperatureVar_Origin)):
        temperatureVarGlo = temperatureVar_Origin - temperature_calibrate
        humidityVarGlo = h
        # else:
                # temperatureVarGlo = 999
                # humidityVarGlo = 999

        payload['Temperature'] = temperatureVarGlo
        payload['Humidity'] = humidityVarGlo

        # if (h is not None and t is not None):
                # print( "Temp: " + str(payload['Temperature']))
                # print("Humid: " + str(payload['Humidity']))
        # else:
                # print "Error collecting values"

# if (h is not None and t is not None):
                # print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(t, h))


def err_blink_light_control():
        GPIO.output(LightPinGlo["postLight1"], GPIO.HIGH)
        GPIO.output(LightPinGlo["magnetLight1"], GPIO.HIGH)
        time.sleep(.5)
        GPIO.output(LightPinGlo["postLight1"], GPIO.LOW)
        GPIO.output(LightPinGlo["magnetLight1"], GPIO.LOW)
        time.sleep(.5)


def post2Server(urlStr):
        global lastStateVarGlo
        # Post Request with payload variable using requests library
        # w = requests.post('http://sems.ieeeconcordia.ca/rec_save_pull_cre.php', payload)
        try:
                status = payload.get('Status')
                if status == 1:
                        keyword = 'open'
                elif status == 0:
                        keyword = 'closed'
                else:
                        keyword = 'invalid'

                message = "Labstatus: "+keyword+" Temperature: " + \
                    str(int(payload.get('Temperature'))) + \
                        " Humidity: "+str(int(payload.get('Humidity')))

				currentTime = datetime.datetime.now().time()

                if keyword == 'open' and lastStateVarGlo != 'open':
                        lastStateVarGlo = keyword
                        disPayLoad = {"content": message}
                        g = requests.post(disPayURL, data=disPayLoad)
							if time_in_range(start, end, currentTime)) == true
								print(true)


                elif keyword == 'closed' and lastStateVarGlo == 'open':
                        lastStateVarGlo=keyword
                        disPayLoad={"content": message}
                        g=requests.post(disPayURL, data = disPayLoad)
							if time_in_range(start, end, currentTime)) == true
								print(true)

        #       message = "Labstatus: "+keyword+" Temperature: "+str(int(payload.get('Temperature')))+" Humidity: "+str(int(payload.get('Humidity')))
                w=requests.post(urlStr, payload, headers=userAgentURL)
        #       g = requests.post(disPayURL, data = disPayLoad)
        except requests.exceptions.HTTPError as errh:
                date_log=datetime.datetime.now()
                with open("SIMS_LOG.txt", 'a+') as f:
                        f.write(str(date_log) + " -- " + \
                                "Http Error: " + errh + '\n')
                # print ("Http Error:",errh)
        except requests.exceptions.ConnectionError as errc:
                # print ("Error Connecting:",errc)
                date_log=datetime.datetime.now()
                with open("SIMS_LOG.txt", 'a+') as f:
                        f.write(str(date_log) + " -- " + \
                                "Connecting Error: " + errc + '\n')
        except requests.exceptions.Timeout as errt:
                # print ("Timeout Error:",errt)
                date_log=datetime.datetime.now()
                with open("SIMS_LOG.txt", 'a+') as f:
                        f.write(str(date_log) + " -- " + \
                                "Timeout Error: " + errt + '\n')
        except requests.exceptions.RequestException as err:
                # print ("OOps: Something Else",err)
                date_log=datetime.datetime.now()
                with open("SIMS_LOG.txt", 'a+') as f:
                        f.write(str(date_log) + " -- " + \
                                "Some Unknown Error: " + err + '\n')
        print(w.text)

def get4mServer(UrlStr):
        global serverStatus
        # Get request just to check the simsLog.txt file
        # try:
        r=requests.get(UrlStr)
        if r.text == 'Updated':
                # print(r.text)
                serverStatus=1
        else:
                # print('error!')
                serverStatus=0
        # except:
                # print('No file')
        # =================================================================

def get_ip_address(ifname):
        try:
                s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                return socket.inet_ntoa(fcntl.ioctl(
                        s.fileno(),
                        0x8915,  # SIOCGIFADDR
                        struct.pack('256s', ifname[:15])
                )[20:24])
        except:
                date_log=datetime.datetime.now()
                with open("SIMS_LOG.txt", 'a+') as f:
                        f.write(str(date_log) + " -- " +
                                "IP address retrieval error occurred. " + '\n')

# NOTE : why do we need this?
def set_ip_address_GLO_write_2_txtfile():
        # print get_ip_address('lo')
        # print get_ip_address('eth0')

        global ipAddressGLO
        ipAddressGLO=str(get_ip_address('eth0'))
        payload['IP_eth0']=ipAddressGLO

        # with open("SIMS_IPAddress.txt",'a+') as f:
        with open("SIMS_IPAddress.txt", 'w+') as f:
                date_log=datetime.datetime.now()
                f.write(str(date_log) + " -- " + "IP Address of lo" + \
                        ": " + get_ip_address('lo') + '\n')
                f.write(str(date_log) + " -- " + "IP Address of eth0" + \
                        ": " + get_ip_address('eth0') + '\n')


def destroy():
  # GPIO.output(LedPin, GPIO.LOW)   # led off
  GPIO.cleanup()                  # Release resource

mainControl()
