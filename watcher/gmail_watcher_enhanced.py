#!/usr/bin/env python3
"""
Enhanced Gmail Watcher with Error Recovery & Graceful Degradation
Monitors Gmail inbox with robust error handling and retry mechanisms
"""

import os
import sys
import time
import pickle
import logging
import traceback
from pathlib import Path
from datetime import datetime
from functools import wraps
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Add parent directory to path for audit_logger import
sys.path.insert(0, str(Path(__file__).parent.parent))
from audit_logger import AuditLogger, EventType

# Configuration
VAULT_PATH = Path(__file__).parent.parent / "AI_Employee_Vault"
EMAILS_PATH = VAULT_PATH / "Emails"
CREDENTIALS_PATH = Path(__file__).parent / "credentials" / "gmail_credentials.json"
TOKEN_PATH = Path(__file__).parent / "credentials" / "gmail_token.pickle"
LOG_PATH = Path(__file__).parent.parent / "logs" / "gmail-watcher-detailed.log"
CHECK_INTERVAL = 120  # 2 minutes
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# Error recovery settings
MAX_RETRIES = 3
INITIAL_RETRY_DELAY = 1  # seconds
MAX_RETRY_DELAY = 60  # seconds
CONSECUTIVE_FAILURE_THRESHOLD = 5

# Track processed emails and failures
processed_ids = set()
consecutive_failures = 0
last_successful_check = None

# Setup logging
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_PATH),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Setup audit logger
audit_logger = AuditLogger("gmail_watcher")


