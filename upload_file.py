from __future__ import print_function
import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle,sys

# --- SETTINGS ---
TOKEN_PICKLE = '/run/secrets/token.pickle'
FOLDER_ID = '1oeDSh7rIYd00eS4TvkuTQoru52MpqxyB'

# If modifying these scopes, delete the file token.pickle
SCOPES = ['https://www.googleapis.com/auth/drive.file']

def authenticate():
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request

    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                TOKEN, SCOPES,
                redirect_uri='urn:ietf:wg:oauth:2.0:oob'
            )

            auth_url, _ = flow.authorization_url(prompt='consent')
            print("Please go to this URL and authorize this app:")
            print(auth_url)

            code = input("Enter the authorization code here: ")

            flow.fetch_token(code=code)
            creds = flow.credentials

        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return creds

def upload_file(file_path):
    #creds = authenticate()
    with open(TOKEN_PICKLE, 'rb') as token:
        creds = pickle.load(token)
    service = build('drive', 'v3', credentials=creds)

    file_metadata = {
        'name': os.path.basename(file_path),
        'parents': [FOLDER_ID]
    }
    media = MediaFileUpload(file_path, resumable=True)

    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()

    print(f"Uploaded file ID: {file.get('id')}")

if __name__ == '__main__':
    upload_file(sys.argv[1])
