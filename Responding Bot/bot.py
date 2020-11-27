import discord
import asyncio
import os
import random
import requests

from discord import Game
from discord.ext import commands
from discord.ext.commands import Bot
from dotenv import load_dotenv

#API
api_key = '3dc655783087f33f09b2b6436a9c2ac0'
base_url = "http://api.openweathermap.org/data/2.5/weather?"
URL = 'https://official-joke-api.appspot.com/random_joke'

#token
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

path = r"C:\Users\Sunny Yang Xu\Python 3.6\animal"
random_filename = random.choice([
    x for x in os.listdir(path)
    if os.path.isfile(os.path.join(path, x))
])

RESPONSES = {
    'yang':['( ͡° ͜ʖ ͡°)',"That's me!",'Did you say YANGGGGGGG',
            "Yang can't pick up the phone rn",'gang gang gang','Yangcouver','Yanghai','Yang Francisco','Yang Jose','Yang Diego', 'Yangwerp', 'Yangtes', 'Yangchester', 'Vayangcia',
            'Casayangca','Yangkara','Yangalore','Yangon', 'Yangkok','Yangdung','Yangzhou','Yangzig','Yangshasa','Yangama City','Hayanga','San Yang (or Yang Juan)','Yangtiago de Chile',
            'Yangto Domingo', 'Rio de Yangeiro', 'Yang Prabang (or Luang Prayang)','Yang Mai'],
    'raghib':['hey Raghib!','Raghib?'],
    'ben':['yo Ben!','Bennifer','MUSHU LI :dragon:'],
    'helen':['Heleeeeeeeeeen!','Heleleleleleelelen',':girl:'],
    'evan':['Evan my guy','EVAAAAAAAAAAAN','circuits'],
    'ty':['any time :) my friend','nppppppppppppppp',],
    'how are you':['good good and you?','happy',],
    'good':['great',':smile:',],
    "what's your favourite food?":['Korean corndogs','rice obviously :rice:','fried rice!'],
    'ying':['yang',':yin_yang:']

    }

#functions
path = r"C:\Users\Sunny Yang Xu\Python 3.6\animal"

async def meme_random():
    random_filename = random.choice([
        x for x in os.listdir(path)
        if os.path.isfile(os.path.join(path, x))
    ])
    channel = client.get_channel(774739743899648000)
    await channel.send(file=discord.File(random_filename))
    await channel.send("we memeing out here")
    
def check_valid_status_code(request):
    if request.status_code == 200:
        return request.json()

    return False

def get_joke():
    request = requests.get(URL)
    data = check_valid_status_code(request)

    return data

async def respond_to_certain_things(message, msg_content):
    if msg_content in RESPONSES.keys():
        responses = RESPONSES[msg_content]
        await send_random(message, responses)



async def send_random(message, responses):
    response = random.choice(responses)
    await message.channel.send(response)
    return
    
                      
#main
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=" Netflix Startup"))

#auto-responder
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    msg_content = message.content.lower()
    await respond_to_certain_things(message, msg_content)
    
    #contents
    if message.content == '-help':
        embed = discord.Embed(title="List of Commands", description='Here are the things I can do! (For now :smirk:)')
        embed.add_field(name="Games :game_die:", value="8ball", inline=False)
        embed.add_field(name="Conversation", value=str(RESPONSES.keys()), inline=False)
        embed.add_field(name="Fun :joy:", value="joke, meme", inline=False)

        await message.channel.send(embed=embed)

#meme
    if message.content.startswith('meme'):
        await meme_random()
#8ball
    if message.content.startswith('8ball'):
        await message.channel.send(random.choice(["It is certain :8ball:","Definetly not :8ball:","It is not looking likely :8ball:",'Too hard to tell :8ball:','Definitely :8ball:']))

#jokes
    if message.content.startswith('joke'):
        joke = get_joke()
        print(joke)

        if joke == False:
            await message.channel.send("Couldn't get joke from API. Try again later.")
        else:
            await message.channel.send(joke['setup'] + '\n' + joke['punchline'])        
#weather
##@client.command()
##async def weather(ctx, *, city: str):
##    city_name = city
##    complete_url = base_url + "appid=" + api_key + "&q=" + city_name
##    response = requests.get(complete_url)
##    x = response.json()
##    channel = ctx.message.channel
##    if x["cod"] != "404":
##        async with channel.typing():
##            y = x["main"]
##            current_temperature = y["temp"]
##            current_temperature_celsiuis = str(round(current_temperature - 273.15))
##            current_pressure = y["pressure"]
##            current_humidity = y["humidity"]
##            z = x["weather"]
##            weather_description = z[0]["description"]
##            embed = discord.Embed(title=f"Weather in {city_name}",
##                          color=ctx.guild.me.top_role.color,
##                          timestamp=ctx.message.created_at,)
##            embed.add_field(name="Descripition", value=f"**{weather_description}**", inline=False)
##            embed.add_field(name="Temperature(C)", value=f"**{current_temperature_celsiuis}°C**", inline=False)
##            embed.add_field(name="Humidity(%)", value=f"**{current_humidity}%**", inline=False)
##            embed.add_field(name="Atmospheric Pressure(hPa)", value=f"**{current_pressure}hPa**", inline=False)
##            embed.set_thumbnail(url="https://i.ibb.co/CMrsxdX/weather.png")
##            embed.set_footer(text=f"Requested by {ctx.author.name}")
##            await channel.send(embed=embed)
##    else:
##        await channel.send("City not found.")
    
client.run(TOKEN)

