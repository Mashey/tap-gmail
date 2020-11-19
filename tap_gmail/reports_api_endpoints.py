import requests
import json
from dotenv import load_dotenv
import os
import pprint
import singer
from singer import Transformer
from datetime import date, datetime, timezone, timedelta
from collections import defaultdict
from tap_gmail import *


def get_abs_path(path):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), path)

with open(get_abs_path('schemas/gmail_schema.json')) as json_file:
    gmail_schema = json.load(json_file)

# Start date is today -9 days
previous_week = find_previous_week()

# Start date is today -3 days
latest_data = find_latest_data()


def find_weekly_active_users(selected_date=previous_week, page_token=None):
    week = create_week(selected_date)
    start_date = week[0]
    end_date = week[-1]

    for date in week:
        process_sent(date, page_token)

    total = total_unique_users(total_weekly_active_users)
    json_response = create_json_response(start_date, end_date, total, 'weekly active users')

    with Transformer() as transformer:
        transformed_record = transformer.transform(json_response, 'gmail')

    singer.write_schema('gmail', gmail_schema, 'timestamp')
    singer.write_records('gmail', transformed_record)

    return json_response


def find_weekly_emails_sent(selected_date=previous_week, page_token=None):
    week = create_week(selected_date)
    start_date = week[0]
    end_date = week[-1]

    total = total_emails_count(total_weekly_active_users)
    json_response = create_json_response(start_date, end_date, total, 'weekly emails sent')

    with Transformer() as transformer:
        transformed_record = transformer.transform(json_response, 'gmail')

    singer.write_schema('gmail', gmail_schema, 'timestamp')
    singer.write_records('gmail', transformed_record)

    return json_response


def find_weekly_emails_received(selected_date=previous_week, page_token=None):
    week = create_week(selected_date)
    start_date = week[0]
    end_date = week[-1]

    for date in week:
        process_received(date, page_token)

    total = total_emails_count(total_weekly_emails_received)
    json_response = create_json_response(start_date, end_date, total, 'weekly emails received')

    with Transformer() as transformer:
        transformed_record = transformer.transform(json_response, 'gmail')

    singer.write_schema('gmail', gmail_schema, 'timestamp')
    singer.write_records('gmail', transformed_record)

    return json_response


def find_daily_active_users(selected_date=latest_data, page_token=None):
    daily_active_senders = get_emails(selected_date, page_token, 'sent')
    start_date = selected_date
    end_date = selected_date

    try:
        for sender in daily_active_senders['usageReports']:
            total_daily_senders[sender['date']].append(
                {sender['entity']['userEmail']: sender['parameters'][0]['intValue']}
            )
    except KeyError:
        print('Only partial or no data available. Please try an earlier date.')

    if 'nextPageToken' in daily_active_senders:
        find_daily_active_users(
            selected_date, daily_active_senders['nextPageToken'])
        return

    total = len(total_daily_senders.get(selected_date, []))
    json_response = create_json_response(start_date, end_date, total, 'daily active users')

    with Transformer() as transformer:
        transformed_record = transformer.transform(json_response, 'gmail')

    singer.write_schema('gmail', gmail_schema, 'timestamp')
    singer.write_records('gmail', transformed_record)

    return json_response


def find_daily_emails_sent(selected_date=latest_data, page_token=None):
    week = create_week(selected_date)
    start_date = selected_date
    end_date = selected_date

    total = total_emails_count(total_daily_senders)
    json_response = create_json_response(start_date, end_date, total, 'daily emails sent')

    with Transformer() as transformer:
        transformed_record = transformer.transform(json_response, 'gmail')

    singer.write_schema('gmail', gmail_schema, 'timestamp')
    singer.write_records('gmail', transformed_record)

    return json_response


def find_daily_emails_received(selected_date=latest_data, page_token=None):
    daily_emails_received = get_emails(selected_date, page_token, 'received')
    start_date = selected_date
    end_date = selected_date

    try:
        for sender in daily_emails_received['usageReports']:
            total_daily_emails_received[sender['date']].append(
                {sender['entity']['userEmail']: sender['parameters'][0]['intValue']}
            )
    except KeyError:
        print('Only partial or no data available. Please try an earlier date.')

    if 'nextPageToken' in daily_emails_received:
        find_daily_emails_received(
            selected_date, daily_emails_received['nextPageToken'])
        return

    total = total_emails_count(total_daily_emails_received)
    json_response = create_json_response(start_date, end_date, total, 'daily emails received')

    with Transformer() as transformer:
        transformed_record = transformer.transform(json_response, 'gmail')

    singer.write_schema('gmail', gmail_schema, 'timestamp')
    singer.write_records('gmail', transformed_record)

    return json_response


find_weekly_active_users()
find_weekly_emails_sent()
find_weekly_emails_received()
find_daily_active_users()
find_daily_emails_sent()
find_daily_emails_received()