# Imports
import asyncio
from discord.utils import get
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# load the .env file
load_dotenv(".env")
client = commands.Bot(command_prefix="MR. HAT!")
TOKEN = os.getenv('DISCORD_TOKEN')

# Define Constants
swear_ban_time = 15

# Define Dictionaries
swear_words = open("swear_words.txt", "r")


# creating on ready command to let us know the bot is online
@client.event
async def on_ready():
    print("My Boty is ready...")


# Read Dictionary Method
async def read_dic(msg, dic):
    dic.seek(0)     # Set the line reader to the first line
    for word in dic.readlines():
        if word.strip().lower() in msg.content.lower():
            return True

    return False


# reading messages sent in a discord and responds to specific phrases or words
@client.event
async def on_message(msg):
    swear_check = await read_dic(msg, swear_words)

    # Swear Check: Did the person swear? Is this person a REAL person? Are we REAL?
    if swear_check and not msg.author.bot:
        # Role Check: Is the bot more superior than the offending user? Is the user the server owner?
        if get(msg.guild.roles, name="ToxicBot") > msg.author.top_role and msg.author.id != msg.guild.owner_id:
            await msg.author.send(f"Watch your language. You have been banned for {swear_ban_time} seconds\n"
                                      f"You may use the invite link to rejoin: https://discord.gg/gMYzJN8hb7")
            await msg.author.ban(reason="Cursing")
            await msg.channel.send(f"{msg.author.mention} was banned")
            await asyncio.sleep(swear_ban_time)
            await msg.author.unban()
        else:
            await msg.reply(f"You should be setting an example")

    # processes all commands in messages so bot can read other commands afterwards
    await client.process_commands(msg)


# command input your prefix then your command
@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')

client.run(TOKEN)