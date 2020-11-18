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


def find_previous_week():
    previous_week = date.today() - timedelta(days=9)

    return previous_week.isoformat()


def find_latest_data():
    two_days_ago = date.today() - timedelta(days=3)
    return two_days_ago.isoformat()


previous_week = find_previous_week()
latest_data = find_latest_data()


def create_week(start_date):
    week = []
    week.append(start_date)
    current_date = start_date

    while len(week) < 7:
        new_date = date.fromisoformat(current_date) + timedelta(days=1)
        week.append(new_date.isoformat())
        current_date = new_date.isoformat()

    return week


def get_emails(selected_date, page_token, sent_or_recieved):
    request_type = None

    if sent_or_recieved == 'sent':
        request_type = 'gmail:num_emails_sent'
    elif sent_or_recieved == 'recieved':
        request_type = 'gmail:num_emails_recieved'

    emails = service.userUsageReport().get(
        userKey='all',
        date=selected_date,
        parameters=request_type,
        filters=f'{request_type}>0',
        maxResults=10,
        pageToken=page_token
    ).execute()

    return emails


total_weekly_active_users = defaultdict(list)


def process_sent(date, page_token):
    weekly_active_senders = get_emails(date, page_token, 'sent')

    try:
        for sender in weekly_active_senders['usageReports']:
            total_weekly_active_users[sender['date']].append(
                {sender['entity']['userEmail']: sender['parameters'][0]['intValue']}
            )
    except KeyError:
        return 'Only partial or no data available. Please try an earlier date.'

    if 'nextPageToken' in weekly_active_senders:
        process_sent(
            date, weekly_active_senders['nextPageToken'])


total_weekly_emails_recieved = defaultdict(list)


def process_recieved(date, page_token):
    weekly_emails_recieved = get_emails(date, page_token, 'recieved')

    try:
        for sender in weekly_emails_recieved['usageReports']:
            total_weekly_emails_recieved[sender['date']].append(
                {sender['entity']['userEmail']: sender['parameters'][0]['intValue']}
            )
    except KeyError:
        return 'Only partial or no data available. Please try an earlier date.'

    if 'nextPageToken' in weekly_emails_recieved:
        process_recieved(
            date, weekly_emails_recieved['nextPageToken'])


def unqiue_users(data):
    user_list = []

    for date in data:
        users = list(data[date])
        for user in users:
            user = list(user.keys())[0]
            user_list.append(user)

    user_set = set(user_list)
    return len(user_set)


def find_weekly_active_users(selected_date=previous_week, page_token=None):
    week = create_week(selected_date)

    for date in week:
        process_sent(date, page_token)

    total = unqiue_users(total_weekly_active_users)
    return total


def count_emails(data):
    total_emails = 0

    for date in data:
        users = list(data[date])
        for user in users:
            emails = list(user.values())[0]
            emails_int = int(emails)
            total_emails += emails_int

    return total_emails


def find_weekly_emails_sent(selected_date=previous_week, page_token=None):
    week = create_week(selected_date)

    total = count_emails(total_weekly_active_users)
    return total


def find_weekly_emails_recieved(selected_date=previous_week, page_token=None):
    week = create_week(selected_date)

    for date in week:
        process_recieved(date, page_token)

    total = count_emails(total_weekly_emails_recieved)
    return total


total_daily_senders = defaultdict(list)


def find_daily_active_senders(selected_date=latest_data, page_token=None):
    daily_active_senders = get_emails(selected_date, page_token, 'sent')

    try:
        for sender in daily_active_senders['usageReports']:
            total_daily_senders[sender['date']].append(
                {sender['entity']['userEmail']
                    : sender['parameters'][0]['intValue']}
            )
    except KeyError:
        return 'Only partial or no data available. Please try an earlier date.'

    if 'nextPageToken' in daily_active_senders:
        find_daily_active_senders(
            selected_date, daily_active_senders['nextPageToken'])

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


find_weekly_active_users()
find_weekly_emails_sent()

break_point = 'Testing break point'
