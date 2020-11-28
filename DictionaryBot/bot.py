# bot.py
import os
import random

import discord
from dotenv import load_dotenv

from PyDictionary import PyDictionary

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

# Create dictionary instance
dictionary = PyDictionary()

# word is the word being defined
# definition is a dictionary type with key-value pairs
# of (type of word => definition)
# For example one of these pairs for "cheese" is
# ("Noun" => "a solid food prepared from the pressed curd of milk")
def create_embed(word, definition):
    to_return = discord.Embed(title = word)

    # Use the word type (e.g. noun, verb, etc) as headings
    for word_type in definition:
        # Use the actual definition associated with that word type as body text
        # under each heading
        for given_def in definition[word_type]:
            to_return.add_field(name = word_type, value = given_def, inline = False)

    return to_return

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

@client.event
async def on_message(message):
    if(message.author == client.user):
        return

    if(message.content.startswith('def')):
        word = message.content.split(' ')[1]
        definition = dictionary.meaning(word)
        print(definition)
        print(type(definition))

        if(definition):
            await message.channel.send(embed = create_embed(word, definition))
        else:
            await message.channel.send(f'{word}: definition not found')

client.run(TOKEN)