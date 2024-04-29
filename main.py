import discord
import asyncio
import requests
from datetime import datetime

intents = discord.Intents.default()
intents.messages = True 

client = discord.Client(intents=intents)

API_URL = 'http://api.timezonedb.com/v2.1/get-time-zone?key=API_KEY&format=json&by=zone&zone=Asia/Kolkata'

def fetch_api_data():
    response = requests.get(API_URL)
    if response.status_code == 200:
        return response.json()
    else:
        return None
    
@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    channel = discord.utils.get(client.get_all_channels(), name='general')
    if channel is None:
        print("General channel not found.")
        return

async def send_hi():
    await client.wait_until_ready()
    channel = discord.utils.get(client.get_all_channels(), name='general')
    if channel is None:
        print("General channel not found.")
        return
    while not client.is_closed():
        api_data = fetch_api_data()
        if api_data:
            utc_time = datetime.utcfromtimestamp(api_data['timestamp'])
            formatted_time = utc_time.strftime('%Y-%m-%d %H:%M:%S')
            message = f'Current Time (India): {formatted_time}'
            await channel.send(message)
        else:
            await channel.send('Failed to fetch API data')
        await asyncio.sleep(60)

async def start_bot():
    await client.start("Enter your token")

async def main():
    await asyncio.gather(start_bot(), send_hi())

asyncio.run(main())
