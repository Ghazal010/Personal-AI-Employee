#!/usr/bin/env python3
"""
Enhanced WhatsApp Monitor with Error Recovery & Graceful Degradation
Processes WhatsApp chat exports with robust error handling
"""

import os
import sys
import re
import time
import logging
import traceback
from pathlib import Path
from datetime import datetime
from functools import wraps

# Add parent directory to path for audit_logger import
sys.path.insert(0, str(Path(__file__).parent.parent))
from audit_logger import AuditLogger, EventType

# Configuration
VAULT_PATH = Path(__file__).parent.parent / "AI_Employee_Vault"
WHATSAPP_PATH = VAULT_PATH / "WhatsApp_Chats"
WHATSAPP_INBOX = Path(__file__).parent / "whatsapp_inbox"
LOG_PATH = Path(__file__).parent.parent / "logs" / "whatsapp-monitor-detailed.log"
CHECK_INTERVAL = 60  # Check every 1 minute
PROCESSED_FILE = Path(__file__).parent / ".processed_chats.txt"

# Error recovery settings
MAX_RETRIES = 3
INITIAL_RETRY_DELAY = 1
MAX_RETRY_DELAY = 30
CONSECUTIVE_FAILURE_THRESHOLD = 5

# Track processed files and failures
processed_files = set()
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
audit_logger = AuditLogger("whatsapp_monitor")


def retry_with_backoff(max_retries=MAX_RETRIES, initial_delay=INITIAL_RETRY_DELAY):
    """Decorator for retry logic with exponential backoff"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            delay = initial_delay
            last_exception = None

            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
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

            # Return None for graceful degradation
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


def load_processed_files():
    """Load list of already processed files with error handling"""
    global processed_files
    try:
        if PROCESSED_FILE.exists():
            with open(PROCESSED_FILE, 'r', encoding='utf-8') as f:
                processed_files = set(line.strip() for line in f if line.strip())
            logger.info(f"Loaded {len(processed_files)} processed files from history")
        else:
            logger.info("No processed files history found. Starting fresh.")
    except Exception as e:
        logger.error(f"Error loading processed files: {e}. Starting with empty set.")
        processed_files = set()


def mark_as_processed(filename: str):
    """Mark file as processed with error handling"""
    try:
        processed_files.add(filename)
        with open(PROCESSED_FILE, 'a', encoding='utf-8') as f:
            f.write(f"{filename}\n")
        logger.debug(f"Marked {filename} as processed")
    except Exception as e:
        logger.error(f"Error marking file as processed: {e}")


@retry_with_backoff(max_retries=3)
def parse_whatsapp_export(file_path: Path) -> dict:
    """Parse WhatsApp exported chat file with error handling"""
    try:
        # Validate file exists and is readable
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        if file_path.stat().st_size == 0:
            raise ValueError(f"File is empty: {file_path}")

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        if not content.strip():
            raise ValueError(f"File has no content: {file_path}")

        # Extract chat name from filename or content
        chat_name = file_path.stem.replace('WhatsApp Chat with ', '')

        # Parse messages (format: [DD/MM/YY, HH:MM:SS] Name: Message)
        messages = []
        pattern = r'\[(\d{2}/\d{2}/\d{2}), (\d{2}:\d{2}:\d{2})\] ([^:]+): (.+)'

        for match in re.finditer(pattern, content):
            try:
                date, time_str, sender, message = match.groups()
                messages.append({
                    'date': date,
                    'time': time_str,
                    'sender': sender.strip(),
                    'message': message.strip()
                })
            except Exception as e:
                logger.warning(f"Error parsing message in {file_path.name}: {e}")
                continue

        if not messages:
            logger.warning(f"No messages found in {file_path.name}. File may have different format.")
            # Still return data for logging purposes
            return {
                'chat_name': chat_name,
                'total_messages': 0,
                'recent_messages': [],
                'file_name': file_path.name,
                'parse_warning': 'No messages could be parsed'
            }

        # Get last 10 messages for context
        recent_messages = messages[-10:] if len(messages) > 10 else messages

        logger.info(f"Successfully parsed {len(messages)} messages from {file_path.name}")

        # Audit log chat received
        audit_logger.log_whatsapp_received(chat_name, len(messages))

        return {
            'chat_name': chat_name,
            'total_messages': len(messages),
            'recent_messages': recent_messages,
            'file_name': file_path.name
        }

    except UnicodeDecodeError as e:
        logger.error(f"Encoding error reading {file_path.name}: {e}. Trying different encoding...")
        try:
            with open(file_path, 'r', encoding='latin-1') as f:
                content = f.read()
            # Retry parsing with different encoding
            logger.info(f"Successfully read {file_path.name} with latin-1 encoding")
            # Re-run parsing logic here if needed
        except Exception as e2:
            logger.error(f"Failed to read {file_path.name} with alternative encoding: {e2}")
            raise

    except Exception as e:
        logger.error(f"Error parsing {file_path.name}: {e}\n{traceback.format_exc()}")
        audit_logger.log_event(
            EventType.WHATSAPP_ERROR,
            "Failed to parse WhatsApp chat",
            status="failure",
            details={"file_name": file_path.name, "error": str(e)}
        )
        raise


@retry_with_backoff(max_retries=3)
def create_action_file(chat_data: dict):
    """Create action item file in WhatsApp_Chats folder with error handling"""
    try:
        # Ensure folder exists
        WHATSAPP_PATH.mkdir(parents=True, exist_ok=True)

        # Generate unique ID
        file_id = datetime.now().strftime("%Y%m%d%H%M%S")

        # Clean chat name for filename
        clean_name = re.sub(r'[^\w\s-]', '', chat_data['chat_name'])[:50]
        if not clean_name:
            clean_name = "Unknown_Chat"

        filename = f"WHATSAPP-{file_id}-{clean_name}.md"

        # Build recent messages text
        messages_text = ""
        if chat_data['recent_messages']:
            for msg in chat_data['recent_messages']:
                try:
                    messages_text += f"**[{msg['date']} {msg['time']}] {msg['sender']}:**\n{msg['message']}\n\n"
                except KeyError as e:
                    logger.warning(f"Missing key in message: {e}")
                    continue
        else:
            messages_text = "*No messages could be parsed from this chat export*\n"

        # Add warning if present
        warning_text = ""
        if 'parse_warning' in chat_data:
            warning_text = f"\n⚠️ **Warning:** {chat_data['parse_warning']}\n"

        # Create markdown content
        content = f"""# WhatsApp: {chat_data['chat_name']}

