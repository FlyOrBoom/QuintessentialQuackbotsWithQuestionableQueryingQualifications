from string_ import *
print(time(),'Starting Qlassroom...')
import base64
import re
import random
import os
import sys
import asyncio
import discord
from dotenv import load_dotenv
import config_
import cache_ 
import gmail_
print(time(),'Imported everything.')

async def background():

	await bot.wait_until_ready()
	print(time(),'\033[92mLogged in as',str(bot.user))
	while True:
		await asyncio.gather(
			handler(),
			sleep()
		)

async def sleep():
	await asyncio.sleep(config_.read('settings','refresh interval'))

async def handler():	

	email_ids = load_new_email_ids()

	print(time(),
		'\033[93m'+
		str(len(email_ids)),
		'\033[94mnew emails'
	)

	if not email_ids: return True

	### Get channels	
	
	channels = {
		bot.get_channel(int(channel_id))
		for channel_id
		in config.read('settings','channel ids')
		if channel_id
	}

	if not channels:
		print(time(),warning,'No channels specified.')
		return False

	return await asyncio.gather(*[
		send_email_to_channels(email_id,channels)
		for email_id
		in email_ids
	])

async def send_email_to_channels(email_id,channels):

	### Fetch email

	try:
		email_b64 = gmail.users().messages().get(
			userId='me',
			id=email_id
		).execute()['payload']['parts'][0]['body']['data']
	except KeyError:
		print(time(),warning,'Body data not found in email.')
		return False

	### Decode email
	
	try:
		email_text = base64.urlsafe_b64decode(
			email_b64
		).decode('utf-8').replace('\r','')
	except AttributeError:
		print(time(),warning,'Cannot decode email body.')
		return False

	### Find matches in email body
	
	try:
		matches = re.search(
			config_.read('settings','email pattern'),
			email_text
		).groups()
	except AttributeError:
		print(time(),warning,'Email body does not match pattern.')
		return False

	### Format matches

	try:
		post = {
			'teacher': matches[0],
			'type':	matches[1].capitalize(),
			'class': matches[2],
			'class_url': matches[3],
			'due': matches[4],
			'document': matches[5],
			'description': matches[6].replace('\n',' '),
			'url': matches[7]
		}
	except IndexError:
		print(time(),warning,'Insufficient matches in pattern.')
		return False

	### Create embed

	embed = discord.Embed(
		color = 0x11aa77,
		title = f'📪 '+post['type']+(': '+post['document'] if post['document'] else ''),
		description = post['description'],
		url = post['url']
	).set_author(
		name = post['class'],
		url = post['class_url']
	).set_footer(
		text = post['teacher']
	)

	if post['due']:
		embed.add_field(
			name = 'Due',
			value = post['due'],
			inline = False
		)

	### Send embed

	[	
		print(
			color_ribbon(
				''.join([str(ord(c)).zfill(2)[:2] for c in str(embed)[-17:-1]])+
				f'0000{message.id}'
				f'0000{message.guild.id}'
				f'0000{message.channel.id}'
			)
			+'\033[0m Sent post to '
			f'\033[1m{message.guild.name}\033[0m '
			f'### \033[1m{message.channel.name}\033[0m'
		)
		for message in await asyncio.gather(*[
			channel.send(embed=embed)
			for channel
			in channels
		])
	]
	
	cache_.write(cache_.read()+email_ids)	

	return True

def load_new_email_ids():

	# Call the Gmail API

	response = gmail.users().messages().list(
		userId = 'me',
		q = config_.read('settings','email query')
	).execute()

	# Subtract both sets from each other

	if response and ( 'messages' in response ):
		received_ids = {
			email_info['id']
			for email_info in response['messages']
		}
	else:
		received_ids = set([])
	
	past_ids = cache_.read()
	cache_.write(past_ids.union(received_ids))
	return received_ids - past_ids

gmail = gmail_.load(config_.read('paths','gmail'))
print(time(),'Gmail config.ready.')
load_dotenv()
bot = discord.Client()	
bot.loop.create_task(background())
print(time(),'Bot config.ready.')

try:
	bot.run(os.environ['discord_token'])
except KeyboardInterrupt:
	print(time(),'\033[91mStopping...')
except Exception as e:
	print(e)
	pass
finally:
	sys.exit(0)

