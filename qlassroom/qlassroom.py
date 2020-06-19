from prefixes import *
print(time(),'Starting Qlassroom...')
import base64
import re
import random
import os
import sys
import asyncio
import discord
import dotenv
import config
import cache
import gmail
import socket
print(time(),'Imported everything.')

async def background(discord_client):

	await discord_client.wait_until_ready()
	print(time(),'\033[92mLogged in as',str(discord_client.user))
	while True:
		await asyncio.gather(
			handler(),
			sleep()
		)

async def sleep():
	await asyncio.sleep(config.read('refresh interval'))

async def handler():	

	email_ids = gmail.fetch_email_ids()

	print(time(),
		'\033[93m'+
		str(len(email_ids)),
		'\033[94mnew emails'
	)

	if not email_ids: return True

	### Get channels	
	
	channels = {
		discord_client.get_channel(int(channel_id))
		for channel_id
		in config.read('channel ids')
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
	email_full = gmail.fetch_email(email_id)

	try:
		email_b64 = email_full['payload']['parts'][0]['body']['data']
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
			config.read('email pattern'),
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
	
	cache.write(cache.read().union({email_id}))

	return True

def load_new_email_ids():

	# Call the gmail API

	try:
		response = gmail_client.users().messages().list(
			userId = 'me',
			q = config.read('email query')
		).execute()
	except socket.timeout:
		print(time(),error,'Connection timed out.')
		return set()

	# Subtract discord_clienth sets from each other

	if response and ( 'messages' in response ):
		received_ids = {
			email_info['id']
			for email_info in response['messages']
		}
	else:
		recived_ids = set()
	
	past_ids = cache.read()
	cache.write(past_ids.intersection(received_ids))
	return received_ids - past_ids

try:
	dotenv.load_dotenv()
	discord_client = discord.Client()	
	discord_client.loop.create_task(background(discord_client))
	print(time(),'Bot ready.')

	discord_client.run(os.environ['discord_token'])
except KeyboardInterrupt:
	print(time(),'\033[91mStopping...')
except Exception as e:
	print(time(),error,e)
	pass

