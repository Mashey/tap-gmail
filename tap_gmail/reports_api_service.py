import requests
import json
from dotenv import load_dotenv
import os
import pprint
import singer
# from google.oauth2 import service_account
# from googleapiclient.discovery import build
# from google.auth.transport.requests import AuthorizedSession
from datetime import date, datetime, timezone, timedelta
from collections import defaultdict
from tap_gmail import *

# SCOPES = [
#     'https://www.googleapis.com/auth/admin.reports.usage.readonly',
#     'https://www.googleapis.com/auth/admin.reports.audit.readonly'
# ]

# SERVICE_ACCOUNT_FILE = './service_key.json'

# credentials = service_account.Credentials.from_service_account_file(
#     SERVICE_ACCOUNT_FILE, scopes=SCOPES, subject="jordan@mashey.com")


with open('./tap_gmail/schemas/gmail_schema.json') as json_file:
    gmail_schema = json.load(json_file)


# def create_service():
#     return build('admin', 'reports_v1', credentials=credentials)


# service = create_service()


# def create_timestamp():
#     return datetime.now(timezone.utc).isoformat()


# def find_previous_week():
#     previous_week = date.today() - timedelta(days=9)

#     return previous_week.isoformat()


# def find_latest_data():
#     two_days_ago = date.today() - timedelta(days=3)
#     return two_days_ago.isoformat()


previous_week = find_previous_week()
latest_data = find_latest_data()


# def create_week(start_date):
#     week = []
#     week.append(start_date)
#     current_date = start_date

#     while len(week) < 7:
#         new_date = date.fromisoformat(current_date) + timedelta(days=1)
#         week.append(new_date.isoformat())
#         current_date = new_date.isoformat()

#     return week


# def get_emails(selected_date, page_token, sent_or_received):
#     request_type = None

#     if sent_or_received == 'sent':
#         request_type = 'gmail:num_emails_sent'
#     elif sent_or_received == 'received':
#         request_type = 'gmail:num_emails_received'

#     emails = service.userUsageReport().get(
#         userKey='all',
#         date=selected_date,
#         parameters=request_type,
#         filters=f'{request_type}>0',
#         maxResults=10,
#         pageToken=page_token
#     ).execute()

#     return emails


# total_weekly_active_users = defaultdict(list)


# def process_sent(date, page_token):
#     weekly_active_senders = get_emails(date, page_token, 'sent')

#     try:
#         for sender in weekly_active_senders['usageReports']:
#             total_weekly_active_users[sender['date']].append(
#                 {sender['entity']['userEmail']: sender['parameters'][0]['intValue']}
#             )
#     except KeyError:
#         return 'Only partial or no data available. Please try an earlier date.'

#     if 'nextPageToken' in weekly_active_senders:
#         process_sent(
#             date, weekly_active_senders['nextPageToken'])


# total_weekly_emails_received = defaultdict(list)


# def process_received(date, page_token):
#     weekly_emails_received = get_emails(date, page_token, 'received')

#     try:
#         for sender in weekly_emails_received['usageReports']:
#             total_weekly_emails_received[sender['date']].append(
#                 {sender['entity']['userEmail']: sender['parameters'][0]['intValue']}
#             )
#     except KeyError:
#         return 'Only partial or no data available. Please try an earlier date.'

#     if 'nextPageToken' in weekly_emails_received:
#         process_received(
#             date, weekly_emails_received['nextPageToken'])


# def total_unique_users(data):
#     user_list = []

#     for date in data:
#         users = list(data[date])
#         for user in users:
#             user = list(user.keys())[0]
#             user_list.append(user)

#     user_set = set(user_list)
#     return len(user_set)


# def create_json_response(set_start_date, set_end_date, set_total):
#     now = create_timestamp()

#     response = {
#         'timestamp': now,
#         'start_date': set_start_date,
#         'end_date': set_end_date,
#         'total': set_total
#     }

#     return response


