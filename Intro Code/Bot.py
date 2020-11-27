import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

#load the .env file
load_dotenv()
#setting prefix for commands
client = commands.Bot(command_prefix = ".")
TOKEN = os.getenv('DISCORD_TOKEN')

#creating on ready command to let us know the bot is online 
@client.event
async def on_ready():
    print("Bot is online. ")

#reading messages sent in a discord and responds to specific phrases or words
@client.event
async def on_message(message):
    if (message.content.startswith("Hello")):
        await message.channel.send("hello")
        #add reaction to message sent
        emoji  = '\N{THUMBS UP SIGN}'
        await message.add_reaction(emoji)

    #processes all commands in messages so bot can read other commands afterwards
    await client.process_commands(message)

#command input your prefix then your command 
@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')

client.run(TOKEN)
