#!/usr/bin/env python3
"""
File System Watcher for Personal AI Employee
Monitors the Inbox folder and triggers Claude Code when new files appear
"""

import os
import time
import subprocess
from pathlib import Path
from datetime import datetime

# Configuration
VAULT_PATH = Path(__file__).parent.parent / "AI_Employee_Vault"
INBOX_PATH = VAULT_PATH / "Inbox"
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


def trigger_claude_processing(file_path: Path):
    """Trigger Claude Code to process a new inbox item"""
    log(f"New file detected: {file_path.name}")

    # Create a prompt for Claude Code
    prompt = f"Process the inbox item at {file_path}. Read the file, analyze it, create an action item in Needs_Action folder, update the Dashboard, and move the original to Done folder."

    try:
        # Trigger Claude Code with a proper prompt
        result = subprocess.run(
            ["claude", "code", "--prompt", prompt],
            cwd=VAULT_PATH.parent,
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )

        if result.returncode == 0:
            log(f"Successfully processed: {file_path.name}")
            log(f"Output: {result.stdout[:200]}...")  # Show first 200 chars
        else:
            log(f"Error processing {file_path.name}: {result.stderr}")

    except subprocess.TimeoutExpired:
        log(f"Timeout processing {file_path.name}")
    except Exception as e:
        log(f"Exception processing {file_path.name}: {e}")


def watch_inbox():
    """Main watcher loop"""
    log("Starting Inbox Watcher...")
    log(f"Monitoring: {INBOX_PATH}")
    log(f"Check interval: {CHECK_INTERVAL} seconds")

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
                    trigger_claude_processing(file_path)
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
