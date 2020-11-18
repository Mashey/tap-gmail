from google.oauth2 import service_account
from googleapiclient.discovery import build
from google.auth.transport.requests import AuthorizedSession
from datetime import date, datetime, timezone, timedelta
from collections import defaultdict


SCOPES = [
    'https://www.googleapis.com/auth/admin.reports.usage.readonly',
    'https://www.googleapis.com/auth/admin.reports.audit.readonly'
]

SERVICE_ACCOUNT_FILE = './service_key.json'

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES, subject="jordan@mashey.com")


def create_service():
    return build('admin', 'reports_v1', credentials=credentials)


service = create_service()
today = date.today().isoformat()

def find_previous_week():
    previous_week = date.today() - timedelta(days=9)

    return previous_week.isoformat()


def find_latest_data():
    two_days_ago = date.today() - timedelta(days=3)
    return two_days_ago.isoformat()


def find_next_day(selected_date=None):
    if selected_date == None:
        next_day = date.today() + timedelta(days=1)
        return next_day.isoformat()
    else:
        user_next_day = date.fromisoformat(selected_date) + timedelta(days=1)
        return user_next_day.isoformat()


def create_week(start_date):
    week = []
    week.append(start_date)
    current_date = start_date

    while len(week) < 7:
        new_date = date.fromisoformat(current_date) + timedelta(days=1)
        week.append(new_date.isoformat())
        current_date = new_date.isoformat()
    
    return week

previous_week = find_previous_week()
latest_data = find_latest_data()

def get_emails_sent(selected_date, page_token):
    emails_sent = service.userUsageReport().get(
        userKey='all',
        date=selected_date,
        parameters='gmail:num_emails_sent',
        filters='gmail:num_emails_sent>0',
        maxResults=10,
        pageToken=page_token
    ).execute()

    return emails_sent


total_weekly_senders = defaultdict(list)

def process_week(date, page_token):
    weekly_active_senders = get_emails_sent(date, page_token)

    try:
        for sender in weekly_active_senders['usageReports']:
            total_weekly_senders[sender['date']].append(
                {sender['entity']['userEmail']: sender['parameters'][0]['intValue']}
            )
    except KeyError:
        return 'Only partial or no data available. Please try an earlier date.'

    if 'nextPageToken' in weekly_active_senders:
        process_week(date, weekly_active_senders['nextPageToken'])
    
    return weekly_active_senders


def find_weekly_active_senders(selected_date=previous_week, page_token=None):
    week = create_week(selected_date)

    for date in week:
        process_week(date, page_token)

    return len(total_weekly_senders[selected_date])


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

def find_daily_active_senders(selected_date=latest_data, page_token=None):
    daily_active_senders = get_emails_sent(selected_date, page_token)

    try:
        for sender in daily_active_senders['usageReports']:
            total_daily_senders[sender['date']].append(
                {sender['entity']['userEmail']: sender['parameters'][0]['intValue']}
            )
    except KeyError:
        return 'Only partial data available. Please try an earlier date.'

    if 'nextPageToken' in daily_active_senders:
        find_daily_active_senders(selected_date, daily_active_senders['nextPageToken'])

    return len(total_daily_senders[selected_date])


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


find_weekly_active_senders()

break_point = 'Testing break point'
