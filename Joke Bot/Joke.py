import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import random

#load the .env file
load_dotenv()
#setting prefix for commands
client = commands.Bot(command_prefix = '.')
TOKEN = os.getenv('DISCORD_TOKEN')

#creating on ready command to let us know the bot is online 
@client.event
async def on_ready():
    print("Bot is online. ")

#joke command
@client.command()
async def joke(ctx):
    with open('Jokes.txt', 'r',encoding="utf8") as f: #opening jokes file
        l = f.readlines() #l is a list where each joke is an element
    msg = random.choice(l) #choosing random element from the list
    await ctx.send(msg) #sending message

client.run(TOKEN)