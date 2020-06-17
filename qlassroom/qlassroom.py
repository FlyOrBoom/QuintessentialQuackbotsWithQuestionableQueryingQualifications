from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import base64
import quopri
import html
import re

import os,asyncio,json,discord
from dotenv import load_dotenv
load_dotenv()

bot = discord.Client()
email_record_file = open('email_record.txt')
email_record = email_record_file.read().split(',')
email_record_file.close()

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
	await bot.wait_until_ready()
	print(f'\033[92mLogged in as {str(bot.user)}.')
	while True:
		print('\033[94mChecking for new emails...')
		emails = get_emails()
		print(len(emails),'new emails.')
		for email in emails:

			full = str(
				quopri.decodestring(
					base64.urlsafe_b64decode(
						email['raw'].encode('ASCII')
					)
				)
			)

			email_subject = 'hello'

			subject = re.search(
				r'Subject:(.*?)\\r',
				full
			).group(1)
			
			cut = re.search(
				r'text\/plain.*?,.{4}(.*?).{4}OPEN',
				full
			).group(1).split(
				r'\r\n'
			)

			print(cut)
			teacher = cut[0].split(' posted ')[0]
			classname = cut[0].split(' in ')[1][:-0]
			url = cut[1][1:-2]
			duedate = 'duedate'
			comment = ' '.join(cut[4:])
			
			print(teacher,classname,duedate,comment)
			
			embed = discord.Embed(
				color = 0x11aa77,
				title = '📪 '+subject,
				description = f'{comment}\n**({duedate})**',
				url = url
			).set_author(
				name = classname
			).set_footer(
				text = teacher
			)
			channels = (
				bot.get_channel(int(channel_id))
				for channel_id
				in os.environ['CHANNEL_IDS'].split(',')
			)
			for channel in channels:
				print(f'🎉 \033[95mSent\033[0m {email["snippet"]} \033[95mto\033[0m {channel.id}')
				await channel.send(embed=embed)

			email_record.append(email['id'])

		email_record_file = open('email_record.txt','w')
		email_record_file.write(','.join(email_record))
		email_record_file.close()

		await asyncio.sleep(60)

def get_emails():
	# Call the Gmail API
	response = gmail.users().messages().list(
		userId='me',
		q='label:Qlassroom newer_than:1d'
	).execute()

	# Filter out old messages	
	global email_record
	email_ids = list(filter(
		lambda email_id: email_id not in email_record,
		list( email_info['id'] for email_info in response['messages'] )
	))

	# Return full emails
	emails = list(
		gmail.users().messages().get(
			userId='me',
			id=email_id,
			format='raw'
		).execute() for email_id in email_ids
	)	
	
	return emails

gmail = build('gmail', 'v1', credentials=get_gmail_creds())
bot.loop.create_task(handle_emails())
bot.run(os.environ['TOKEN'])
