import RPI.GPIO as GPIO # interface to control the raspberry pi pins
import Adafruit_DHT as dht  #module to interact with temperature sensor


import requests 
import time
import datetime
import socket
import fcntl
import struct
import asyncio

from dotenv import load_dotenv
import os






def post_to_server(payload:object) -> int:
    pass


def get_ip_address(ifname: str) -> str:
    try:
        # Create socket 
        family = socket.AF_INET  #for IPv4
        protocol = socket.SOCK_DGRAM  #for UDP
        client_socket = socket.socket(family, protocol)

        #get packed ip address
        request_code = 0x8915
        packed_ip_address = fcntl.ioctl(client_socket.fileno(), request_code, struct.pack('256s',ifname[:15].encode()))

        # convert ip address from packed binary string to human readable: b'\x7f\x00\x00\x01' -> 127.0.0.1 
        ip_address = socket.inet_ntoa(packed_ip_address[20:24])
    
    except Exception as e:
        ip_address = None
        log_error(e.args)
    finally:
        client_socket.close()
    return ip_address


def get_temp_and_hum(pin: int) -> [] :
    pass 


def get_temperature(pin_number: int)->float:
    sensor_type = dht.DHT22
    time.sleep(2)

    #read data from the dht sensor and returns a tuple containing humidity and temperature values
    _, temperature = dht.read_retry(sensor_type, pin_number, retries=5)
    
    if(temperature is None):
        return None
    else:
        #NEEED TO DO SOME ADJUSTEMENT 
        return temperature


def get_humidity(pin_number:int)->float:
    sensor = dht.DHT22
    time.sleep(2)

    #read data from the dht sensor and returns a tuple containing humidity and temperature values
    humidity, _ = dht.read_retry(sensor, pin_number, retries=5)
    
    if(humidity is None):
        raise ValueError("Humidity value not captured")
    else:
        return humidity



# handling door status
def get_backdoor_status():
    pass
def get_frontdoor_status():
    pass


# when an error occurs, light will flash to indicate that there is a problem
def err_blink_light_control(light_pin:int, magnet_pin:int) -> None:
    GPIO.output(light_pin, GPIO.HIGH)
    GPIO.output(magnet_pin, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(light_pin, GPIO.LOW)
    GPIO.output(magnet_pin, GPIO.LOW)
    time.sleep(0.5)


def time_in_range(start: datetime, end: datetime, current: datetime) -> bool:
    return start <= current <= end


def log_error(message):
    date_log = str(datetime.datetime.now())
    with open("SIMS_LOG.txt", "a+") as f:
        f.write(date_log + " -- " + message + "\n")
        
            
def clean():
    GPIO.cleanpup()



def main():
    # pin numbers
    light_out_pin= 4
    magnet_light_pin = 2
    front_magnet_sensor_pin = 27 # pin for the front door
    back_magnet_sensor_pin = 21  # pin for the back door
    temp_humidity_sensor_pin = 23
    

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    #set up for all the pins used 

    GPIO.setup(temp_humidity_sensor_pin,GPIO.IN)

    # NOTE: what does the pull_uip_down param do?
    GPIO.setup(front_magnet_sensor_pin,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    GPIO.setup(light_out_pin, GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(magnet_light_pin, GPIO.OUT, initial=GPIO.HIGH)


    
    payload = {}

    #LOOOP
    # load environment variables
    load_dotenv()


    payload["frontdoor status"] = get_frontdoor_status(front_magnet_sensor_pin)
    payload["backdoor status"] = get_backdoor_status(back_magnet_sensor_pin)
    payload["temperature"] = get_temperature(temp_humidity_sensor_pin)
    payload["humidity"] = get_humidity(temp_humidity_sensor_pin)
    payload["post_key"] = os.getenv("POST_KEY")
    payload["IP_eht0"] = get_ip_address() #*** maybe not

    async def inner_loop():
        pass
        
        
    # check for error

    # check if back is open and do some light games

    # post payload to database
    post_to_server(payload)
    
    #if the back

    # delay () 


if __name__ == "__main__":
    main()