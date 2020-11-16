from google.oauth2 import service_account
from googleapiclient.discovery import build
from google.auth.transport.requests import AuthorizedSession
from datetime import date, datetime, timezone, timedelta
from collections import defaultdict


today = date.today().isoformat()

def find_previous_week():
    previous_week = date.today() - timedelta(days=7)
    return previous_week.isoformat()


def find_next_day():
    next_day = date.today() + timedelta(days=1)
    return next_day.isoformat()


def find_previous_day():
    previous_day = date.today() - timedelta(days=1)
    return previous_day.isoformat()


previous_week = find_previous_week()
next_day = find_next_day()
previous_day = find_previous_day()

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

total_active_weekly_senders = {
    f'{previous_week}_to_{today}': 0
}

def find_weekly_active_senders(page_token=None):
    weekly_active_senders = service.userUsageReport().get(
        userKey='all',
        date=f'{previous_week}',
        parameters='gmail:num_emails_sent',
        filters='gmail:num_emails_sent>0',
        maxResults=10,
        pageToken=page_token
    ).execute()

    total_active_weekly_senders[f'{previous_week}_to_{today}'] += len(
        weekly_active_senders['usageReports']
    )

    if 'nextPageToken' in weekly_active_senders:
        find_weekly_active_senders(weekly_active_senders['nextPageToken'])
    else:
        return total_active_weekly_senders


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


total_daily_senders = defaultdict(list)

def find_daily_active_senders(selected_date=today, page_token=None):
    daily_active_senders = service.userUsageReport().get(
        userKey='all',
        date='2020-11-13',
        parameters='gmail:num_emails_sent',
        filters='gmail:num_emails_sent>0',
        maxResults=10,
        pageToken=page_token
    ).execute()

    for sender in daily_active_senders['usageReports']:
        total_daily_senders[sender['date']].append({sender['entity']['userEmail']: sender['parameters'][0]['intValue']})

    if 'nextPageToken' in daily_active_senders:
        find_daily_active_senders(daily_active_senders['nextPageToken'])

    return len(total_daily_senders['today'])


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

find_daily_active_senders()

break_point = 'Testing break point'
