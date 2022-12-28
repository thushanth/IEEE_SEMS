import RPI.GPIO as GPIO # interface to control the raspberry pi pins
import Adafruit_DHT as dht  #module to interact with temperature sensor

import time
import datetime
import socket
import fcntl
import struct

from typing import List

from dotenv import load_dotenv
import os


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

    GPIO.setup(front_magnet_sensor_pin,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    GPIO.setup(light_out_pin, GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(magnet_light_pin, GPIO.OUT, initial=GPIO.HIGH)



    load_dotenv()
    # object to send to server
    payload = {}
    payload["post_key"] = os.getenv("POST_KEY")
    payload["IP_eht0"] = get_ip_address() #*** maybe not

    start_time = datetime.datetime.now()

    while True:
        try: 
            # get current status of the lab and update the payload
            payload["frontdoor_status"] = get_status(front_magnet_sensor_pin)
            payload["backdoor_status"] = get_status(back_magnet_sensor_pin)
            
            temperature, humidity  = get_temperature_and_humidity(temp_humidity_sensor_pin)

            payload["temperature"] = temperature
            payload["humidity"] = humidity


            #if frontdoor and backdoor are open
            if payload("frontdoor_status")==1 and payload("backdoor_status")==1:
                pass            


            # send the payload to the server every 5 minutes
            end_time = datetime.datetime.now()
            elasped_time = end_time - start_time 
            elapsed_minutes = elasped_time.total_seconds()/60

            if(elapsed_minutes > 5): 
                # post payload to database
                url = os.getenv("DATABASE_URL")
                post_to_db(payload, url)
                
                #reset timer
                start_time = datetime.datetime.now()
        except:
        # error handling        
            pass
        finally:
            pass



# connect to database and inser
def post_to_db(payload: object, url: str ) -> None:
    try:
        client = MongoClient(url)
        db = client["reports"]
        collection  = db["statusReports"]
        collection.insert_one(payload)

    except Exception as e:
        pass
    finally:
        pass

    # remove oldest record from database
    return 1

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
    finally:
        client_socket.close()
    return ip_address


def get_temperature_and_humidity(pin_number: int) -> List[float]:
    sensor_type = dht.DHT22
    time.sleep(2)

    #read data from the dht sensor and returns a tuple containing humidity and temperature values
    humidity, temperature = dht.read_retry(sensor_type, pin_number, retries=5)

    if (temperature is None):
        raise Error("Cannot get humidity or temperature", 1)
    elif (humidity is None):
        raise Error("Cannot get humidity")
    else:
        return [temperature,humidity]



# handling door status
def get_status(pin_number: int) -> int:
    status = GPIO.input(pin_number)

    if status == True : return 1
    elif status == False : return 0
    else : raise Error("Cannot get door status",1)
         

            
def clean():
    GPIO.cleanpup()



class Error(Exception):
    def __init__(self, message:str, code:int):
        self.message = message
        self.code = code
        self.signal_error(code)
        self.log_error(message)
        super().__init__(self.message)
    
    def signal_error(self,code:int):
        # switch case that ini
        pass


    def log_error(self,message:str):
        date_log = str(datetime.datetime.now())
        with open("SIMS_LOG.txt", "a+") as f:
            f.write(date_log + " -- " + message + "\n")




if __name__ == "__main__":
    main()