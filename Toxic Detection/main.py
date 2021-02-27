# Imports
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# load the .env file
load_dotenv(".env")
client = commands.Bot(command_prefix="MR. HAT!")
TOKEN = os.getenv('DISCORD_TOKEN')

# Define Constants


# Define Dictionaries



# creating on ready command to let us know the bot is online
@client.event
async def on_ready():
    print("My Boty is ready...")


# Read Dictionary Method
async def read_dic(msg, dic):
    pass

# reading messages sent in a discord and responds to specific phrases or words
@client.event
async def on_message(msg):
    # Swear Check: Did the person swear? Is this person a REAL person? Are we REAL?
    if condition:
        # Role Check: Is the bot more superior than the offending user? Is the user the server owner?
        if condition:
            pass
        else:
            pass

    # processes all commands in messages so bot can read other commands afterwards
    await client.process_commands(msg)


# command input your prefix then your command
@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')

client.run(TOKEN)
