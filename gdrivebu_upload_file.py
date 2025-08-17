#!/bin/python3
from __future__ import print_function
import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle,sys

# --- SETTINGS ---
TOKEN_PICKLE = '/tmp/token.pickle'
ROOT_FOLDER_ID = '1oeDSh7rIYd00eS4TvkuTQoru52MpqxyB'

def list_subfolders(service, parent_id):
    query = (
        f"'{parent_id}' in parents "
        f"and mimeType = 'application/vnd.google-apps.folder' "
        f"and trashed = false"
    )

    results = service.files().list(
        q=query,
        spaces='drive',
        fields='files(id, name)',
        pageSize=100
    ).execute()

    for f in results.get('files', []):
        print(f"Found subfolder: {f['name']} (ID: {f['id']})")

def get_subfolder_id(service, parent_id, subfolder_name):
    """
    Returns the ID of a subfolder given its name and the parent folder ID.
    If multiple matches are found, returns the first one.
    Returns None if not found.
    """
    query = (
        f"'{parent_id}' in parents "
        f"and mimeType = 'application/vnd.google-apps.folder' "
        f"and name = '{subfolder_name}' "
        f"and trashed = false"
    )

    results = service.files().list(
        q=query,
        spaces='drive',
        fields='files(id, name)',
        pageSize=10
    ).execute()

    files = results.get('files', [])
    if not files:
        return None
    return files[0]['id']

def upload_file(service, file_path, folder_id):

    file_metadata = {
        'name': os.path.basename(file_path),
        'parents': [folder_id]
    }
    media = MediaFileUpload(file_path, resumable=True)

    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()

    print(f"Uploaded file ID: {file.get('id')}")

if __name__ == '__main__':
    with open(TOKEN_PICKLE, 'rb') as token:
        creds = pickle.load(token)
    service = build('drive', 'v3', credentials=creds)

    if len(sys.argv) > 2:
        folder_id = get_subfolder_id(service, ROOT_FOLDER_ID, sys.argv[2])
        if folder_id:
            print(f"Folder ID: {folder_id}")
        else:
            print(f"Sub folder {sys.argv[2]} not found")
            exit
    else:
        folder_id = ROOT_FOLDER_ID

    upload_file(service, sys.argv[1], folder_id)
