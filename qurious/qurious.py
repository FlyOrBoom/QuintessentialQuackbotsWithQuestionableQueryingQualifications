import os, discord, requests
from dotenv import load_dotenv

mdn = 'https://developer.mozilla.org/'
digits = ['0️⃣', '1️⃣','2️⃣','3️⃣', '4️⃣','5️⃣','6️⃣', '7️⃣','8️⃣','9️⃣']
active_ids = []
active_documents = []
load_dotenv()
client = discord.Client()

@client.event
async def on_ready():
	print('Logged in as',str(client.user))

@client.event
async def on_message(message):
	params = message.content.split(' ',1)
	if len(params) == 2 and ( params[0].lower() in ['.m','.mdn'] ):
		async with message.channel.typing():
			documents = requests.get(
				mdn + 'api/v1/search/en-US?highlight=false&q=' + params[1]
			).json()['documents']
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
		title =       document['title'],
		url =         mdn + 'en-US/docs/' + document['slug'],
		description = document['excerpt'],
		color =       0x83d0f2
	).set_author(
		name =       'ᴍᴅɴ',
		url =         mdn + 'en-US/docs/Web',
		icon_url =    mdn + 'static/img/favicon32.7f3da72dcea1.png'
	).set_footer(
		text =        'Click the numbers below to view other results'
	)

client.run(os.environ['TOKEN'])
