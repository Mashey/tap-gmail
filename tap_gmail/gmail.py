import requests
import json
from dotenv import load_dotenv
import os
from collections import defaultdict
import pandas as pd
import pprint
import singer
from datetime import datetime, timezone


pp = pprint.PrettyPrinter(indent=4, depth=3)

# This code is for production.
# args = singer.utils.parse_args(["key"])
# API_KEY = args.config['key']

# The code below is for testing with Pytest.
load_dotenv()
API_KEY = json.loads(os.getenv('gitlab'))['key']

# headers = {
#     'Authorization': API_KEY
# }

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
