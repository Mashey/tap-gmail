import requests
import json
from dotenv import load_dotenv
import os
from collections import defaultdict
import pandas as pd
import pprint
import singer
from datetime import date, datetime, timezone
from tap_gmail.reports_api_service import *

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

# Reports API Service
service = create_service()

