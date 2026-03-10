#!/usr/bin/env python3
"""
Lightweight WhatsApp Monitor for Personal AI Employee
Uses manual export + automation hybrid approach

SETUP:
1. Export WhatsApp chat: Chat → More → Export chat
2. Save to whatsapp_inbox/ folder
3. This script processes and creates action items

Memory usage: ~20-30 MB (vs 500 MB for browser automation)
"""

import os
import re
import time
from pathlib import Path
from datetime import datetime

# Configuration
VAULT_PATH = Path(__file__).parent.parent / "AI_Employee_Vault"
WHATSAPP_PATH = VAULT_PATH / "WhatsApp_Chats"  # Updated: Save to WhatsApp_Chats folder
WHATSAPP_INBOX = Path(__file__).parent / "whatsapp_inbox"
CHECK_INTERVAL = 60  # Check every 1 minute
PROCESSED_FILE = Path(__file__).parent / ".processed_chats.txt"

# Track processed files
processed_files = set()


def log(message: str):
    """Log with timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")


def load_processed_files():
    """Load list of already processed files"""
    global processed_files
    if PROCESSED_FILE.exists():
        with open(PROCESSED_FILE, 'r') as f:
            processed_files = set(line.strip() for line in f)
    log(f"Loaded {len(processed_files)} processed files")


def mark_as_processed(filename: str):
    """Mark file as processed"""
    processed_files.add(filename)
    with open(PROCESSED_FILE, 'a') as f:
        f.write(f"{filename}\n")


def parse_whatsapp_export(file_path: Path) -> dict:
    """Parse WhatsApp exported chat file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract chat name from filename or content
        chat_name = file_path.stem.replace('WhatsApp Chat with ', '')

        # Parse messages (format: [DD/MM/YY, HH:MM:SS] Name: Message)
        messages = []
        pattern = r'\[(\d{2}/\d{2}/\d{2}), (\d{2}:\d{2}:\d{2})\] ([^:]+): (.+)'

        for match in re.finditer(pattern, content):
            date, time_str, sender, message = match.groups()
            messages.append({
                'date': date,
                'time': time_str,
                'sender': sender,
                'message': message
            })

        # Get last 10 messages for context
        recent_messages = messages[-10:] if len(messages) > 10 else messages

        return {
            'chat_name': chat_name,
            'total_messages': len(messages),
            'recent_messages': recent_messages,
            'file_name': file_path.name
        }

    except Exception as e:
        log(f"Error parsing {file_path.name}: {e}")
        return None


def create_action_file(chat_data: dict):
    """Create action item file in Needs_Action folder"""
    try:
        # Generate unique ID
        file_id = datetime.now().strftime("%Y%m%d%H%M%S")

        # Clean chat name for filename
        clean_name = re.sub(r'[^\w\s-]', '', chat_data['chat_name'])[:50]
        filename = f"WHATSAPP-{file_id}-{clean_name}.md"

        # Build recent messages text
        messages_text = ""
        for msg in chat_data['recent_messages']:
            messages_text += f"**[{msg['date']} {msg['time']}] {msg['sender']}:**\n{msg['message']}\n\n"

        # Create markdown content
        content = f"""# WhatsApp: {chat_data['chat_name']}

**Date:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Chat:** {chat_data['chat_name']}
**Total Messages:** {chat_data['total_messages']}
**Type:** WhatsApp Chat
**Priority:** Review Required

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

This chat was manually exported from WhatsApp and processed by WhatsApp Monitor.

**Source File:** {chat_data['file_name']}
**Processed:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""

        # Write to WhatsApp_Chats folder
        action_file = WHATSAPP_PATH / filename
        with open(action_file, 'w', encoding='utf-8') as f:
            f.write(content)

        log(f"✅ Created action file: {filename}")
        return True

    except Exception as e:
        log(f"❌ Error creating action file: {e}")
        return False


def check_for_new_chats():
    """Check whatsapp_inbox for new exported chats"""
    if not WHATSAPP_INBOX.exists():
        WHATSAPP_INBOX.mkdir(parents=True)
        log(f"Created inbox folder: {WHATSAPP_INBOX}")
        return

    # Find .txt files (WhatsApp exports as .txt)
    txt_files = list(WHATSAPP_INBOX.glob("*.txt"))

    new_files = [f for f in txt_files if f.name not in processed_files]

    if not new_files:
        return

    log(f"Found {len(new_files)} new WhatsApp chat(s)")

    for file_path in new_files:
        log(f"Processing: {file_path.name}")

        # Parse chat
        chat_data = parse_whatsapp_export(file_path)

        if chat_data:
            # Create action file
            if create_action_file(chat_data):
                mark_as_processed(file_path.name)
                log(f"✅ Processed: {file_path.name}")
        else:
            log(f"⚠️ Skipped: {file_path.name} (parsing failed)")


def main():
    """Main monitoring loop"""
    log("🚀 WhatsApp Monitor started (Lightweight Python version)")
    log(f"📁 Monitoring: {WHATSAPP_INBOX}")
    log(f"📊 Action files: {WHATSAPP_PATH}")
    log(f"⏱️ Check interval: {CHECK_INTERVAL} seconds")
    log("")
    log("📱 HOW TO USE:")
    log("1. Open WhatsApp chat")
    log("2. Tap ⋮ (menu) → More → Export chat")
    log("3. Choose 'Without Media'")
    log("4. Save to: whatsapp_inbox/ folder")
    log("5. This script will auto-process it!")
    log("")

    # Ensure folders exist
    WHATSAPP_PATH.mkdir(parents=True, exist_ok=True)
    WHATSAPP_INBOX.mkdir(parents=True, exist_ok=True)

    # Load processed files
    load_processed_files()

    try:
        while True:
            check_for_new_chats()
            time.sleep(CHECK_INTERVAL)

    except KeyboardInterrupt:
        log("\n👋 WhatsApp Monitor stopped")
    except Exception as e:
        log(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
