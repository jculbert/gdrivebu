from __future__ import print_function
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Path to your service account key file
SERVICE_ACCOUNT_FILE = '/run/secrets/google_service_account.json'
#DRIVE_ID = '1u1OHSEWIaAIpsKzTS4czPmRyihJub1CO'
DRIVE_ID = '1JVK40rwydVduYnfQfZQonls24V9KLYw_'

# This scope allows full access to Drive
SCOPES = ['https://www.googleapis.com/auth/drive']

def upload_file_old(file_path, drive_folder_id=None):
    # Authenticate using the service account
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    service = build('drive', 'v3', credentials=creds)

    # Prepare file metadata
    file_metadata = {'name': os.path.basename(file_path)}
    #if drive_folder_id:
        #file_metadata['parents'] = [drive_folder_id]
    file_metadata['parents'] = DRIVE_ID

    media = MediaFileUpload(file_path, resumable=True)

    # Upload the file
    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id',
        supportsAllDrives=True
    ).execute()

    print(f"File uploaded successfully, ID: {file.get('id')}")

def upload_file(file_path, drive_folder_id=None):
    from googleapiclient.discovery import build
    from google.oauth2 import service_account

    # Authenticate with service account
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=['https://www.googleapis.com/auth/drive']
    )

    service = build('drive', 'v3', credentials=creds)

    # File metadata
    file_metadata = {
        'name': 'jeff.txt',           # Name in Drive
        'parents': [DRIVE_ID],        # Required for Shared Drive root
    #    'driveId': DRIVE_ID           # Explicitly specify Shared Drive
    }

    # Upload media
    from googleapiclient.http import MediaFileUpload
    media = MediaFileUpload(file_path, mimetype='text/plain')

    # Create file
    file = service.files().create(
        body=file_metadata,
        media_body=media,
        supportsAllDrives=True
    ).execute()

    print(f"File ID: {file.get('id')}")

if __name__ == '__main__':
    # Local file to upload
    local_file_path = 'jeff.txt'
    
    # Optional: Google Drive folder ID
    folder_id = None  # e.g. '1A2B3C4D5E6F'
    
    upload_file(local_file_path, folder_id)


