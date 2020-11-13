import requests
import json
from dotenv import load_dotenv
import os
from collections import defaultdict
import pandas as pd
import pprint
import singer
from datetime import date, datetime, timezone
import reports_api_service

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
