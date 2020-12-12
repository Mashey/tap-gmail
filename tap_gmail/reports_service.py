from google.oauth2 import service_account
from googleapiclient.discovery import build
from google.auth.transport.requests import AuthorizedSession
import json
import os

SERVICE_ACCOUNT_FILE = os.getenv("ADMIN_SDK_KEY")
SERVICE_ACCOUNT_FILE_JSON = json.loads(SERVICE_ACCOUNT_FILE)

SCOPES = [
    'https://www.googleapis.com/auth/admin.reports.usage.readonly',
    'https://www.googleapis.com/auth/admin.reports.audit.readonly'
]

credentials = service_account.Credentials.from_service_account_info(
    SERVICE_ACCOUNT_FILE_JSON, scopes=SCOPES, subject="jordan@mashey.com")


def create_service():
    return build(
        'admin',
        'reports_v1',
        credentials=credentials,
        cache_discovery=False
    )


service = create_service()
