import discord 
import asyncio
import os
import random

from dotenv import load_dotenv

#token
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()
channel = client.get_channel(781325140881047572)

#not case sensitive 
TRIGGER_WORDS = {
    "yang": ["That's me!", "( ͡° ͜ʖ ͡°)"],
    "marco": ["polo!"],
    "hi": ["hello","hi",":smile:"],
    "8ball": ["It is certain :8ball:","Definetly not :8ball:","It is not looking likely :8ball:",'Too hard to tell :8ball:','Definitely :8ball:']
    }


#functions
async def random_response(message, responses):
    response = random.choice(responses)
    await message.channel.send(response)
    return

async def respond_to_trigger_words(message, msg_content):
    if msg_content in TRIGGER_WORDS.keys():
        responses = TRIGGER_WORDS[msg_content]
        await random_response(message, responses)

#on ready
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=" Netflix"))

#auto-responder
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    msg_content = message.content.lower()
    await respond_to_trigger_words(message, msg_content)

client.run(TOKEN)

    

