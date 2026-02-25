#!/usr/bin/env python3
"""
WhatsApp Watcher for Personal AI Employee
Monitors WhatsApp Web for urgent messages

WARNING: This uses WhatsApp Web automation which may violate WhatsApp Terms of Service.
Use at your own risk. For production, use WhatsApp Business API.

SETUP REQUIRED:
1. Install Playwright: pip install playwright
2. Install browsers: playwright install chromium
3. First run will require QR code scan
4. Session will be saved for future use
"""

import time
from pathlib import Path
from datetime import datetime
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

# Configuration
VAULT_PATH = Path(__file__).parent.parent / "AI_Employee_Vault"
NEEDS_ACTION_PATH = VAULT_PATH / "Needs_Action"
SESSION_PATH = Path(__file__).parent / "credentials" / "whatsapp_session"
CHECK_INTERVAL = 30  # 30 seconds
URGENT_KEYWORDS = ['urgent', 'asap', 'emergency', 'invoice', 'payment', 'help', 'important']

# Track processed messages
processed_messages = set()


def log(message: str):
    """Log with timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")


def create_action_file(message_data):
    """Create action file in Needs_Action folder"""
    NEEDS_ACTION_PATH.mkdir(parents=True, exist_ok=True)

    # Create filename
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    safe_sender = "".join(c for c in message_data['sender']
                         if c.isalnum() or c in (' ', '-', '_'))[:30]
    filename = f"WHATSAPP-{timestamp}-{safe_sender}.md"
    filepath = NEEDS_ACTION_PATH / filename

    # Create content
    content = f"""# WhatsApp: {message_data['sender']}

**Date:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**From:** {message_data['sender']}
**Type:** WhatsApp Message
**Priority:** 🔴 Urgent (contains urgent keywords)

## Message Content

{message_data['message']}

---

## Detected Keywords

{', '.join(message_data['keywords'])}

## Suggested Actions

- [ ] Read and analyze message
- [ ] Determine urgency level
- [ ] Draft response
- [ ] Reply via WhatsApp
- [ ] Take required action

## Notes

This message was flagged as urgent based on keyword detection.

**Source:** WhatsApp Watcher
"""

    filepath.write_text(content)
    log(f"Created action file: {filename}")
    return filepath


def watch_whatsapp():
    """Main watcher loop"""
    log("Starting WhatsApp Watcher...")
    log(f"Session path: {SESSION_PATH}")
    log(f"Check interval: {CHECK_INTERVAL} seconds")
    log(f"Urgent keywords: {', '.join(URGENT_KEYWORDS)}")

    SESSION_PATH.mkdir(parents=True, exist_ok=True)

    try:
        with sync_playwright() as p:
            # Launch browser with persistent context (saves session)
            browser = p.chromium.launch_persistent_context(
                user_data_dir=str(SESSION_PATH),
                headless=False,  # Set to True after first login
                args=['--no-sandbox']
            )

            page = browser.pages[0] if browser.pages else browser.new_page()

            # Navigate to WhatsApp Web
            log("Navigating to WhatsApp Web...")
            page.goto('https://web.whatsapp.com')

            # Wait for QR code or chat list
            try:
                log("Waiting for WhatsApp to load...")
                log("If this is first run, please scan QR code")
                page.wait_for_selector('[data-testid="chat-list"]', timeout=60000)
                log("Successfully connected to WhatsApp Web")
            except PlaywrightTimeout:
                log("ERROR: Could not connect to WhatsApp Web")
                log("Please scan QR code and try again")
                return

            # Main monitoring loop
            while True:
                try:
                    # Find unread chats
                    unread_chats = page.query_selector_all('[aria-label*="unread"]')

                    if unread_chats:
                        log(f"Found {len(unread_chats)} unread chats")

                        for chat in unread_chats:
                            try:
                                # Get chat text
                                chat_text = chat.inner_text().lower()

                                # Check for urgent keywords
                                found_keywords = [kw for kw in URGENT_KEYWORDS
                                                if kw in chat_text]

                                if found_keywords:
                                    # Click chat to open
                                    chat.click()
                                    time.sleep(1)

                                    # Get sender name
                                    sender_elem = page.query_selector('[data-testid="conversation-header"]')
                                    sender = sender_elem.inner_text() if sender_elem else "Unknown"

                                    # Get last message
                                    messages = page.query_selector_all('[data-testid="msg-container"]')
                                    if messages:
                                        last_msg = messages[-1].inner_text()

                                        # Create unique ID
                                        msg_id = f"{sender}_{last_msg[:50]}"

                                        if msg_id not in processed_messages:
                                            log(f"Urgent message from {sender}")

                                            message_data = {
                                                'sender': sender,
                                                'message': last_msg,
                                                'keywords': found_keywords
                                            }

                                            create_action_file(message_data)
                                            processed_messages.add(msg_id)

                            except Exception as e:
                                log(f"Error processing chat: {e}")
                                continue

                except Exception as e:
                    log(f"Error checking messages: {e}")

                time.sleep(CHECK_INTERVAL)

    except KeyboardInterrupt:
        log("WhatsApp Watcher stopped by user")
    except Exception as e:
        log(f"WhatsApp Watcher error: {e}")
        raise


if __name__ == "__main__":
    watch_whatsapp()
