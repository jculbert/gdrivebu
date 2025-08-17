from __future__ import print_function
import os
import pickle
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

#SCOPES = ['https://www.googleapis.com/auth/drive.file']
#SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly', 'https://www.googleapis.com/auth/drive.file']
SCOPES = ['https://www.googleapis.com/auth/drive']
TOKEN = '/tmp/google_drive_api_client_secret.json'

def authenticate():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # This will open your browser
            flow = InstalledAppFlow.from_client_secrets_file(
                TOKEN, SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return creds

if __name__ == '__main__':
    authenticate()
    print("✅ Token generated and saved as token.pickle")
