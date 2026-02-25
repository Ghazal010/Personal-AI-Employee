#!/usr/bin/env python3
"""
Simple notification-based watcher for Bronze Tier
Monitors Inbox and creates notification files for manual processing
"""

import time
from pathlib import Path
from datetime import datetime

# Configuration
VAULT_PATH = Path(__file__).parent.parent / "AI_Employee_Vault"
INBOX_PATH = VAULT_PATH / "Inbox"
NEEDS_ACTION_PATH = VAULT_PATH / "Needs_Action"
CHECK_INTERVAL = 30  # seconds

# Track processed files
processed_files = set()


def log(message: str):
    """Log with timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")


def get_inbox_files():
    """Get all files in the Inbox folder"""
    if not INBOX_PATH.exists():
        INBOX_PATH.mkdir(parents=True, exist_ok=True)
        return []

    return [f for f in INBOX_PATH.iterdir() if f.is_file() and not f.name.startswith('.')]


def create_notification(file_path: Path):
    """Create a notification file for manual processing"""
    log(f"New file detected: {file_path.name}")

    # Create notification in Needs_Action
    notification_file = NEEDS_ACTION_PATH / f"PROCESS-{file_path.stem}.md"

    notification_content = f"""# 🔔 New Inbox Item Detected

**Detected:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**File:** {file_path.name}
**Location:** {file_path}

## Action Required

A new item has been detected in the Inbox. Please process it:

1. Read the file: `{file_path}`
2. Analyze the content
3. Create appropriate action items
4. Update the Dashboard
5. Move to Done folder when complete

## Quick Process

Run this command:
```bash
claude code
```

Then say: "Process the inbox item at {file_path}"

---

**Status:** ⏳ Awaiting Processing
**Priority:** Based on content
**Auto-detected by:** Inbox Watcher
"""

    notification_file.write_text(notification_content)
    log(f"Created notification: {notification_file.name}")


def watch_inbox():
    """Main watcher loop"""
    log("Starting Simple Inbox Watcher...")
    log(f"Monitoring: {INBOX_PATH}")
    log(f"Check interval: {CHECK_INTERVAL} seconds")
    log(f"Notifications will be created in: {NEEDS_ACTION_PATH}")

    # Initialize with existing files
    for file_path in get_inbox_files():
        processed_files.add(file_path.name)

    log(f"Found {len(processed_files)} existing files (will not process)")

    try:
        while True:
            current_files = get_inbox_files()

            # Check for new files
            for file_path in current_files:
                if file_path.name not in processed_files:
                    create_notification(file_path)
                    processed_files.add(file_path.name)

            # Check for deleted files (cleanup tracking)
            current_names = {f.name for f in current_files}
            processed_files.intersection_update(current_names)

            time.sleep(CHECK_INTERVAL)

    except KeyboardInterrupt:
        log("Watcher stopped by user")
    except Exception as e:
        log(f"Watcher error: {e}")
        raise


if __name__ == "__main__":
    watch_inbox()
