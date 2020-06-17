from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from time import sleep

import base64
import email

import os,asyncio,json,discord
from dotenv import load_dotenv
load_dotenv()

bot = discord.Client()
email_record = []

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
				'credentials.json', SCOPES)
			creds = flow.run_local_server(port=0)
		# Save the credentials for the next run
		with open('token.pickle', 'wb') as token:
			pickle.dump(creds, token)
	return creds


async def handle_emails():
	global email_record
	channels = (
		bot.get_channel(int(channel_id))
		for channel_id
		in os.environ['CHANNEL_IDS'].split(',')
	)
	await bot.wait_until_ready()
	print(f'Logged in as {str(bot.user)}.')
	while True:
		print('Checking for new emails...')
		for email in get_emails():
			message = '📪 '+email['snippet']
			print(message)
			email_record.append(email['id'])
			for channel in channels:
				await channel.send(message)
		await asyncio.sleep(60)

def get_emails():

	# Call the Gmail API
	response = gmail.users().messages().list(
		userId='me',
		q='label:Plassroom newer_than:1d'
	).execute()

	# Filter out old messages	
	global email_record
	email_ids = filter(
		lambda email_id: email_id not in email_record,
		list( email_info['id'] for email_info in response['messages'] )
	)

	# Return full emails
	return (
		gmail.users().messages().get(
			userId='me',
			id=email_id,
			format='raw'
		).execute() for email_id in email_ids
	)	
gmail = build('gmail', 'v1', credentials=get_gmail_creds())
bot.loop.create_task(handle_emails())
bot.run(os.environ['TOKEN'])
print('Logging in...')

