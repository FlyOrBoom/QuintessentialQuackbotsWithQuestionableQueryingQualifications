import datetime

def time_print(*args):
	print(
		f'\033[95m{str(datetime.datetime.now()).split(" ")[1].split(".")[0]}:\033[0m',
		*args,
		'\033[0m'
	)

time_print('Starting Qlassroom...')

import json

paths = None
with open('paths.json') as file:
	paths = json.loads(file.read())
if not paths:
	time_print('\033[91mMissing paths.json! Exiting...')
	sys.exit(0)

import pickle

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import base64
import re
import random

import os
import sys
import asyncio
import discord

from dotenv import load_dotenv

time_print('Imported everything.')

load_dotenv()
bot = discord.Client()

def skip(reason):
	time_print(f'\033[91m{reason} Skipping...\033[0m')
	
def get_gmail_creds():

	# If modifying these scopes, delete the file token.pickle.
	SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
		
	creds = None
	
	# The file token.pickle stores the user's access and refresh tokens, and is
	# created automatically when the authorization flow completes for the first
	# time.
	
	path = paths['gmail']['token']
	if os.path.exists(path):
		with open(path, 'rb') as token:
			creds = pickle.load(token)
	# If there are no (valid) credentials available, let the user log in.
	if not creds or not creds.valid:
		if creds and creds.expired and creds.refresh_token:
			creds.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file(
				'gmail/credentials.json', SCOPES)
			creds = flow.run_local_server(port=0)
		# Save the credentials for the next run
		with open(path, 'wb') as token:
			pickle.dump(creds, token)
	return creds

async def background():

	await bot.wait_until_ready()
	time_print('\033[92mLogged in as',str(bot.user))
	while True:
		await handler()
		refresh_interval = float(access_config(
			name = 'refresh_interval',
			default = '60'
		))
		await asyncio.sleep(refresh_interval)

async def handler():	

	email_ids = []
	email_ids = fetch_new_email_ids()

	time_print(
		'\033[93m'+
		str(len(email_ids)),
		'\033[94mnew emails'
	)

	### Get channel ids
	channel_ids = access_config(
		name = 'channel_ids',
	)	

	### Get channels	
	
	channels = [
		bot.get_channel(int(channel_id))
		for channel_id in channel_ids
		if int(channel_id) and len(channel_id) == 18
	]

	return await asyncio.gather(*[
		send_email_to_channels(email_id,channels)
		for email_id
		in email_ids
	])

def access_config(name,write='',append='',default=''):
	path = paths['config'][name]
	os.makedirs('config',exist_ok=True)
	data = None
	response = None
	if os.path.exists(path):
		with open(path,'r') as file:
			data = file.read()
	if data:
		if write:
			with open(path,'w') as file:
				file.write(write)		
		elif append:
			with open(path,'a') as file:
				file.write(append)
	else:
		with open(path,'w') as file:
			file.write(default)
	with open(path,'r') as file:
		return file.read()

async def send_email_to_channels(email_id,channels):

	### Fetch full email

	email_full = None

	email_full = gmail.users().messages().get(
		userId='me',
		id=email_id
	).execute()

	### Retrieve email body

	email_body_b64 = None
	
	try:
		email_body_b64 = email_full['payload']['parts'][0]['body']['data']
	except KeyError:
		skip('Body data not found in email!')

	### Decode email body
	
	email_body = None

	try:
		email_body = base64.urlsafe_b64decode(
			email_body_b64
		).decode('utf-8').replace('\r','')
	except AttributeError:
		skip('Cannot decode email body!')

	### Find matches in email body
	
	pattern = access_config(
		name = 'email_pattern',
		default = '(.+) p.+ (.+) in (.+)\n<(.+)>.\n\n(?:\[.*\n)?(?:Due: (.+)\n(.+)\n)?([\s\S]+)\nO.+[\n ]<(.+)>'
	)

	try:
		matches = re.search(
			pattern,
			email_body
		).groups()
	except AttributeError:
		skip('Email body does not match pattern!')
		return

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
		skip('Insufficient matches in pattern!')
		return

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
	
	print(str(
		color_ribbon(
			str(str(ord(c)).zfill(2)[:1] for c in str(embed)[-17:-1])+
			f'0000{message.id}'
			f'0000{message.guild.id}'
			f'0000{message.channel.id}'
		)
		+'\033[0m Sent post to '
		f'\033[1m{message.guild.name}\033[0m '
		f'### \033[1m{message.channel.name}\033[0m\n'
		for message in await asyncio.gather(*[
			channel.send(embed=embed)
			for channel
			in channels
		])
	))
	access_config(
		name = 'past_email_ids',
		append = ','+email_id,
		default = email_id
	)

def color_ribbon(number):
	return str([
		f'\033[38:5:{x}m▮'
		for x
		in re.findall('..',str(number))
	])

def fetch_new_email_ids():

	# Call the Gmail API

	query = access_config(
		name = 'email_query',
		default = 'newer_than:1d'
	)

	response = gmail.users().messages().list(
		userId = 'me',
		q = query
	).execute()

	if response and ( 'messages' in response ):
		past_email_ids = access_config(
			name = 'past_email_ids'
		)
		return [
			email_info['id']
			for email_info in response['messages']
			if email_info['id'] not in past_email_ids
		]

	return []

gmail = build('gmail', 'v1', credentials=get_gmail_creds())
time_print('Gmail ready.')
bot.loop.create_task(background())
time_print('Bot ready.')
try:
	bot.run(os.environ['discord_token'])
except KeyboardInterrupt:
	time_print('\033[91mStopping...')
except Exception as e:
	skip(e)
	pass
finally:
	sys.exit(0)
