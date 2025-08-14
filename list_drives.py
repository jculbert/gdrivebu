from googleapiclient.discovery import build
from google.oauth2 import service_account

SERVICE_ACCOUNT_FILE = '/run/secrets/google_service_account.json'
SCOPES = ['https://www.googleapis.com/auth/drive']

creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE,
    scopes=SCOPES
)
service = build('drive', 'v3', credentials=creds)

# List all Shared Drives the service account can access
results = service.drives().list(pageSize=10).execute()
drives = results.get('drives', [])

if not drives:
    print('No Shared Drives found. Make sure the service account is added to one.')
else:
    for d in drives:
        print(f"Name: {d['name']}, ID: {d['id']}")
