import discord
import asyncio
import os
import random
import praw

from discord.ext import commands, tasks
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

path = r"C:\Users\Sunny Yang Xu\Python 3.6\animal"

async def send_random():
    random_filename = random.choice([
        x for x in os.listdir(path)
        if os.path.isfile(os.path.join(path, x))
    ])
    channel = bot.get_channel(774739743899648000)
    await channel.send(file=discord.File(random_filename))
    await channel.send("here's your daily dose of wholesomeness")
    
@bot.event
async  def on_ready():
    change_status.start()
    print('bot in active')

@tasks.loop(seconds=10)
async def change_status():
    await bot.change_presence(activity=discord.Game('online'))
    print('test')
    await send_random()
    
bot.run(TOKEN)
