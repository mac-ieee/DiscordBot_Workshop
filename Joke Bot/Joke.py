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
    #opening jokes file and setting a list of each joke as an element to joke_list
    with open('Jokes.txt', 'r', encoding="utf8") as f:
        joke_list = f.readlines()
    msg = random.choice(joke_list) #choosing random element from the list
    await ctx.send(msg) #sending message

#knock knock joke command
@client.command()
async def knockjoke(ctx):
    await ctx.send("Knock Knock!")
    
    #waiting for the user to send the message "who's there?" it will timeout in 60 seconds
    def check(msg):
        return msg.content == "who's there?" and msg.channel == ctx.channel and msg.author == ctx.author
    await client.wait_for("message", check=check, timeout = 60.0)

    #opening knockjokes file and setting a list of each joke to knock_joke_list
    with open("knockjokes.txt", "r", encoding="utf8") as f:
        knock_joke_list = f.readlines()
    joke = random.choice(knock_joke_list).split("*") #choosing a random joke from the list and splitting that list into two sublists
    who = joke[0] #the who is the first element of the list
    await ctx.send(who)

    #waiting for user to send "{message that bot just sent} who?" it will timeout in 60 seconds
    message = f"{who} who?"
    def check1(msg):
        return msg.content == message and msg.channel == ctx.channel and msg.author == ctx.author
    await client.wait_for("message", check=check1, timeout = 60.0)

    await ctx.send(joke[1]) #sending second element in joke sublist

client.run(TOKEN)