**Date:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Chat:** {chat_data['chat_name']}
**Total Messages:** {chat_data['total_messages']}
**Type:** WhatsApp Chat
**Priority:** Review Required
{warning_text}
## Recent Messages

{messages_text}

---

## Suggested Actions

- [ ] Read and analyze conversation
- [ ] Identify action items
- [ ] Draft response if needed
- [ ] Reply via WhatsApp
- [ ] Archive chat

## Notes

This chat was manually exported from WhatsApp and processed by WhatsApp Monitor (Enhanced).

**Source File:** {chat_data['file_name']}
**Processed:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""

        # Write to WhatsApp_Chats folder
        action_file = WHATSAPP_PATH / filename
        action_file.write_text(content, encoding='utf-8')

        logger.info(f"✅ Created action file: {filename}")

        # Audit log file creation
        audit_logger.log_file_created(str(action_file), "whatsapp")
        audit_logger.log_event(
            EventType.WHATSAPP_PROCESSED,
            "WhatsApp chat converted to action file",
            details={
                "chat_name": chat_data['chat_name'],
                "message_count": chat_data['total_messages'],
                "file_path": str(action_file)
            }
        )

        return True

    except Exception as e:
        logger.error(f"Error creating action file: {e}\n{traceback.format_exc()}")
        audit_logger.log_event(
            EventType.WHATSAPP_ERROR,
            "Failed to create action file",
            status="failure",
            details={"chat_name": chat_data.get('chat_name', 'unknown'), "error": str(e)}
        )
        raise


