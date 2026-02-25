#!/usr/bin/env python3
"""
Gmail Watcher for Personal AI Employee
Monitors Gmail inbox and creates action items for important emails

SETUP REQUIRED:
1. Enable Gmail API in Google Cloud Console
2. Download credentials.json
3. Run: pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client
4. First run will open browser for OAuth consent
"""

import os
import time
import pickle
from pathlib import Path
from datetime import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Configuration
VAULT_PATH = Path(__file__).parent.parent / "AI_Employee_Vault"
NEEDS_ACTION_PATH = VAULT_PATH / "Needs_Action"
CREDENTIALS_PATH = Path(__file__).parent / "credentials" / "gmail_credentials.json"
TOKEN_PATH = Path(__file__).parent / "credentials" / "gmail_token.pickle"
CHECK_INTERVAL = 120  # 2 minutes
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# Track processed emails
processed_ids = set()


def log(message: str):
    """Log with timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")


def get_gmail_service():
    """Authenticate and return Gmail service"""
    creds = None

    # Load existing token
    if TOKEN_PATH.exists():
        with open(TOKEN_PATH, 'rb') as token:
            creds = pickle.load(token)

    # If no valid credentials, authenticate
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not CREDENTIALS_PATH.exists():
                log(f"ERROR: Credentials file not found at {CREDENTIALS_PATH}")
                log("Please download credentials.json from Google Cloud Console")
                return None

            flow = InstalledAppFlow.from_client_secrets_file(
                str(CREDENTIALS_PATH), SCOPES)
            creds = flow.run_local_server(port=0)

        # Save token for future use
        TOKEN_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(TOKEN_PATH, 'wb') as token:
            pickle.dump(creds, token)

    return build('gmail', 'v1', credentials=creds)


def get_unread_important_emails(service):
    """Get unread important emails"""
    try:
        results = service.users().messages().list(
            userId='me',
            q='is:unread is:important',
            maxResults=10
        ).execute()

        messages = results.get('messages', [])
        return [msg for msg in messages if msg['id'] not in processed_ids]

    except Exception as e:
        log(f"Error fetching emails: {e}")
        return []


def get_email_details(service, message_id):
    """Get full email details"""
    try:
        msg = service.users().messages().get(
            userId='me',
            id=message_id,
            format='full'
        ).execute()

        # Extract headers
        headers = {h['name']: h['value']
                  for h in msg['payload']['headers']}

        # Extract body
        body = ""
        if 'parts' in msg['payload']:
            for part in msg['payload']['parts']:
                if part['mimeType'] == 'text/plain':
                    import base64
                    body = base64.urlsafe_b64decode(
                        part['body']['data']).decode('utf-8')
                    break
        elif 'body' in msg['payload']:
            import base64
            body = base64.urlsafe_b64decode(
                msg['payload']['body']['data']).decode('utf-8')

        return {
            'id': message_id,
            'from': headers.get('From', 'Unknown'),
            'subject': headers.get('Subject', 'No Subject'),
            'date': headers.get('Date', 'Unknown'),
            'body': body[:1000]  # First 1000 chars
        }

    except Exception as e:
        log(f"Error getting email details: {e}")
        return None


def create_action_file(email):
    """Create action file in Needs_Action folder"""
    NEEDS_ACTION_PATH.mkdir(parents=True, exist_ok=True)

    # Create filename
    safe_subject = "".join(c for c in email['subject']
                          if c.isalnum() or c in (' ', '-', '_'))[:50]
    filename = f"EMAIL-{email['id'][:8]}-{safe_subject}.md"
    filepath = NEEDS_ACTION_PATH / filename

    # Create content
    content = f"""# Email: {email['subject']}

**Date:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**From:** {email['from']}
**Received:** {email['date']}
**Type:** Email
**Priority:** Important

## Email Content

{email['body']}

---

## Suggested Actions

- [ ] Read and analyze email
- [ ] Draft response
- [ ] Take required action
- [ ] Reply to sender
- [ ] Archive email

## Notes

This email was flagged as important by Gmail.

**Email ID:** {email['id']}
**Source:** Gmail Watcher
"""

    filepath.write_text(content)
    log(f"Created action file: {filename}")
    return filepath


def watch_gmail():
    """Main watcher loop"""
    log("Starting Gmail Watcher...")
    log(f"Monitoring Gmail inbox")
    log(f"Check interval: {CHECK_INTERVAL} seconds")

    # Get Gmail service
    service = get_gmail_service()
    if not service:
        log("ERROR: Could not authenticate with Gmail")
        log("Please set up credentials first")
        return

    log("Successfully authenticated with Gmail")

    try:
        while True:
            # Get unread important emails
            new_emails = get_unread_important_emails(service)

            if new_emails:
                log(f"Found {len(new_emails)} new important emails")

                for msg in new_emails:
                    email = get_email_details(service, msg['id'])
                    if email:
                        create_action_file(email)
                        processed_ids.add(msg['id'])

            time.sleep(CHECK_INTERVAL)

    except KeyboardInterrupt:
        log("Gmail Watcher stopped by user")
    except Exception as e:
        log(f"Gmail Watcher error: {e}")
        raise


if __name__ == "__main__":
    watch_gmail()
