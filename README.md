# Google Workplace :: Reports API :: Singer Tap

The first version of this application will retrieve Gmail data from a Google Workplace (formerly G-suite) organization.

The `Reports API` is part of the `Admin SDK`.

## Setup

The Google API Python Client documentation provides a guide for completing all necessary steps to ensure the application and environment are configured correclty. The guide can be found here:

[Using OAuth 2.0 for Server to Server Applications](https://github.com/googleapis/google-api-python-client/blob/master/docs/oauth-server.md)

The key steps in the guide are:

- Creating a service account
- Delegating domain-wide authority to the service account

## Endpoints :: Reports API :: Gmail

|Gmail query param|

### Daily Active Users

```python
def find_daily_active_users(selected_date=latest_data, page_token=None)
```

- This function will return the number of daily active users for a given date.
- The default date is always (today - 3) in order to account for the lag time of data availability.

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

[GCP Authentication](https://cloud.google.com/docs/authentication)

[OAuth API Verification FAQs](https://support.google.com/cloud/answer/9110914)

[Reports API :: User Usage Reports :: Guide](https://developers.google.com/admin-sdk/reports/v1/guides/manage-usage-users)

[Reports API :: Usage Reports (GET) :: Reference](https://developers.google.com/admin-sdk/reports/v1/reference/userUsageReport/get)

[Reports API :: Gmail Parameters](https://developers.google.com/admin-sdk/reports/v1/appendix/usage/user/gmail)

[Reports API :: Authorize Requests](https://developers.google.com/admin-sdk/reports/v1/guides/authorizing)