def check_for_new_chats():
    """Check whatsapp_inbox for new exported chats with error handling"""
    global consecutive_failures, last_successful_check

    try:
        if not WHATSAPP_INBOX.exists():
            WHATSAPP_INBOX.mkdir(parents=True)
            logger.info(f"Created inbox folder: {WHATSAPP_INBOX}")
            return

        # Find .txt files (WhatsApp exports as .txt)
        try:
            txt_files = list(WHATSAPP_INBOX.glob("*.txt"))
        except Exception as e:
            logger.error(f"Error listing files in inbox: {e}")
            return

        new_files = [f for f in txt_files if f.name not in processed_files]

        if not new_files:
            logger.debug("No new WhatsApp chats found")
            return

        logger.info(f"📱 Found {len(new_files)} new WhatsApp chat(s)")

        for file_path in new_files:
            try:
                logger.info(f"Processing: {file_path.name}")

                # Parse chat
                chat_data = parse_whatsapp_export(file_path)

                if chat_data:
                    # Create action file
                    if create_action_file(chat_data):
                        mark_as_processed(file_path.name)
                        logger.info(f"✅ Successfully processed: {file_path.name}")
                        consecutive_failures = 0
                        last_successful_check = datetime.now()
                    else:
                        logger.warning(f"⚠️ Failed to create action file for: {file_path.name}")
                        consecutive_failures += 1
                else:
                    logger.warning(f"⚠️ Skipped: {file_path.name} (parsing returned None)")
                    consecutive_failures += 1

            except Exception as e:
                logger.error(f"❌ Error processing {file_path.name}: {e}")
                consecutive_failures += 1
                # Continue with next file instead of stopping

    except Exception as e:
        logger.error(f"Error in check_for_new_chats: {e}\n{traceback.format_exc()}")
        consecutive_failures += 1


def check_system_health():
    """Check system health and log status"""
    global consecutive_failures, last_successful_check

    health_status = {
        'consecutive_failures': consecutive_failures,
        'last_successful_check': last_successful_check,
        'inbox_exists': WHATSAPP_INBOX.exists(),
        'output_folder_exists': WHATSAPP_PATH.exists(),
        'processed_file_exists': PROCESSED_FILE.exists(),
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


def main():
    """Main monitoring loop with graceful degradation"""
    global consecutive_failures, last_successful_check

    logger.info("=" * 60)
    logger.info("🚀 Starting Enhanced WhatsApp Monitor with Error Recovery")
    logger.info("=" * 60)
    logger.info(f"📁 Monitoring: {WHATSAPP_INBOX}")
    logger.info(f"📊 Action files: {WHATSAPP_PATH}")
    logger.info(f"⏱️ Check interval: {CHECK_INTERVAL} seconds")
    logger.info(f"🔄 Max retries per operation: {MAX_RETRIES}")
    logger.info(f"📝 Detailed logs: {LOG_PATH}")
    logger.info("")
    logger.info("📱 HOW TO USE:")
    logger.info("1. Open WhatsApp chat")
    logger.info("2. Tap ⋮ (menu) → More → Export chat")
    logger.info("3. Choose 'Without Media'")
    logger.info("4. Save to: whatsapp_inbox/ folder")
    logger.info("5. This script will auto-process it!")
    logger.info("")

    # Audit log system start
    audit_logger.log_system_start()

    # Ensure folders exist
    try:
        WHATSAPP_PATH.mkdir(parents=True, exist_ok=True)
        WHATSAPP_INBOX.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        logger.error(f"Failed to create required folders: {e}")
        audit_logger.log_error("folder_creation", str(e), None)
        return

    # Load processed files
    load_processed_files()

    try:
        while True:
            try:
                # Check system health periodically
                if not check_system_health():
                    logger.warning("System health check indicates issues. Continuing with caution...")

                # Check for new chats
                check_for_new_chats()

                time.sleep(CHECK_INTERVAL)

            except KeyboardInterrupt:
                raise

            except Exception as e:
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

                # Continue running even after error
                logger.info(f"⏳ Waiting {CHECK_INTERVAL}s before next attempt...")
                time.sleep(CHECK_INTERVAL)

    except KeyboardInterrupt:
        logger.info("\n👋 WhatsApp Monitor stopped by user")
        audit_logger.log_system_stop("user_interrupt")
    except Exception as e:
        logger.error(f"💥 Fatal error in WhatsApp Monitor: {e}\n{traceback.format_exc()}")
        audit_logger.log_error("fatal_error", str(e), traceback.format_exc())
        audit_logger.log_system_stop("fatal_error")
        raise


if __name__ == "__main__":
    main()
