import os
import pickle

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

def load(paths):
	return build('gmail', 'v1', credentials=load_credentials(paths))
def load_credentials(paths):

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
				paths['gmail']['credentials'], SCOPES)
			creds = flow.run_local_server(port=0)
		# Save the credentials for the next run
		with open(path, 'wb') as token:
			pickle.dump(creds, token)
	return creds

