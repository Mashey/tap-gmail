from google.oauth2 import service_account
from googleapiclient.discovery import build
from google.auth.transport.requests import AuthorizedSession
from datetime import date, datetime, timezone, timedelta


today = date.today().isoformat()

def find_previous_week():
    previous_week = datetime.now() - timedelta(days=7)
    return previous_week.isoformat() + "Z"


previous_week = find_previous_week()

SCOPES = [
    'https://www.googleapis.com/auth/admin.reports.usage.readonly',
    'https://www.googleapis.com/auth/admin.reports.audit.readonly'
]

SERVICE_ACCOUNT_FILE = './service_key.json'

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES, subject="jordan@mashey.com")

service = build(
    'admin', 'reports_v1', credentials=credentials
)

def find_weekly_active_senders():
    weekly_active_senders = service.userUsageReport().get(
        userKey='all',
        date=today,
        parameters='gmail:num_emails_sent',
        maxResults=10
    ).execute()

    return len(weekly_active_senders['usageReports'])


def find_weekly_emails_sent():
    weekly_emails_sent = service.userUsageReport().get(
        userKey='all',
        date=today,
        parameters='gmail:num_emails_sent',
        filters=f'gmail:num_emails_sent>{previous_week}',
        maxResults=10
    ).execute()

    return len(weekly_emails_sent['usageReports'])


def find_weekly_emails_recieved():
    weekly_emails_recieved = service.userUsageReport().get(
        userKey='all',
        date=today,
        parameters='gmail:num_emails_recieved',
        filters=f'gmail:num_emails_recieved>{previous_week}',
        maxResults=10
    ).execute()

    return len(weekly_emails_recieved['usageReports'])

def find_daily_active_senders():
    daily_active_senders = service.userUsageReport().get(
        userKey='all',
        date=today,
        parameters='gmail:num_emails_sent',
        maxResults=10
    ).execute()

    return len(daily_active_senders['usageReports'])


def find_daily_emails_sent():
    daily_emails_sent = service.userUsageReport().get(
        userKey='all',
        date=today,
        parameters='gmail:num_emails_sent',
        maxResults=10
    ).execute()

    return len(daily_emails_sent['usageReports'])

def find_daily_emails_recieved():
    daily_emails_recieved = service.userUsageReport().get(
        userKey='all',
        date=today,
        parameters='gmail:num_emails_recieved',
        maxResults=10
    ).execute()

    return len(daily_emails_recieved['usageReports'])


# authed_session = AuthorizedSession(credentials)

# response = authed_session.get(
#     "https://www.googleapis.com/admin/reports/v1/usage/users/all/dates/2013-03-03")

print(weekly_emails_sent)
