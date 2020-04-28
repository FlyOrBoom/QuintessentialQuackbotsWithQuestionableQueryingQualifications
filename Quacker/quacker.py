from dotenv import load_dotenv
load_dotenv()

import os
import discord
from random import randint, random
import asyncio

client = discord.Client()
latest_message_id = {}

@client.event
async def on_ready():
	print('Logged in as ' + str(client.user))

@client.event
async def on_message(message):
	channel = message.channel
	if (
		message.author != client.user
		and any(trigger in channel.name for trigger in ['duck','bot','spam'])
	):
		latest_message_id[str(channel.id)] = message.id
		await asyncio.sleep(random()*4) #Pause and ponder
		async with channel.typing():
			for i in range(1,8):
				await asyncio.sleep(random())
				cancel = latest_message_id[str(channel.id)] != message.id #Stops typing if there's a new message
				if cancel: break
			if not cancel:
				await channel.send(
					( 'quack' if randint(0,36) else 'honk' ) * randint(1,5)
					+ ( '!' if randint(0,1) else '?' )
				)

client.run(os.environ['TOKEN'])
