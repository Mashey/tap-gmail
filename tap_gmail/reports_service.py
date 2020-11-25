from google.oauth2 import service_account
from googleapiclient.discovery import build
from google.auth.transport.requests import AuthorizedSession
from google.cloud import secretmanager
import json


def access_secret_version(project_id, secret_id, version_id):
    # Create the Secret Manager client.
    secret_client = secretmanager.SecretManagerServiceClient()

    # Build the resource name of the secret version.
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"

    # Access the secret version.
    response = secret_client.access_secret_version(request={"name": name})
    data = json.loads(response.payload.data)

    return data


SERVICE_ACCOUNT_FILE = access_secret_version('102430623331', 'service_key', 1)

SCOPES = [
    'https://www.googleapis.com/auth/admin.reports.usage.readonly',
    'https://www.googleapis.com/auth/admin.reports.audit.readonly'
]

credentials = service_account.Credentials.from_service_account_info(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES, subject="jordan@mashey.com")


def create_service():
    return build(
        'admin',
        'reports_v1',
        credentials=credentials,
        cache_discovery=False
    )


service = create_service()
