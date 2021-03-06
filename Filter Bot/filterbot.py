
import cv2
# pip install opencv-python
import numpy as np
from PIL import Image
# pip install Pillow
# python3 -m pip install Pillow
from _io import BytesIO
import requests
import discord
from discord.ext import commands

sushi = commands.Bot(command_prefix="&")
# client

@sushi.event
async def on_ready():
	print("Sushi has been fried!")

@sushi.command()
async def filter(ctx, arg):
	sendfile = 0
	for file in ctx.message.attachments:
		sendfile = 1
		link = requests.get(file.url)
		img = Image.open(BytesIO(link.content))
		img.save('image.jpg')

		image = cv2.imread('image.jpg')

		filename = 'filtered.jpg'

		if arg == 'blur':
			blurred = cv2.GaussianBlur(image,(33,33,),0)
			# blurred = cv2.medianBlur(image,55)
			cv2.imwrite(filename,blurred)
			await ctx.message.channel.send(file=discord.File(filename))

		elif arg == 'gray':
			gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
			cv2.imwrite(filename,gray)
			await ctx.message.channel.send(file=discord.File(filename))

		elif arg == 'edge':
			gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
			blurred = cv2.GaussianBlur(gray,(5,5,),0)
			edged = cv2.Canny(blurred,85,85)
			cv2.imwrite(filename,edged)
			await ctx.message.channel.send(file=discord.File(filename))

		elif arg == 'reflect':
			flip = cv2.flip(image, 1)
			cv2.imwrite(filename,flip)
			await ctx.message.channel.send(file=discord.File(filename))

		elif arg == 'bright':
			array = np.array([[0.01, 0.54, 0.9],[0.4, 0.01, 0.4],[0.01, 0.2, 0.01]])
			bright = cv2.filter2D(image, -1, array)
			cv2.imwrite(filename,bright)
			await ctx.message.channel.send(file=discord.File(filename))

		elif arg == '70s':
			gray = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
			cv2.imwrite(filename,gray)
			await ctx.message.channel.send(file=discord.File(filename))
		
		else:
			await ctx.message.channel.send('Improper Usage\nFilters: **blur, gray, edge, reflect, bright, 70s**\nFilter Usage Example: *&filter edge*')

	if sendfile == 0:
		await ctx.message.channel.send('Improper Usage\nFilters: **blur, gray, edge, reflect, bright, 70s**\nFilter Usage Example: *&filter edge*')




sushi.run("TOKEN")
#the last line needs to be .run
