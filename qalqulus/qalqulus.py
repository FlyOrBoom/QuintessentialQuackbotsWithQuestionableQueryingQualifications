import os,asyncio,json,discord
from dotenv import load_dotenv
import re

load_dotenv()

client = discord.Client()

@client.event
async def on_ready():
	print('Logged in as ' + str(client.user))

@client.event
async def on_message(message):
	channel = message.channel
	if message.author != client.user:
		match = re.match(r'\!leithold (\d+)', message.content.lower())
		if match:
			page = str(int(match.groups()[0]))
			try:
				await channel.send(file=discord.File('resources/leithold-'+page+'.jpg'))
			except Exception:
				await channel.send("I don't have that page!")

client.run(os.environ['TOKEN'])
