import requests
import json
from collections import defaultdict
from datetime import date, datetime, timezone, timedelta
from tap_gmail.reports_service import *


total_weekly_active_users = defaultdict(list)
total_weekly_emails_received = defaultdict(list)
total_daily_senders = defaultdict(list)
total_daily_emails_received = defaultdict(list)


def create_timestamp():
    return datetime.now(timezone.utc).isoformat()


def find_previous_week():
    previous_week = date.today() - timedelta(days=9)

    return previous_week.isoformat()


def find_latest_data():
    two_days_ago = date.today() - timedelta(days=3)
    return two_days_ago.isoformat()


def create_week(start_date):
    week = []
    week.append(start_date)
    current_date = start_date

    while len(week) < 7:
        new_date = date.fromisoformat(current_date) + timedelta(days=1)
        week.append(new_date.isoformat())
        current_date = new_date.isoformat()

    return week


def get_emails(selected_date, page_token, sent_or_received):
    request_type = None

    if sent_or_received == 'sent':
        request_type = 'gmail:num_emails_sent'
    elif sent_or_received == 'received':
        request_type = 'gmail:num_emails_received'

    emails = service.userUsageReport().get(
        userKey='all',
        date=selected_date,
        parameters=request_type,
        filters=f'{request_type}>0',
        maxResults=100,
        pageToken=page_token
    ).execute()

    return emails


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


def process_received(date, page_token):
    weekly_emails_received = get_emails(date, page_token, 'received')

    try:
        for sender in weekly_emails_received['usageReports']:
            total_weekly_emails_received[sender['date']].append(
                {sender['entity']['userEmail']: sender['parameters'][0]['intValue']}
            )
    except KeyError:
        return 'Only partial or no data available. Please try an earlier date.'

    if 'nextPageToken' in weekly_emails_received:
        process_received(
            date, weekly_emails_received['nextPageToken'])


def total_unique_users(data):
    user_list = []

    for date in data:
        users = list(data[date])
        for user in users:
            user = list(user.keys())[0]
            user_list.append(user)

    user_set = set(user_list)
    return len(user_set)


def create_json_response(set_start_date, set_end_date, set_total, set_query):
    now = create_timestamp()

    response = {
        'timestamp': now,
        'query_type': set_query,
        'start_date': set_start_date,
        'end_date': set_end_date,
        'total': set_total
    }
    return [response]


def total_emails_count(data):
    total_emails = 0

    for date in data:
        users = list(data[date])
        for user in users:
            emails = list(user.values())[0]
            emails_int = int(emails)
            total_emails += emails_int

    return total_emails

