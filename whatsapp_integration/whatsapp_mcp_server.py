#!/usr/bin/env python3
"""
WhatsApp MCP Server for Personal AI Employee
Lightweight version using pywhatkit

Provides tools for:
- Sending WhatsApp messages
- Checking monitor status
- Listing recent chats

Memory usage: ~30-40 MB (lightweight!)
"""

import json
import sys
import pywhatkit as kit
from datetime import datetime
from pathlib import Path

# Configuration
WHATSAPP_INBOX = Path(__file__).parent / "whatsapp_inbox"
VAULT_PATH = Path(__file__).parent.parent / "AI_Employee_Vault"
NEEDS_ACTION_PATH = VAULT_PATH / "Needs_Action"


def log_error(message: str):
    """Log error to stderr"""
    print(json.dumps({"error": message}), file=sys.stderr)


def send_whatsapp_message(phone_number: str, message: str, hour: int = None, minute: int = None):
    """
    Send WhatsApp message using pywhatkit

    Args:
        phone_number: Phone number with country code (e.g., +923001234567)
        message: Message text
        hour: Hour to send (24-hour format, optional - sends immediately if None)
        minute: Minute to send (optional)
    """
    try:
        # Validate phone number
        if not phone_number.startswith('+'):
            return {
                "success": False,
                "error": "Phone number must start with + and country code (e.g., +923001234567)"
            }

        # Send immediately (1 minute from now)
        if hour is None or minute is None:
            now = datetime.now()
            hour = now.hour
            minute = now.minute + 1

            if minute >= 60:
                minute = 0
                hour += 1
            if hour >= 24:
                hour = 0

        # Send message
        kit.sendwhatmsg(phone_number, message, hour, minute, wait_time=15, tab_close=True)

        return {
            "success": True,
            "message": f"WhatsApp message scheduled to {phone_number}",
            "scheduled_time": f"{hour:02d}:{minute:02d}",
            "note": "WhatsApp Web will open automatically. Keep browser open until message is sent."
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def get_monitor_status():
    """Get WhatsApp monitor status"""
    try:
        # Check if inbox exists
        inbox_exists = WHATSAPP_INBOX.exists()

        # Count files in inbox
        if inbox_exists:
            txt_files = list(WHATSAPP_INBOX.glob("*.txt"))
            file_count = len(txt_files)
        else:
            file_count = 0

        # Count WhatsApp action files
        whatsapp_actions = list(NEEDS_ACTION_PATH.glob("WHATSAPP-*.md"))
        action_count = len(whatsapp_actions)

        return {
            "success": True,
            "inbox_exists": inbox_exists,
            "inbox_path": str(WHATSAPP_INBOX),
            "pending_exports": file_count,
            "action_files_created": action_count,
            "status": "Ready" if inbox_exists else "Setup required"
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def list_recent_chats():
    """List recent WhatsApp chats in Needs_Action"""
    try:
        whatsapp_files = sorted(
            NEEDS_ACTION_PATH.glob("WHATSAPP-*.md"),
            key=lambda x: x.stat().st_mtime,
            reverse=True
        )[:10]

        chats = []
        for file in whatsapp_files:
            # Extract chat name from filename
            name = file.stem.replace('WHATSAPP-', '').split('-', 1)[-1]
            chats.append({
                "filename": file.name,
                "chat_name": name,
                "created": datetime.fromtimestamp(file.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")
            })

        return {
            "success": True,
            "total_chats": len(chats),
            "recent_chats": chats
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def handle_request(request: dict) -> dict:
    """Handle MCP tool request"""
    tool = request.get("tool")
    params = request.get("params", {})

    if tool == "send_whatsapp":
        return send_whatsapp_message(
            phone_number=params.get("phone_number"),
            message=params.get("message"),
            hour=params.get("hour"),
            minute=params.get("minute")
        )

    elif tool == "whatsapp_status":
        return get_monitor_status()

    elif tool == "list_whatsapp_chats":
        return list_recent_chats()

    else:
        return {
            "success": False,
            "error": f"Unknown tool: {tool}"
        }


def main():
    """Main MCP server loop"""
    print(json.dumps({
        "name": "whatsapp_server",
        "version": "1.0.0",
        "tools": [
            {
                "name": "send_whatsapp",
                "description": "Send WhatsApp message to a phone number",
                "parameters": {
                    "phone_number": "Phone number with country code (e.g., +923001234567)",
                    "message": "Message text to send",
                    "hour": "Hour to send (optional, 24-hour format)",
                    "minute": "Minute to send (optional)"
                }
            },
            {
                "name": "whatsapp_status",
                "description": "Check WhatsApp monitor status",
                "parameters": {}
            },
            {
                "name": "list_whatsapp_chats",
                "description": "List recent WhatsApp chats in Needs_Action folder",
                "parameters": {}
            }
        ]
    }))
    sys.stdout.flush()

    # Read requests from stdin
    for line in sys.stdin:
        try:
            request = json.loads(line.strip())
            response = handle_request(request)
            print(json.dumps(response))
            sys.stdout.flush()
        except Exception as e:
            print(json.dumps({"success": False, "error": str(e)}))
            sys.stdout.flush()


if __name__ == "__main__":
    main()
