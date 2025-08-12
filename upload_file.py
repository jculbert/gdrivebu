from __future__ import print_function
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Path to your service account key file
SERVICE_ACCOUNT_FILE = 'service_account.json'

# This scope allows full access to Drive
SCOPES = ['https://www.googleapis.com/auth/drive']

def upload_file(file_path, drive_folder_id=None):
    # Authenticate using the service account
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    service = build('drive', 'v3', credentials=creds)

    # Prepare file metadata
    file_metadata = {'name': os.path.basename(file_path)}
    if drive_folder_id:
        file_metadata['parents'] = [drive_folder_id]

    media = MediaFileUpload(file_path, resumable=True)

    # Upload the file
    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()

    print(f"File uploaded successfully, ID: {file.get('id')}")

if __name__ == '__main__':
    # Local file to upload
    local_file_path = 'test.txt'
    
    # Optional: Google Drive folder ID
    folder_id = None  # e.g. '1A2B3C4D5E6F'
    
    upload_file(local_file_path, folder_id)


