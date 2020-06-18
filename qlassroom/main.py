import pickle
import json

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import base64
import re
import datetime
import random

import os
import asyncio
import json
import discord

from dotenv import load_dotenv
load_dotenv()

bot = discord.Client()
email_record_file = open('email_record.txt')
email_record = email_record_file.read().split(',')
email_record_file.close()

wait_duration = 60
email_query = 'newer_than:1d'

async def color_of(thing):
	return ''.join(
		map(
			lambda x:f'\033[38:5:{x}m▮',
			re.findall(
				'..',
				str(thing)
			)
		)
	)

async def print_error(error):
	print(f'\033[91m{error}\033[0m')

async def time():
	return f'\033[95m{str(datetime.datetime.now()).split(" ")[1].split(".")[0]}:\033[0m'
	
def get_gmail_creds():

	# If modifying these scopes, delete the file token.pickle.
	SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
		
	creds = None
	
	# The file token.pickle stores the user's access and refresh tokens, and is
	# created automatically when the authorization flow completes for the first
	# time.
	if os.path.exists('token.pickle'):
		with open('token.pickle', 'rb') as token:
			creds = pickle.load(token)
	# If there are no (valid) credentials available, let the user log in.
	if not creds or not creds.valid:
		if creds and creds.expired and creds.refresh_token:
			creds.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file(
				'gmail-credentials.json', SCOPES)
			creds = flow.run_local_server(port=0)
		# Save the credentials for the next run
		with open('token.pickle', 'wb') as token:
			pickle.dump(creds, token)
	return creds


async def handle_emails(email_record):

	await bot.wait_until_ready()
	print(
		await time(),
		'\033[92m',
		f'Logged in as {str(bot.user)}'
	)
	
	while True:

		print(
			await time(),
			'\033[94m',
			'Checking for new emails...',
			end=''
		)

		channel_ids = await fetch_channel_ids()

		email_ids = await fetch_email_ids(
		)

		print(
			'\033[93m',
			len(email_ids)
		)

		if email_ids:

			email_record.extend(email_ids)
	
			await sends(
				await channels_from(
					channel_ids
				),
				await embeds_from(
					await emails_from(
						email_ids
			)	)	)

			email_record_file = open('email_record.txt','w')
			email_record_file.write(','.join(email_record))
			email_record_file.close()

		await asyncio.sleep(wait_duration)

async def sends(channels,embeds):

	return await asyncio.gather(*[
		asyncio.gather(*[
			send(channel,embed)
			for channel
			in channels
		])
		for embed
		in embeds
	])

async def send(channel,embed):

	if not embed:
		print_error('Embed not sent!')
		return
	embedhash = random.seed(str(embed)[-14:])
	print(
		await time(),
		'\033[95m',
		'🎉 Sent',
		await color_of(random.randint(1e16,1e17-1)),
		'\033[95m'+
		'to',
		await color_of(channel.id)
	)
	return await channel.send(embed=embed)

async def channels_from(channel_ids):
	return await asyncio.gather(*[
		channel_from(channel_id)
		for channel_id
		in channel_ids
	])

async def channel_from(channel_id):

	try:
		return bot.get_channel(int(channel_id))
	except:
		print_error(f'Channel {channel_id} not found! Skipping...')
		return False

async def fetch_channel_ids():

	return os.environ['CHANNEL_IDS'].split(',')

async def embeds_from(emails):

	return await asyncio.gather(*[
		embed_from(email)
		for email
		in emails
	])

async def embed_from(email):

	try:
		with 
		matches = re.search(
			base64.urlsafe_b64decode(
				email['payload']['parts'][0]['body']['data']
			).decode('utf-8').replace('\r','')
		).groups()
	except AttributeError:
		print_error('Email does not match with regex! Skipping...')

	post = {
		'teacher': matches[0],
		'type':	matches[1].capitalize(),
		'class': matches[2],
		'due': matches[3],
		'class_url': matches[4],
		'document': matches[5],
		'description': matches[6].replace('\n',' '),
		'url': matches[7]
	}

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

	if not embed:
		print_error('Failed to create embed!')
		return False

	if post['due']:
		embed.add_field(
			name = 'Due',
			value = post['due'],
			inline = False
		)

	return embed

async def emails_from(email_ids):
	return await asyncio.gather(*[
		email_from(email_id)
		for email_id
		in email_ids
	])
	
async def email_from(email_id):
	return gmail.users().messages().get(
		userId='me',
		id=email_id
	).execute()

async def fetch_email_ids():
	# Call the Gmail API
	response = gmail.users().messages().list(
		userId='me',
		q = email_query
	).execute()

	if response and ( 'messages' in response ):
		return list(filter(
			lambda email_id: email_id not in email_record,
			list( email_info['id'] for email_info in response['messages'] )
		))
	
	return []

gmail = build('gmail', 'v1', credentials=get_gmail_creds())
bot.loop.create_task(handle_emails(email_record))
bot.run(os.environ['discord_token'])