def retry_with_backoff(max_retries=MAX_RETRIES, initial_delay=INITIAL_RETRY_DELAY):
    """
    Decorator for retry logic with exponential backoff
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            delay = initial_delay
            last_exception = None

            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except HttpError as e:
                    last_exception = e
                    error_code = e.resp.status

                    # Don't retry on authentication errors
                    if error_code in [401, 403]:
                        logger.error(f"Authentication error in {func.__name__}: {e}")
                        raise

                    # Don't retry on client errors (except rate limit)
                    if 400 <= error_code < 500 and error_code != 429:
                        logger.error(f"Client error in {func.__name__}: {e}")
                        raise

                    # Retry on server errors and rate limits
                    if attempt < max_retries - 1:
                        logger.warning(
                            f"Attempt {attempt + 1}/{max_retries} failed for {func.__name__}: {e}. "
                            f"Retrying in {delay}s..."
                        )
                        time.sleep(delay)
                        delay = min(delay * 2, MAX_RETRY_DELAY)  # Exponential backoff
                    else:
                        logger.error(f"All {max_retries} attempts failed for {func.__name__}: {e}")

                except Exception as e:
                    last_exception = e
                    if attempt < max_retries - 1:
                        logger.warning(
                            f"Attempt {attempt + 1}/{max_retries} failed for {func.__name__}: {e}. "
                            f"Retrying in {delay}s..."
                        )
                        time.sleep(delay)
                        delay = min(delay * 2, MAX_RETRY_DELAY)
                    else:
                        logger.error(
                            f"All {max_retries} attempts failed for {func.__name__}: {e}\n"
                            f"Traceback: {traceback.format_exc()}"
                        )

            # If all retries failed, return None for graceful degradation
            return None

        return wrapper
    return decorator


def log(message: str, level: str = "INFO"):
    """Log with timestamp and level"""
    if level == "ERROR":
        logger.error(message)
    elif level == "WARNING":
        logger.warning(message)
    else:
        logger.info(message)


@retry_with_backoff(max_retries=3)
def get_gmail_service():
    """Authenticate and return Gmail service with retry logic"""
    creds = None

    # Load existing token
    if TOKEN_PATH.exists():
        try:
            with open(TOKEN_PATH, 'rb') as token:
                creds = pickle.load(token)
        except Exception as e:
            logger.error(f"Error loading token: {e}. Will re-authenticate.")
            creds = None

    # If no valid credentials, authenticate
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
                logger.info("Successfully refreshed credentials")
                audit_logger.log_auth_event("token_refresh", True)
            except Exception as e:
                logger.error(f"Error refreshing credentials: {e}. Will re-authenticate.")
                audit_logger.log_auth_event("token_refresh", False, {"error": str(e)})
                creds = None

        if not creds:
            if not CREDENTIALS_PATH.exists():
                logger.error(f"Credentials file not found at {CREDENTIALS_PATH}")
                logger.error("Please download credentials.json from Google Cloud Console")
                raise FileNotFoundError(f"Credentials file not found: {CREDENTIALS_PATH}")

            try:
                flow = InstalledAppFlow.from_client_secrets_file(
                    str(CREDENTIALS_PATH), SCOPES)
                creds = flow.run_local_server(port=0)
                logger.info("Successfully authenticated with new credentials")
                audit_logger.log_auth_event("oauth_authentication", True)
            except Exception as e:
                logger.error(f"Authentication failed: {e}")
                audit_logger.log_auth_event("oauth_authentication", False, {"error": str(e)})
                raise

        # Save token for future use
        try:
            TOKEN_PATH.parent.mkdir(parents=True, exist_ok=True)
            with open(TOKEN_PATH, 'wb') as token:
                pickle.dump(creds, token)
            logger.info("Token saved successfully")
        except Exception as e:
            logger.warning(f"Could not save token: {e}. Will need to re-authenticate next time.")

    return build('gmail', 'v1', credentials=creds)


@retry_with_backoff(max_retries=3)
def get_unread_important_emails(service):
    """Get unread important emails with retry logic"""
    try:
        results = service.users().messages().list(
            userId='me',
            q='is:unread is:important',
            maxResults=10
        ).execute()

        messages = results.get('messages', [])
        new_messages = [msg for msg in messages if msg['id'] not in processed_ids]

        if new_messages:
            logger.info(f"Found {len(new_messages)} new important emails")
            for msg in new_messages:
                audit_logger.log_event(
                    EventType.EMAIL_RECEIVED,
                    "New important email detected",
                    details={"email_id": msg['id']}
                )

        return new_messages

    except HttpError as e:
        logger.error(f"HTTP error fetching emails: {e}")
        raise
    except Exception as e:
        logger.error(f"Error fetching emails: {e}")
        raise


@retry_with_backoff(max_retries=3)
def get_email_details(service, message_id):
    """Get full email details with retry logic"""
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
                    try:
                        body = base64.urlsafe_b64decode(
                            part['body']['data']).decode('utf-8')
                        break
                    except Exception as e:
                        logger.warning(f"Error decoding email body part: {e}")
        elif 'body' in msg['payload']:
            import base64
            try:
                body = base64.urlsafe_b64decode(
                    msg['payload']['body']['data']).decode('utf-8')
            except Exception as e:
                logger.warning(f"Error decoding email body: {e}")
                body = "[Could not decode email body]"

        return {
            'id': message_id,
            'from': headers.get('From', 'Unknown'),
            'subject': headers.get('Subject', 'No Subject'),
            'date': headers.get('Date', 'Unknown'),
            'body': body[:1000]  # First 1000 chars
        }

    except HttpError as e:
        logger.error(f"HTTP error getting email details for {message_id}: {e}")
        audit_logger.log_event(
            EventType.EMAIL_ERROR,
            "Failed to fetch email details",
            status="failure",
            details={"email_id": message_id, "error": str(e)}
        )
        raise
    except Exception as e:
        logger.error(f"Error getting email details for {message_id}: {e}")
        audit_logger.log_event(
            EventType.EMAIL_ERROR,
            "Failed to fetch email details",
            status="failure",
            details={"email_id": message_id, "error": str(e)}
        )
        raise


def create_action_file(email):
    """Create action file in Emails folder with error handling"""
    try:
        EMAILS_PATH.mkdir(parents=True, exist_ok=True)

        # Create filename
        safe_subject = "".join(c for c in email['subject']
                              if c.isalnum() or c in (' ', '-', '_'))[:50]
        filename = f"EMAIL-{email['id'][:8]}-{safe_subject}.md"
        filepath = EMAILS_PATH / filename

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
**Source:** Gmail Watcher (Enhanced)
"""

        filepath.write_text(content, encoding='utf-8')
        logger.info(f"✅ Created action file: {filename}")

        # Audit log file creation
        audit_logger.log_file_created(str(filepath), "email")
        audit_logger.log_event(
            EventType.EMAIL_PROCESSED,
            "Email converted to action file",
            details={
                "email_id": email['id'],
                "from": email['from'],
                "subject": email['subject'],
                "file_path": str(filepath)
            }
        )

        return filepath

    except Exception as e:
        logger.error(f"Error creating action file for email {email.get('id', 'unknown')}: {e}")
        return None