# def total_emails_count(data):
#     total_emails = 0

#     for date in data:
#         users = list(data[date])
#         for user in users:
#             emails = list(user.values())[0]
#             emails_int = int(emails)
#             total_emails += emails_int

#     return total_emails


def find_weekly_active_users(selected_date=previous_week, page_token=None):
    week = create_week(selected_date)
    start_date = week[0]
    end_date = week[-1]

    for date in week:
        process_sent(date, page_token)

    total = total_unique_users(total_weekly_active_users)
    json_response = create_json_response(start_date, end_date, total)

    # singer.write_schema('gmail', gmail_schema, 'timestamp')
    # singer.write_records('gmail', json_response)

    return json_response


def find_weekly_emails_sent(selected_date=previous_week, page_token=None):
    week = create_week(selected_date)
    start_date = week[0]
    end_date = week[-1]

    total = total_emails_count(total_weekly_active_users)
    json_response = create_json_response(start_date, end_date, total)

    # singer.write_schema('gmail', gmail_schema, 'timestamp')
    # singer.write_records('gmail', json_response)

    return json_response


def find_weekly_emails_recieved(selected_date=previous_week, page_token=None):
    week = create_week(selected_date)
    start_date = week[0]
    end_date = week[-1]

    for date in week:
        process_received(date, page_token)

    total = total_emails_count(total_weekly_emails_received)
    json_response = create_json_response(start_date, end_date, total)

    # singer.write_schema('gmail', gmail_schema, 'timestamp')
    # singer.write_records('gmail', json_response)

    return json_response


# total_daily_senders = defaultdict(list)


def find_daily_active_users(selected_date=latest_data, page_token=None):
    daily_active_senders = get_emails(selected_date, page_token, 'sent')
    start_date = selected_date
    end_date = selected_date

    try:
        for sender in daily_active_senders['usageReports']:
            total_daily_senders[sender['date']].append(
                {sender['entity']['userEmail']
                    : sender['parameters'][0]['intValue']}
            )
    except KeyError:
        return 'Only partial or no data available. Please try an earlier date.'

    if 'nextPageToken' in daily_active_senders:
        find_daily_active_users(
            selected_date, daily_active_senders['nextPageToken'])

    total = len(total_daily_senders[selected_date])
    json_response = create_json_response(start_date, end_date, total)

    # singer.write_schema('gmail', gmail_schema, 'timestamp')
    # singer.write_records('gmail', json_response)

    return json_response


def find_daily_emails_sent(selected_date=latest_data, page_token=None):
    week = create_week(selected_date)
    start_date = week[0]
    end_date = week[-1]

    total = total_emails_count(total_daily_senders)
    json_response = create_json_response(start_date, end_date, total)

    # singer.write_schema('gmail', gmail_schema, 'timestamp')
    # singer.write_records('gmail', json_response)

    return json_response


# total_daily_emails_received = defaultdict(list)


def find_daily_emails_received(selected_date=latest_data, page_token=None):
    daily_emails_received = get_emails(selected_date, page_token, 'received')
    start_date = selected_date
    end_date = selected_date

    try:
        for sender in daily_emails_received['usageReports']:
            total_daily_emails_received[sender['date']].append(
                {sender['entity']['userEmail']
                    : sender['parameters'][0]['intValue']}
            )
    except KeyError:
        return 'Only partial or no data available. Please try an earlier date.'

    if 'nextPageToken' in daily_emails_received:
        find_daily_emails_received(
            selected_date, daily_emails_received['nextPageToken'])

    total = total_emails_count(total_daily_emails_received)
    json_response = create_json_response(start_date, end_date, total)

    # singer.write_schema('gmail', gmail_schema, 'timestamp')
    # singer.write_records('gmail', json_response)

    return json_response


find_weekly_active_users()
find_weekly_emails_sent()
find_weekly_emails_recieved()
# find_daily_active_users()
# find_daily_emails_sent()
# find_daily_emails_received()
