from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = [
    'https://www.googleapis.com/auth/admin.reports.usage.readonly',
    'https://www.googleapis.com/auth/admin.reports.audit.readonly'
]

SERVICE_ACCOUNT_FILE = '/path/to/service.json'

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES, subject="jordan@mashey.com")

service = build(
    'admin', 'reports_v1', credentials=credentials
)

results = service.userUsageReport().get(
    userKey='all', date='2020-11-01', parameters='gmail:timestamp_last_interaction',
    maxResults=50
).execute()

print(results)
