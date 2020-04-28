from dotenv import load_dotenv
load_dotenv()

import os
import discord
import requests
import re

client = discord.Client()
active_ids = []
active_results = []
digits = [
	'0️⃣',
	'1️⃣',
	'2️⃣',
	'3️⃣',
	'4️⃣',
	'5️⃣',
	'6️⃣',
	'7️⃣',
	'8️⃣',
	'9️⃣'
]

@client.event
async def on_ready():
	print('Logged in as',str(client.user))

@client.event
async def on_message(message):

	match = re.match(
		'q(|css|canvas|html|http|js|svg|webdev|standards|webext|webgl)\s(.*)',
		message.content
	)

	if match:
		results = requests.get(
			f'https://developer.mozilla.org/api/v1/search/en-us?q={match.group(0)}&topic={match.group(1)}'
		).json()['documents']

		reply = await message.channel.send(
			embed = await embed(results[0])
		)

		for digit in digits:
			await reply.add_reaction(digit)

		active_ids.append(reply.id)
		active_results.append(results)

		if len(active_ids) > 10:
			del active_ids[0]
			del active_results[0]

@client.event
async def on_reaction_add(reaction, user):
	await react(reaction,user)

@client.event
async def on_reaction_remove(reaction, user):
	await react(reaction,user)

async def embed(result):
	return discord.Embed(
		title=result['title'],
		description=result['excerpt']
	)

async def react(reaction,user):
	if (user != client.user
		and reaction.message.id in active_ids
		and reaction.emoji in digits):
		await reaction.message.edit(
			embed = await embed(
				active_results[active_ids.index(reaction.message.id)][digits.index(reaction.emoji)]
			)
		)

client.run(os.environ['TOKEN'])
