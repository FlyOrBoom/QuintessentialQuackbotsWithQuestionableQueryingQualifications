import os
import pickle
import httplib2
from googleapiclient.discovery import build
from prefixes import *
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import asyncio
import cache
import socket,ssl
import config
import sys

def load_client(paths):
	return build('gmail', 'v1', credentials=load_credentials(paths))

def load_credentials(paths):

	# If modifying these scopes, delete the file token.pickle.
	SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
		
	creds = None
	
	# The file token.pickle stores the user's access and refresh tokens, and is
	# created automatically when the authorization flow completes for the first
	# time.
	
	path = paths['token']
	if os.path.exists(path):
		with open(path, 'rb') as token:
			creds = pickle.load(token)
	# If there are no (valid) credentials available, let the user log in.
	if not creds or not creds.valid:
		if creds and creds.expired and creds.refresh_token:
			creds.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file(
				paths['credentials'], SCOPES)
			creds = flow.run_local_server(port=0)
		# Save the credentials for the next run
		with open(path, 'wb') as token:
			pickle.dump(creds, token)
	return creds


def fetch_email_ids():

	# Call the gmail API

	try:
		response = gmail_client.users().messages().list(
			userId = 'me',
			q = config.read('email query')
		).execute()
	except socket.timeout or ssl.SSLCertificationError:
		print(time(),error,'Network Error: Unable to fetch email IDs.')
		return set()

	# Subtract discord_clienth sets from each other

	received_ids = set()

	if response and ( 'messages' in response ):
		received_ids = {
			email_info['id']
			for email_info in response['messages']
		}
	
	past_ids = cache.read()
	cache.write(past_ids.intersection(received_ids))
	return received_ids - past_ids

def fetch_email(email_id):
	return gmail_client.users().messages().get(
		userId='me',
		id=email_id
	).execute()

try:
	gmail_client = load_client({
		'token':'gmail/token.pickle',
		'credentials':'gmail/credentials.json'
	})
except httplib2.HttpLib2Error:
	print(time(),error,f'Network Error: Unable to start Gmail.')
	sys.exit(0)
print(time(),'Gmail ready.')