def check_system_health():
    """Check system health and log status"""
    global consecutive_failures, last_successful_check

    health_status = {
        'consecutive_failures': consecutive_failures,
        'last_successful_check': last_successful_check,
        'credentials_exist': CREDENTIALS_PATH.exists(),
        'token_exists': TOKEN_PATH.exists(),
        'emails_folder_exists': EMAILS_PATH.exists(),
    }

    # Audit log health check
    audit_logger.log_health_check(health_status)

    if consecutive_failures >= CONSECUTIVE_FAILURE_THRESHOLD:
        logger.error(
            f"⚠️ HEALTH CHECK FAILED: {consecutive_failures} consecutive failures. "
            f"Last successful check: {last_successful_check}"
        )
        return False

    return True


def watch_gmail():
    """Main watcher loop with graceful degradation"""
    global consecutive_failures, last_successful_check

    logger.info("=" * 60)
    logger.info("🚀 Starting Enhanced Gmail Watcher with Error Recovery")
    logger.info("=" * 60)
    logger.info(f"📁 Monitoring Gmail inbox")
    logger.info(f"⏱️ Check interval: {CHECK_INTERVAL} seconds")
    logger.info(f"🔄 Max retries per operation: {MAX_RETRIES}")
    logger.info(f"📝 Detailed logs: {LOG_PATH}")

    # Audit log system start
    audit_logger.log_system_start()

    # Initial authentication
    service = get_gmail_service()
    if not service:
        logger.error("❌ Could not authenticate with Gmail. Exiting.")
        audit_logger.log_error("authentication", "Failed to authenticate with Gmail", None)
        return

    logger.info("✅ Successfully authenticated with Gmail")
    logger.info("🔍 Starting monitoring loop...")

    try:
        while True:
            try:
                # Check system health periodically
                if not check_system_health():
                    logger.warning("System health check indicates issues. Continuing with caution...")

                # Get unread important emails
                new_emails = get_unread_important_emails(service)

                if new_emails is None:
                    # Graceful degradation: continue even if this check failed
                    logger.warning("⚠️ Failed to fetch emails this cycle. Will retry next cycle.")
                    consecutive_failures += 1
                    time.sleep(CHECK_INTERVAL)
                    continue

                # Reset failure counter on success
                consecutive_failures = 0
                last_successful_check = datetime.now()

                if new_emails:
                    logger.info(f"📧 Found {len(new_emails)} new important emails")

                    for msg in new_emails:
                        email = get_email_details(service, msg['id'])

                        if email:
                            result = create_action_file(email)
                            if result:
                                processed_ids.add(msg['id'])
                            else:
                                logger.warning(f"Failed to create action file for email {msg['id']}")
                        else:
                            logger.warning(f"Failed to get details for email {msg['id']}")
                else:
                    logger.debug("No new important emails")

                time.sleep(CHECK_INTERVAL)

            except KeyboardInterrupt:
                raise  # Re-raise to be caught by outer try-except

            except Exception as e:
                # Graceful degradation: log error but continue running
                consecutive_failures += 1
                logger.error(
                    f"❌ Error in monitoring cycle (failure #{consecutive_failures}): {e}\n"
                    f"Traceback: {traceback.format_exc()}"
                )

                # Audit log error
                audit_logger.log_error(
                    "monitoring_cycle_error",
                    str(e),
                    traceback.format_exc()
                )

                if consecutive_failures >= CONSECUTIVE_FAILURE_THRESHOLD:
                    logger.error(
                        f"🚨 Too many consecutive failures ({consecutive_failures}). "
                        f"Attempting to re-authenticate..."
                    )
                    try:
                        service = get_gmail_service()
                        if service:
                            logger.info("✅ Re-authentication successful")
                            consecutive_failures = 0
                        else:
                            logger.error("❌ Re-authentication failed")
                    except Exception as auth_error:
                        logger.error(f"❌ Re-authentication error: {auth_error}")

                # Continue running even after error
                logger.info(f"⏳ Waiting {CHECK_INTERVAL}s before next attempt...")
                time.sleep(CHECK_INTERVAL)

    except KeyboardInterrupt:
        logger.info("\n👋 Gmail Watcher stopped by user")
        audit_logger.log_system_stop("user_interrupt")
    except Exception as e:
        logger.error(f"💥 Fatal error in Gmail Watcher: {e}\n{traceback.format_exc()}")
        audit_logger.log_error("fatal_error", str(e), traceback.format_exc())
        audit_logger.log_system_stop("fatal_error")
        raise


if __name__ == "__main__":
    watch_gmail()
