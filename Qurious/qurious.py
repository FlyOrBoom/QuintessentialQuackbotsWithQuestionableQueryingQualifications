from dotenv import load_dotenv
load_dotenv()

import os
import discord
import requests
import re
import textwrap

mdn='https://developer.mozilla.org/'
client = discord.Client(
	activity=discord.CustomActivity('Query MDN: .q / .qjs / .qcs / etc')
)
active_ids = []
active_documents = []
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
		'.mdn(|css|canvas|html|http|js|svg|webdev|standards|webext|webgl)\s(.*)',
		message.content
	)

	if match:
		async with message.channel.typing():
			documents = requests.get(
				f"{mdn}api/v1/search/en-US?q={match.group(0)}&topic={match.group(1)}"
			).json()['documents']

			for document in documents:
				document['url']=f"{mdn}en-US/docs/{document['slug']}"

			reply = await message.channel.send(
				embed = await embed(documents[0])
			)

		for digit in digits:
			await reply.add_reaction(digit)

		active_ids.append(reply.id)
		active_documents.append(documents)

		if len(active_ids) > 10:
			del active_ids[0]
			del active_documents[0]

@client.event
async def on_reaction_add(new_reaction, user):
	if (user != client.user
		and new_reaction.message.id in active_ids
		and new_reaction.emoji in digits):
		await new_reaction.message.edit(
			embed = await embed(
				active_documents[active_ids.index(new_reaction.message.id)][digits.index(new_reaction.emoji)]
			)
		)
		for reaction in new_reaction.message.reactions:
			if reaction != new_reaction:
				async for user in reaction.users():
					if user != client.user:
						await reaction.remove(user)

async def embed(document):
	return discord.Embed(
		title=document['title'],
		url=document['url'],
		description=(
			re.sub(r"<.+?>",'',
			re.sub(r"<\/?pre>",'```',
			re.sub(r"<\/?code>",'`',
			re.sub(r"<\/?em>",'*',
			re.sub(r"<\/?strong>",'**',
			requests.get(f"{document['url']}?summary&raw").text
		)))))),
		color=0x83d0f2
	).set_author(
		name='ᴍᴅɴ',
		url=f"{mdn}en-US/docs/Web",
		icon_url=f"{mdn}static/img/favicon32.7f3da72dcea1.png"
	).set_footer(
		text='Click the numbers below to view other results'
	)

client.run(os.environ['TOKEN'])
