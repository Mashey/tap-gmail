import requests
import json
from dotenv import load_dotenv
import os
from collections import defaultdict
import pandas as pd
import pprint
import singer
from datetime import date, datetime, timezone


pp = pprint.PrettyPrinter(indent=4, depth=3)
current_datetime = date.today()

# This code is for production.
# args = singer.utils.parse_args(["key", "token"])
# API_KEY = args.config['key']
# TOKEN = args.config['token']

# The code below is for testing with Pytest.
load_dotenv()
API_KEY = json.loads(os.getenv('gitlab'))['key']
# TOKEN = json.loads(os.getenv('gitlab'))['token']

headers = {
    # 'Authorization': TOKEN,
    'Accept': 'application/json'
}

client = requests.Session()

# Requirements
# daily active email senders from gitlab.com
# daily emails sent from gitlab.com
# daily emails received to gitlab.com
# weekly active email senders from gitlab.com
# weekly emails sent from gitlab.com
# weekly emails received to gitlab.com

# Example
# GET https: // www.googleapis.com/admin/reports/v1/usage/users/[USERKEY]/dates/[DATE]?key = [YOUR_API_KEY] HTTP/1.1

# Authorization: Bearer[YOUR_ACCESS_TOKEN]
# Accept: application/json

# Gmail Parameters
# num_emails_exchanged
#  - integer
#  - The total number of emails exchanged. This is the total of num_emails_sent plus num_emails_received.

# num_emails_received
#  - integer
#  - The number of emails received by the user.

# num_emails_sent
#  - integer
#  - The number of emails sent by the user.

# timestamp_last_access
#  - integer
#  - Last access timestamp

# timestamp_last_interaction
#  - integer
#  - Last interactive access timestamp


def fetch_reports_gmail(user="all", date_param=current_datetime):
    user_key = user
    start_date = date_param

    payload = {
        'applicationName': 'gmail',
        'key': API_KEY
    }

    response = client.get(
        f"https://www.googleapis.com/admin/reports/v1/usage/users/{user_key}/dates/{start_date}", headers=headers, params=payload)

    gmail_reports = response.json()

    # singer.write_schema('gmail_reports', gmail_reports_schema, 'id')
    # singer.write_records('gmail_reports', gmail_reports)

    return gmail_reports
