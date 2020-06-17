import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import base64
import re
import datetime

import os,asyncio,json,discord
from dotenv import load_dotenv
load_dotenv()

bot = discord.Client()
email_record_file = open('email_record.txt')
email_record = email_record_file.read().split(',')
email_record_file.close()

def time():
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
				'credentials.json', SCOPES)
			creds = flow.run_local_server(port=0)
		# Save the credentials for the next run
		with open('token.pickle', 'wb') as token:
			pickle.dump(creds, token)
	return creds


async def handle_emails():
	global email_record
	await bot.wait_until_ready()
	print(
		time(),
		'\033[92m',
		f'Logged in as {str(bot.user)}'
	)
	while True:
		print(
			time(),
			'\033[94m',
			'Checking for new emails...',
			end=''
		)
		emails = get_emails()
		print(
			'\033[93m',
			len(emails)
		)
		for email in emails:

			content = re.search(
				r'([\w ]+) posted a (\w+ \w+) in ([\w ]+)\n.*\n\n.*\n(?:Due: (.*?)\n(.*)\n)?((?:.|\n)*)\nOPEN(?: |\n)<(.*?)>\n.*\n',
				str(
					base64.urlsafe_b64decode(
						email['payload']['parts'][0]['body']['data']
					).decode('utf-8')
				).replace('\r','')
			).groups()

			post = {
				'teacher': content[0],
				'type':	content[1].capitalize(),
				'class': content[2],
				'due': content[3],
				'document': content[4],
				'description': content[5].replace('\n',' '),
				'url': content[6]
			}

			embed = discord.Embed(
				color = 0x11aa77,
				title = f'📪 '+post['type']+(': '+post['document'] if post['document'] else ''),
				description = post['description'],
				url = post['url']
			).set_author(
				name = post['class']
			).set_footer(
				text = post['teacher']
			)

			if post['due']:
				embed.add_field(
					name = 'Due',
					value = post['due'],
					inline = False
				)

			channels = (
				bot.get_channel(int(channel_id))
				for channel_id
				in os.environ['CHANNEL_IDS'].split(',')
			)
			for channel in channels:
				print(
					time(),
					'\033[95m',
					'🎉 Sent',
					'\033[0m',
					email['id'],
					'\033[95m',
					'to'
					'\033[0m',
					channel.id
				)
				await channel.send(embed=embed)

			email_record.append(email['id'])

		email_record_file = open('email_record.txt','w')
		email_record_file.write(','.join(email_record))
		email_record_file.close()

		await asyncio.sleep(300)

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
			format='full'
		).execute() for email_id in email_ids
	)	
	
	return emails

gmail = build('gmail', 'v1', credentials=get_gmail_creds())
bot.loop.create_task(handle_emails())
bot.run(os.environ['TOKEN'])
