#libraries
import discord
import asyncio
import os
import random

from dotenv import load_dotenv

#token
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

#channel
channel = client.get_channel(774739743899648000)

#dictionary 
TRIGGER_WORDS = {
    "yang": ["That's me!", "( ͡° ͜ʖ ͡°)"],
    "marco": ["polo!"],
    "hi": ["hello","hi",":smile:"],
    "8ball": ["It is certain :8ball:", "Definetly not :8ball:", "Definietly :8ball:" ]

    }

#functions: 
#random_response
async def random_response(message, responses):
	response = random.choice(reponses)
	await message.channel.send(response)
	return

#respond_to_trigger_words
async def respond_to_trigger_words(messgae, msg_content):
	if msg_content in TRIGGER_WORDS.keys():
		reponses = TRIGGER_WORDS[msg_content]
		await random_response(messgae, reponses)


#on ready
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=" Netflix"))


#main
@client.event
async def on_message(message):
	if message.auther == client.user:
		return

	msg_content = message.content.lower()
	await respond_to_trigger_words(messages, msg_content)

client.run(TOKEN)
