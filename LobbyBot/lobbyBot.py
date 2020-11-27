import discord
import random
import string
from discord.ext import commands

client = discord.Client()

tokenFile = open("token.txt", 'r')
token = tokenFile.read()
tokenFile.close()

lobbies = {}

bot = commands.Bot(command_prefix=".")

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    await bot.process_commands(message)

#Check for correct input and return correct relevant information
async def getParams(ctx, arg):
    channel = ctx.message.channel
    user = ctx.message.author
    arg = arg.upper()
    if not(arg in lobbies):
        await channel.send("{} is not a valid lobby!".format(arg))
        return channel, user, ""
    return channel, user, arg

#Creates a new lobby with either a randomly generated lobby token or one passed by the lobby creator
@bot.command()
async def startLobby(ctx):
    lobbyToken = ''.join(random.choice(string.ascii_uppercase) for i in range(5))
    lobbies[lobbyToken] = {
        'players':[ctx.message.author]
    }
    await ctx.message.channel.send("{} has started a lobby, to join, type .join {} ".format(ctx.message.author.name, lobbyToken))

#Prints information about a given lobby
@bot.command()
async def lobbyInfo(ctx, arg):
    arg = arg.upper()
    if not(arg in lobbies):
        await ctx.message.channel.send("{} is not a valid lobby".format(arg))
    else:
        await ctx.message.channel.send("Players in the lobby:")
        players = ''
        for player in lobbies[arg]['players']:
            players += (player.name)
            players += (", ")
        await ctx.message.channel.send("Participants: {}".format(players))

#Prints a list of all current lobbies
@bot.command()
async def showLobbies(ctx):
    lobbyString = ''
    for lobby in lobbies:
        lobbyString += lobby+"\n"
    if(lobbyString):
        await ctx.message.channel.send(lobbyString)
    else:
        await ctx.message.channel.send("No lobbies currently active")

#Removes empty lobbies
@bot.command()
async def cleanupLobbies(ctx):
    emptyLobbies = []
    cleanedUpLobbies = ''
    for lobby in lobbies:
        if not(lobbies[lobby]['players']):
            emptyLobbies.append(lobby)
            cleanedUpLobbies += lobby+"\n"
    for lobby in emptyLobbies:
        lobbies.pop(lobby, None)
    await ctx.message.channel.send("Deleted the following empty lobbies: {}".format(cleanedUpLobbies))     

#Allows a player not currently in a given lobby to join said lobby
@bot.command()
async def join(ctx, arg):
    channel, user, lobbyToken = await getParams(ctx, arg)
    if not(lobbyToken):
        return
    if not(user in lobbies[lobbyToken]['players']):
        lobbies[lobbyToken]['players'].append(user)
        await channel.send("{}, you have joined lobby {}".format(user.mention,lobbyToken))
    else:
        await channel.send("Cannot join {}, already in lobby!".format(lobbyToken))

#Allows a player in a lobby to leave that lobby
@bot.command()
async def leave(ctx, arg):
    channel, user, lobbyToken = await getParams(ctx, arg)
    if not(lobbyToken):
        return
    if (user in lobbies[lobbyToken]['players']):
        lobbies[lobbyToken]['players'].remove(user)
        await channel.send("{}, you have left lobby {}".format(user.mention,lobbyToken))
    else:
        await channel.send("{}, you are not in lobby {}".format(user.mention,lobbyToken))

#Message a random user in the lobby and have them remove a user of their choice from the lobby
@bot.command()
async def messageRandomUser(ctx, arg):
    channel, user, lobbyToken = await getParams(ctx, arg)
    
    if not(lobbyToken):
        return
    if not(user in lobbies[lobbyToken]['players']):
        await channel.send("{}, you are not in lobby {}".format(user.mention,lobbyToken))
    else:
        pick = lobbies[lobbyToken]['players'][random.randint(0,len(lobbies[lobbyToken]['players'])-1)]
        dmChannel = pick.dm_channel

        if not(pick.dm_channel):
            dmChannel = await pick.create_dm()
        playerNameMap = {}
        for player in lobbies[lobbyToken]['players']:
            playerNameMap[player.name.upper()] = player
        await dmChannel.send("Who do you want to remove: {}".format(playerNameMap.keys()))
        victim = ""
        def check(m):
            return m.channel == dmChannel
        while( not(victim in playerNameMap) ):
            response = await bot.wait_for('message', timeout=60.0, check=check)
            victim = response.content.upper()
        lobbies[lobbyToken]['players'].remove(playerNameMap[victim])
        await channel.send("{}, you were removed!".format(playerNameMap[victim].mention))


bot.run(token)
