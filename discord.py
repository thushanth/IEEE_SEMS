import discord
from pymongo import MongoClient
from dotenv import load_dotenv
import os

client = discord.Client()

load_dotenv()
client = MongoClient(os.getenv("DATABASE_URL"))
db = client['reports']
collection = db["statusReports"]

@client.event
async def on_message(message):
    response = ""
    message = message.content
    message = message.lower()
    if message == "!status": 
        latest_payload = collection.find().sort("createdAt", -1).limit(1)
        status = latest_payload["frontdoor_status"]
        temperature = latest_payload["temperature"]
        humidity = latest_payload["humidity"]
        
        # TODO: Write logic on who is exec or not
        is_exec = True
        if(not(is_exec) and not(time_in_range())):
            response = "Lab is closed from 6PM"
        else: 
            response = get_response(status, temperature, humidity)

        await message.channel.send(response)
        


def get_response(status:int, temperature:float, humidity:float):
    response = ""

    if(status ==1):
        response = "Status: open"  
    else: response = "Status: closed" 

    response = response + "Temperature: " + temperature + "Humidity: " + humidity
    
    return response
        

# return true if time is between 8AM and 6PM
def time_in_range():
    pass 
client.run(os.getenv("DISCORD_TOKEN"))