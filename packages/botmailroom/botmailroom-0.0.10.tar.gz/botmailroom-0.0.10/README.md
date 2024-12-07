# BotMailroom Python Client

The BotMailroom Python client allows you to interact with the [BotMailroom API](https://docs.botmailroom.com/). It provides both synchronous and asynchronous methods for interacting with the API.

## Quickstart

### 1. Get an API Key

You can get an API key by signing up for a BotMailroom account and creating an API key at https://auth.botmailroom.com/account/api_keys

### 2. Install the Client

```bash
pip install botmailroom
```

### 3. Initialize the Client

```python
from botmailroom import BotMailRoom

client = BotMailRoom(api_key="your_api_key") # or set the BOTMAILROOM_API_KEY environment variable
```

### 4. Create an Inbox

```python
inbox = client.create_inbox(name="My Inbox", email_address="CHANGE_THIS@inbox.botmailroom.com")
```

### 5. Check Emails

Unless you have specific allow and block rules that prevent it, you will receive an email from `support@inbox.botmailroom.com` after you create an inbox **for the first time**. If you’d like to send a test email to your inbox, you can do so by:

1. Using a mail client of your choice.
2. Sending a request with the `send_email` method.

You can then check for new emails using the `get_emails` method.

```python
emails = client.get_emails(inbox_id=inbox.id)
print(emails)
```
