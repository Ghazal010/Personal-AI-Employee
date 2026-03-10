#!/usr/bin/env python3
"""
Generate Audit Log Summary for Obsidian Dashboard
Reads audit logs and creates markdown summaries
"""

import json
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict
from audit_logger import AuditLogReader

# Paths
VAULT_PATH = Path(__file__).parent / "AI_Employee_Vault"
AUDIT_SUMMARY_PATH = VAULT_PATH / "Audit_Logs.md"


def format_timestamp(iso_timestamp):
    """Format ISO timestamp to readable format"""
    try:
        dt = datetime.fromisoformat(iso_timestamp)
        now = datetime.now()
        diff = now - dt

        if diff.total_seconds() < 60:
            return "Just now"
        elif diff.total_seconds() < 3600:
            mins = int(diff.total_seconds() / 60)
            return f"{mins}m ago"
        elif diff.total_seconds() < 86400:
            hours = int(diff.total_seconds() / 3600)
            return f"{hours}h ago"
        else:
            return dt.strftime("%Y-%m-%d %H:%M")
    except:
        return iso_timestamp


def get_event_emoji(event_type):
    """Get emoji for event type"""
    emoji_map = {
        "email_received": "📧",
        "email_sent": "📤",
        "email_processed": "✅",
        "email_error": "❌",
        "whatsapp_received": "💬",
        "whatsapp_sent": "📱",
        "whatsapp_processed": "✅",
        "whatsapp_error": "❌",
        "system_start": "🚀",
        "system_stop": "🛑",
        "system_error": "⚠️",
        "system_health_check": "🏥",
        "auth_success": "🔐",
        "auth_failure": "🔒",
        "file_created": "📄",
        "file_moved": "📁",
        "file_deleted": "🗑️",
    }
    return emoji_map.get(event_type, "📋")


def get_status_emoji(status):
    """Get emoji for status"""
    if status == "success":
        return "✅"
    elif status == "failure":
        return "❌"
    elif status == "warning":
        return "⚠️"
    else:
        return "ℹ️"


def generate_recent_events(reader, limit=20):
    """Generate recent events section"""
    logs = reader.read_logs(limit=limit)

    if not logs:
        return "*No audit events recorded yet*\n"

    output = ""
    for log in reversed(logs):  # Most recent first
        emoji = get_event_emoji(log.get('event_type', ''))
        status_emoji = get_status_emoji(log.get('status', ''))
        timestamp = format_timestamp(log.get('timestamp', ''))
        component = log.get('component', 'unknown')
        action = log.get('action', 'Unknown action')

        output += f"{emoji} **{action}** {status_emoji}\n"
        output += f"   *{component}* • {timestamp}\n\n"

    return output


def generate_statistics(reader, days=7):
    """Generate statistics section"""
    stats = reader.get_statistics(days=days)

    output = f"**Last {days} Days**\n\n"
    output += f"- **Total Events:** {stats['total_events']}\n"
    output += f"- **Success:** {stats['success_count']} ✅\n"
    output += f"- **Failures:** {stats['failure_count']} ❌\n"
    output += f"- **Warnings:** {stats['warning_count']} ⚠️\n\n"

    # Success rate
    if stats['total_events'] > 0:
        success_rate = (stats['success_count'] / stats['total_events']) * 100
        output += f"- **Success Rate:** {success_rate:.1f}%\n\n"

    return output


def generate_component_breakdown(reader, days=7):
    """Generate component breakdown"""
    stats = reader.get_statistics(days=days)

    output = "**By Component:**\n\n"

    for component, count in sorted(stats['events_by_component'].items(),
                                   key=lambda x: x[1], reverse=True):
        output += f"- **{component}:** {count} events\n"

    output += "\n"
    return output


def generate_event_type_breakdown(reader, days=7):
    """Generate event type breakdown"""
    stats = reader.get_statistics(days=days)

    output = "**By Event Type:**\n\n"

    # Group by category
    email_events = {}
    whatsapp_events = {}
    system_events = {}
    other_events = {}

    for event_type, count in stats['events_by_type'].items():
        if event_type.startswith('email_'):
            email_events[event_type] = count
        elif event_type.startswith('whatsapp_'):
            whatsapp_events[event_type] = count
        elif event_type.startswith('system_') or event_type.startswith('auth_'):
            system_events[event_type] = count
        else:
            other_events[event_type] = count

    if email_events:
        output += "📧 **Email Events:**\n"
        for event_type, count in sorted(email_events.items(), key=lambda x: x[1], reverse=True):
            emoji = get_event_emoji(event_type)
            output += f"  {emoji} {event_type.replace('_', ' ').title()}: {count}\n"
        output += "\n"

    if whatsapp_events:
        output += "💬 **WhatsApp Events:**\n"
        for event_type, count in sorted(whatsapp_events.items(), key=lambda x: x[1], reverse=True):
            emoji = get_event_emoji(event_type)
            output += f"  {emoji} {event_type.replace('_', ' ').title()}: {count}\n"
        output += "\n"

    if system_events:
        output += "⚙️ **System Events:**\n"
        for event_type, count in sorted(system_events.items(), key=lambda x: x[1], reverse=True):
            emoji = get_event_emoji(event_type)
            output += f"  {emoji} {event_type.replace('_', ' ').title()}: {count}\n"
        output += "\n"

    return output


def generate_audit_summary():
    """Generate complete audit summary markdown"""
    reader = AuditLogReader()

    content = f"""# 📊 Audit Logs

> [!info]+ 🎮 Navigation
> **Views:** [[Dashboard]] | [[Kanban Board]] | [[Audit Logs]] (Current)
> **Last Updated:** {datetime.now().strftime("%Y-%m-%d %H:%M")} | **Status:** 🟢 Logging Active

---

## 📈 Statistics

> [!abstract]+ 📊 Overview
>
> {generate_statistics(reader, days=7)}

---

## 🔍 Recent Events

> [!tip]+ 📋 Last 20 Events
>
> {generate_recent_events(reader, limit=20)}

---

## 📊 Breakdown

> [!example]+ 🏢 Component Activity
>
> {generate_component_breakdown(reader, days=7)}

---

> [!example]+ 📋 Event Types
>
> {generate_event_type_breakdown(reader, days=7)}

---

## 🔧 Actions

> [!warning]+ ⚡ Quick Actions
>
> **View Logs:**
> - Full audit log: `logs/audit.jsonl`
> - Gmail watcher: `logs/gmail-watcher-detailed.log`
> - WhatsApp monitor: `logs/whatsapp-monitor-detailed.log`
>
> **Generate Report:**
> ```bash
> python3 generate_audit_summary.py
> ```
>
> **View Raw Logs:**
> ```bash
> tail -f logs/audit.jsonl | jq
> ```

---

<div align="center">

**📊 Comprehensive Audit Logging System**

*All system events tracked and logged*

</div>
"""

    return content


def main():
    """Main function"""
    print("🔍 Generating audit log summary...")

    try:
        # Generate summary
        content = generate_audit_summary()

        # Write to vault
        VAULT_PATH.mkdir(parents=True, exist_ok=True)
        AUDIT_SUMMARY_PATH.write_text(content, encoding='utf-8')

        print(f"✅ Audit summary generated: {AUDIT_SUMMARY_PATH}")
        print(f"📊 Open in Obsidian to view")

    except Exception as e:
        print(f"❌ Error generating audit summary: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
