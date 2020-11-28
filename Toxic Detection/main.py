import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import json

load_dotenv(".env")
client = commands.Bot(command_prefix="et ")
client.remove_command("help")


# Dictionaries, if these return an error, uncomment the line below
# os.chdir(r"File directory of your files e.g. C:\folder\positive_words.txt")
pos_words = open("positive_words.txt", "r")
neg_words = open("negative_words.txt", "r")


@client.event
async def on_ready():
    print("My Boty is ready...")


async def read_dic(msg, dic):
    max_points = 0
    dic.seek(0)
    for line in dic.readlines():
        word = line.split()[0].lower()
        if word in msg.content.lower():
            points = int(line.split()[1])
        else:
            points = 0

        if points > max_points:
            max_points = points

    return max_points


async def edit_user(msg, user, points):
    with open("users.json", "r") as file:
        users = json.load(file)

    if user not in users:
        users[user] = {}
        users[user]["Reputation"] = 0
        users[user]["Kindness"] = 0
        users[user]["Toxicness"] = 0
    if points > 0:
        users[user]["Reputation"] += points
        users[user]["Kindness"] += points

        if users[user]["Kindness"] >= 24 and users[user]["Toxicness"] > 0:
            users[user]["Kindness"] -= 24
            users[user]["Toxicness"] -= 1
    elif points < 0:
        users[user]["Reputation"] += points
        users[user]["Toxicness"] -= points
        if users[user]["Toxicness"] > 30:
            users[user]["Toxicness"] = 30

        await msg.channel.send(f"{msg.author.mention},"
                               f" you should probably refrain from being toxic *[{users[user]['Toxicness']}/30]*")
        if users[user]["Toxicness"] >= 30:
            users[user]["Toxicness"] = 0
            try:
                await msg.author.ban(reason="Toxic Behaviour")
                await msg.channel.send(f"{msg.author} has been *banned*")
            except discord.Forbidden:
                await msg.channel.send("**ERROR:**  My permissions are not high enough to ban this user")

    with open("users.json", "w") as file:
        json.dump(users, file, indent=4)


@client.event
async def on_message(msg):
    if not msg.author.bot:
        max_points = await read_dic(msg, pos_words)
        await edit_user(msg, str(msg.author.id), max_points)

        max_points = await read_dic(msg, neg_words)
        await edit_user(msg, str(msg.author.id), -max_points)

    await client.process_commands(msg)


@client.command(aliases=["p", "prof"])
async def profile(ctx, victim: discord.User = None):
    with open("users.json", "r") as file:
        users = json.load(file)

    if victim and not victim.bot:
        user = str(victim.id)
        user_info = victim
    else:
        user = str(ctx.author.id)
        user_info = ctx.author

    if user not in users:
        users[user] = {}
        users[user]["Reputation"] = 0
        users[user]["Kindness"] = 0
        users[user]["Toxicness"] = 0

        with open("users.json", "w") as file:
            json.dump(users, file, indent=4)

    profile_embed = discord.Embed(colour=0X2072AA)
    profile_embed.set_author(name=f"{user_info.name}'s Profile", icon_url=user_info.avatar_url)
    profile_embed.set_thumbnail(url=user_info.avatar_url)
    profile_embed.add_field(name="STATS:",
                            value=f"**Reputation:** {users[user]['Reputation']}\n"
                                  f"**Kindness:** {users[user]['Kindness']}\n"
                                  f"**Toxicness:** {users[user]['Toxicness']}",
                            inline=False)

    await ctx.send(embed=profile_embed)

client.run(os.getenv("DISCORD_TOKEN"))
