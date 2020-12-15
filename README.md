# Google Workplace :: Reports API :: Singer Tap

This application retrieves Gmail data from a Google Workplace (formerly G-suite) organization. The privacy of user data and personal identifying information is a focus, thus all data for each request is cleaned and modeled at the point of origin before being transported into a data warehouse.

The aggregated data follows a simple JSON schema that contains the following properties:

- `timestamp`
  - The time the query was run
- `start_date`
  - The range start date of the query
- `end_date`
  - The range end date of the query
- `query_type`
  - The type of query
    - `daily active users`
    - `daily emails sent`
    - `daily emails received`
    - `weekly active users`
    - `weekly emails sent`
    - `weekly emails received`
- `total`
  - The integer total returned by the above query types

This application utilizes the [Reports API](https://developers.google.com/admin-sdk/reports/v1/get-start/getting-started) which is part of the [Admin SDK](https://developers.google.com/admin-sdk).

## Admin SDK Setup

The Google API Python Client documentation provides a guide for completing all necessary steps to ensure the application and environment are configured correclty. The guide can be found here:

[Using OAuth 2.0 for Server to Server Applications](https://github.com/googleapis/google-api-python-client/blob/master/docs/oauth-server.md)

The key steps in the guide are:

- Create a service account
- Delegate domain-wide authority to the service account
- Create and download a `json` [service account key](https://cloud.google.com/iam/docs/creating-managing-service-account-keys#creating_service_account_keys) from the newly-created service account

## Update `reports_service.py` Variables

```python
# "ADMIN_SDK_KEY" should be updated if your Kubernetes secret name is different

SERVICE_ACCOUNT_FILE = os.getenv("ADMIN_SDK_KEY")

# Update to a Google user authorized to run reports in Google Workplace

USER_ACCOUNT = "jordan@mashey.com"
```

## Endpoints :: Reports API :: Gmail

All Reports API endpoints share a common JSON schema:

```json
// gmail_schema.json

{
  "type": ["object", "null"],
  "additionalProperties": false,
  "properties": {
    "timestamp": { "type": ["null", "string"] },
    "query_type": { "type": ["null", "string"] },
    "start_date": { "type": ["null", "string"] },
    "end_date": { "type": ["null", "string"] },
    "total": { "type": ["null", "integer"] }
  }
}
```

### Daily Active Users

```python
def find_daily_active_users(selected_date=latest_data, page_token=None)
```

- This function will return the number of daily active users for a given date.
- The default date is always (today - 3) in order to account for the lag time of data availability.

Example Response:

```json
{
  "timestamp": "2020-11-19T23:02:09.236462+00:00",
  "query_type": "daily active users",
  "start_date": "2020-11-19",
  "end_date": "2020-11-19",
  "total": 50
}
```

### Daily Emails Sent

```python
def find_daily_emails_sent(selected_date=latest_data, page_token=None)
```

- This function will return the number of emails sent for a given date.
- The default date is always (today - 3) in order to account for the lag time of data availability.

Example Response:

```json
{
  "timestamp": "2020-11-19T23:02:09.236462+00:00",
  "query_type": "daily emails sent",
  "start_date": "2020-11-19",
  "end_date": "2020-11-19",
  "total": 50
}
```

### Daily Emails Received

```python
def find_daily_emails_received(selected_date=latest_data, page_token=None)
```

- This function will return the number of emails received for a given date.
- The default date is always (today - 3) in order to account for the lag time of data availability.

Example Response:

```json
{
  "timestamp": "2020-11-19T23:02:09.236462+00:00",
  "query_type": "daily emails received",
  "start_date": "2020-11-19",
  "end_date": "2020-11-19",
  "total": 50
}
```

### Weekly Active Users

```python
def find_weekly_active_users(selected_date=previous_week, page_token=None)
```

- This function will return the number of active users for a given date range.
- The default date range is always (today - 9) in order to account for the lag time of data availability.

Example Response:

```json
{
  "timestamp": "2020-11-19T23:02:09.236462+00:00",
  "query_type": "weekly active users",
  "start_date": "2020-11-09",
  "end_date": "2020-11-15",
  "total": 50
}
```

### Weekly Emails Sent

```python
def find_weekly_emails_sent(selected_date=previous_week, page_token=None)
```

- This function will return the number of emails sent for a given date range.
- The default date range is always (today - 9) in order to account for the lag time of data availability.

Example Response:

```json
{
  "timestamp": "2020-11-19T23:02:09.236462+00:00",
  "query_type": "weekly emails sent",
  "start_date": "2020-11-09",
  "end_date": "2020-11-15",
  "total": 50
}
```

### Weekly Emails Received

```python
def find_weekly_emails_received(selected_date=previous_week, page_token=None)
```

- This function will return the number of emails received for a given date range.
- The default date range is always (today - 9) in order to account for the lag time of data availability.

Example Response:

```json
{
  "timestamp": "2020-11-19T23:02:09.236462+00:00",
  "query_type": "weekly emails received",
  "start_date": "2020-11-09",
  "end_date": "2020-11-15",
  "total": 50
}
```

## Helpful Documentation

Links to helpful documentation for this project

### Google Cloud Platform

[Admin SDK](https://developers.google.com/admin-sdk)

[Admin SDK :: Instance Methods](https://googleapis.github.io/google-api-python-client/docs/dyn/admin_reports_v1.html)

[GCP Authentication](https://cloud.google.com/docs/authentication)

[google-auth Python Library](https://google-auth.readthedocs.io/en/latest/user-guide.html)

[Google Python API Client](https://github.com/googleapis/google-api-python-client)

[Reports API :: User Usage Reports :: Guide](https://developers.google.com/admin-sdk/reports/v1/guides/manage-usage-users)

[Reports API :: Usage Reports (GET) :: Reference](https://developers.google.com/admin-sdk/reports/v1/reference/userUsageReport/get)

[Reports API :: Gmail Parameters](https://developers.google.com/admin-sdk/reports/v1/appendix/usage/user/gmail)

[Reports API :: Authorize Requests](https://developers.google.com/admin-sdk/reports/v1/guides/authorizing)