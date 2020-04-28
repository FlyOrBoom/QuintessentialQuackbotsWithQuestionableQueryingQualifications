from dotenv import load_dotenv
load_dotenv()

import os
import discord
import requests
import re
import textwrap

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
	if (user != client.user
		and new_reaction.message.id in active_ids
		and new_reaction.emoji in digits):
		await new_reaction.message.edit(
			embed = await embed(
				active_results[active_ids.index(new_reaction.message.id)][digits.index(new_reaction.emoji)]
			)
		)
		for reaction in new_reaction.message.reactions:
			if reaction != new_reaction:
				async for user in reaction.users():
					if user != client.user:
						await reaction.remove(user)

async def embed(result):
	return discord.Embed(
		title=result['title'],
		url='https://developer.mozilla.org/en-US/'+result['slug'],
		description=re.sub(
			r'<(|/)mark>',
			'',
			textwrap.shorten(result['excerpt'],width=256,placeholder='..').capitalize()+'.'
		),
		footer='⬇️ flip through results ⬇️',
		color=0xffff00
	).set_author(
		name='ᴍᴅɴ',
		url='https://developer.mozilla.org/en-US',
		icon_url='https://developer.mozilla.org/static/img/favicon32.7f3da72dcea1.png'
	)

client.run(os.environ['TOKEN'])
