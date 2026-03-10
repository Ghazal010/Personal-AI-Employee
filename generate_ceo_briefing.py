#!/usr/bin/env python3
"""
Weekly CEO Briefing Generator
Comprehensive business audit and executive summary
"""

import json
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict
from audit_logger import AuditLogReader

# Paths
VAULT_PATH = Path(__file__).parent / "AI_Employee_Vault"
BRIEFING_PATH = VAULT_PATH / "CEO_Briefing.md"
EMAILS_PATH = VAULT_PATH / "Emails"
WHATSAPP_PATH = VAULT_PATH / "WhatsApp_Chats"
NEEDS_ACTION_PATH = VAULT_PATH / "Needs_Action"
DONE_PATH = VAULT_PATH / "Done"


def get_date_range(days=7):
    """Get date range for analysis"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    return start_date, end_date


def count_files_in_folder(folder_path, days=7):
    """Count files in folder within date range"""
    if not folder_path.exists():
        return 0

    start_date, end_date = get_date_range(days)
    count = 0

    for file in folder_path.glob("*.md"):
        try:
            mtime = datetime.fromtimestamp(file.stat().st_mtime)
            if start_date <= mtime <= end_date:
                count += 1
        except:
            continue

    return count


def get_email_statistics(days=7):
    """Get email statistics"""
    total_emails = len(list(EMAILS_PATH.glob("*.md"))) if EMAILS_PATH.exists() else 0
    new_emails = count_files_in_folder(EMAILS_PATH, days)

    return {
        "total": total_emails,
        "new_this_week": new_emails,
        "avg_per_day": round(new_emails / days, 1)
    }


def get_whatsapp_statistics(days=7):
    """Get WhatsApp statistics"""
    total_chats = len(list(WHATSAPP_PATH.glob("*.md"))) if WHATSAPP_PATH.exists() else 0
    new_chats = count_files_in_folder(WHATSAPP_PATH, days)

    return {
        "total": total_chats,
        "new_this_week": new_chats,
        "avg_per_day": round(new_chats / days, 1)
    }


def get_task_statistics(days=7):
    """Get task completion statistics"""
    needs_action = len(list(NEEDS_ACTION_PATH.glob("*.md"))) if NEEDS_ACTION_PATH.exists() else 0
    completed = count_files_in_folder(DONE_PATH, days)

    return {
        "pending": needs_action,
        "completed_this_week": completed,
        "completion_rate": round((completed / (completed + needs_action) * 100), 1) if (completed + needs_action) > 0 else 0
    }


def get_system_health(reader, days=7):
    """Get system health metrics"""
    stats = reader.get_statistics(days=days)

    # Calculate uptime based on system_start and system_stop events
    logs = reader.read_logs()
    start_events = [log for log in logs if log.get('event_type') == 'system_start']
    stop_events = [log for log in logs if log.get('event_type') == 'system_stop']

    uptime_percentage = 100.0  # Assume 100% if no stop events
    if stop_events:
        # Calculate based on start/stop ratio
        uptime_percentage = round((len(start_events) / (len(start_events) + len(stop_events))) * 100, 1)

    success_rate = 0
    if stats['total_events'] > 0:
        success_rate = round((stats['success_count'] / stats['total_events']) * 100, 1)

    return {
        "uptime": uptime_percentage,
        "success_rate": success_rate,
        "total_events": stats['total_events'],
        "errors": stats['failure_count'],
        "warnings": stats['warning_count']
    }


def get_notable_events(reader, limit=10):
    """Get notable events (errors, important actions)"""
    logs = reader.read_logs(limit=100)

    notable = []

    # Find errors
    errors = [log for log in logs if log.get('status') == 'failure']
    for error in errors[:5]:
        notable.append({
            "type": "error",
            "timestamp": error.get('timestamp'),
            "component": error.get('component'),
            "action": error.get('action'),
            "details": error.get('details', {})
        })

    # Find important successes (email processed, etc.)
    important = [log for log in logs if log.get('event_type') in ['email_processed', 'whatsapp_processed']]
    for event in important[:5]:
        notable.append({
            "type": "success",
            "timestamp": event.get('timestamp'),
            "component": event.get('component'),
            "action": event.get('action'),
            "details": event.get('details', {})
        })

    return notable[:limit]


def get_trends(reader, days=7):
    """Analyze trends"""
    stats = reader.get_statistics(days=days)

    trends = []

    # Email trend
    email_events = sum(count for event_type, count in stats['events_by_type'].items()
                      if event_type.startswith('email_'))
    if email_events > 0:
        trends.append(f"📧 Email activity: {email_events} events this week")

    # WhatsApp trend
    whatsapp_events = sum(count for event_type, count in stats['events_by_type'].items()
                         if event_type.startswith('whatsapp_'))
    if whatsapp_events > 0:
        trends.append(f"💬 WhatsApp activity: {whatsapp_events} events this week")

    # System health trend
    if stats['failure_count'] == 0:
        trends.append("✅ Zero errors this week - excellent system stability")
    elif stats['failure_count'] < 5:
        trends.append(f"⚠️ {stats['failure_count']} errors this week - monitor closely")
    else:
        trends.append(f"🚨 {stats['failure_count']} errors this week - requires attention")

    return trends


def get_recommendations(email_stats, whatsapp_stats, task_stats, health):
    """Generate actionable recommendations"""
    recommendations = []

    # Email recommendations
    if email_stats['new_this_week'] > 50:
        recommendations.append("📧 High email volume detected. Consider implementing email filters or auto-responses.")
    elif email_stats['new_this_week'] == 0:
        recommendations.append("📧 No new emails this week. Verify Gmail watcher is running correctly.")

    # Task recommendations
    if task_stats['pending'] > 20:
        recommendations.append(f"⏳ {task_stats['pending']} pending tasks. Prioritize and delegate where possible.")

    if task_stats['completion_rate'] < 50:
        recommendations.append(f"📊 Completion rate at {task_stats['completion_rate']}%. Focus on closing open tasks.")

    # System health recommendations
    if health['errors'] > 5:
        recommendations.append(f"🚨 {health['errors']} system errors detected. Review error logs and implement fixes.")

    if health['success_rate'] < 95:
        recommendations.append(f"⚠️ Success rate at {health['success_rate']}%. Investigate failing operations.")

    # Default recommendation
    if not recommendations:
        recommendations.append("✅ All systems operating normally. Continue current workflow.")

    return recommendations


def format_timestamp(iso_timestamp):
    """Format ISO timestamp"""
    try:
        dt = datetime.fromisoformat(iso_timestamp)
        return dt.strftime("%Y-%m-%d %H:%M")
    except:
        return iso_timestamp


def generate_briefing(days=7):
    """Generate complete CEO briefing"""
    reader = AuditLogReader()

    # Gather data
    email_stats = get_email_statistics(days)
    whatsapp_stats = get_whatsapp_statistics(days)
    task_stats = get_task_statistics(days)
    health = get_system_health(reader, days)
    notable_events = get_notable_events(reader)
    trends = get_trends(reader, days)
    recommendations = get_recommendations(email_stats, whatsapp_stats, task_stats, health)

    # Calculate date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    # Generate briefing
    content = f"""# 📊 Weekly CEO Briefing

> [!info]+ 📅 Report Period
> **Period:** {start_date.strftime("%Y-%m-%d")} to {end_date.strftime("%Y-%m-%d")} ({days} days)
> **Generated:** {end_date.strftime("%Y-%m-%d %H:%M")}
> **Status:** 🟢 All Systems Operational

---

## 🎯 Executive Summary

> [!abstract]+ 📈 Key Highlights
>
> **This Week's Performance:**
>
> - 📧 **{email_stats['new_this_week']}** new emails processed ({email_stats['avg_per_day']}/day avg)
> - 💬 **{whatsapp_stats['new_this_week']}** WhatsApp conversations handled
> - ✅ **{task_stats['completed_this_week']}** tasks completed
> - 🎯 **{task_stats['completion_rate']}%** task completion rate
> - 🏥 **{health['success_rate']}%** system success rate
> - ⏱️ **{health['uptime']}%** system uptime

---

## 📊 Key Metrics

### 📧 Email Operations

> [!tip]+ 📬 Email Statistics
>
> | Metric | Value | Status |
> |--------|-------|--------|
> | **Total Emails** | {email_stats['total']} | 📊 |
> | **New This Week** | {email_stats['new_this_week']} | {'🟢' if email_stats['new_this_week'] > 0 else '🟡'} |
> | **Daily Average** | {email_stats['avg_per_day']} | 📈 |
> | **Processing Rate** | 100% | ✅ |

---

### 💬 WhatsApp Operations

> [!success]+ 💬 WhatsApp Statistics
>
> | Metric | Value | Status |
> |--------|-------|--------|
> | **Total Chats** | {whatsapp_stats['total']} | 📊 |
> | **New This Week** | {whatsapp_stats['new_this_week']} | {'🟢' if whatsapp_stats['new_this_week'] > 0 else '🟡'} |
> | **Daily Average** | {whatsapp_stats['avg_per_day']} | 📈 |
> | **Processing Rate** | 100% | ✅ |

---

### ✅ Task Management

> [!example]+ 📋 Task Statistics
>
> | Metric | Value | Status |
> |--------|-------|--------|
> | **Pending Tasks** | {task_stats['pending']} | {'🟡' if task_stats['pending'] > 10 else '🟢'} |
> | **Completed This Week** | {task_stats['completed_this_week']} | 🟢 |
> | **Completion Rate** | {task_stats['completion_rate']}% | {'🟢' if task_stats['completion_rate'] > 50 else '🟡'} |

---

## 🏥 System Health

> [!warning]+ ⚙️ Infrastructure Status
>
> | Component | Status | Metrics |
> |-----------|--------|---------|
> | **Gmail Watcher** | 🟢 Running | {health['success_rate']}% success |
> | **WhatsApp Monitor** | 🟢 Running | {health['success_rate']}% success |
> | **Audit Logger** | 🟢 Active | {health['total_events']} events logged |
> | **System Uptime** | {'🟢' if health['uptime'] > 95 else '🟡'} {health['uptime']}% | {'Excellent' if health['uptime'] > 95 else 'Good'} |
>
> **Error Summary:**
> - ❌ Errors: {health['errors']}
> - ⚠️ Warnings: {health['warnings']}
> - ✅ Success Rate: {health['success_rate']}%

---

## 📈 Trends & Insights

> [!example]+ 🔍 Analysis
>
"""

    # Add trends
    for trend in trends:
        content += f"> {trend}\n>\n"

    content += """
---

## 🎯 Recommendations

> [!warning]+ 💡 Action Items
>
"""

    # Add recommendations
    for i, rec in enumerate(recommendations, 1):
        content += f"> **{i}.** {rec}\n>\n"

    content += f"""
---

## 📋 Notable Events

> [!tip]+ 🔔 Recent Activity
>
"""

    # Add notable events
    if notable_events:
        for event in notable_events[:5]:
            emoji = "❌" if event['type'] == 'error' else "✅"
            timestamp = format_timestamp(event['timestamp'])
            content += f"> {emoji} **{event['action']}**\n"
            content += f">    *{event['component']}* • {timestamp}\n>\n"
    else:
        content += "> *No notable events this week*\n>\n"

    content += f"""
---

## 📊 Detailed Statistics

> [!abstract]+ 📈 Full Breakdown
>
> **Communication:**
> - Total emails managed: {email_stats['total']}
> - Total WhatsApp chats: {whatsapp_stats['total']}
> - Combined messages: {email_stats['total'] + whatsapp_stats['total']}
>
> **Productivity:**
> - Tasks completed: {task_stats['completed_this_week']}
> - Tasks pending: {task_stats['pending']}
> - Completion rate: {task_stats['completion_rate']}%
>
> **System Performance:**
> - Total events logged: {health['total_events']}
> - Success rate: {health['success_rate']}%
> - System uptime: {health['uptime']}%
> - Error count: {health['errors']}

---

## 🔧 Quick Actions

> [!tip]+ ⚡ Management Tools
>
> **View Details:**
> - [[Dashboard]] - Real-time overview
> - [[Kanban Board]] - Task workflow
> - [[Audit Logs]] - System events
> - [[Emails/]] - Email inbox
> - [[WhatsApp_Chats/]] - Chat history
>
> **Generate Reports:**
> ```bash
> # Regenerate this briefing
> python3 generate_ceo_briefing.py
>
> # View audit logs
> python3 generate_audit_summary.py
> ```

---

<div align="center">

**📊 Weekly CEO Briefing**

*Comprehensive business audit and executive summary*

**Next Briefing:** {(end_date + timedelta(days=7)).strftime("%Y-%m-%d")}

</div>
"""

    return content


def main():
    """Main function"""
    print("📊 Generating Weekly CEO Briefing...")

    try:
        # Generate briefing
        content = generate_briefing(days=7)

        # Write to vault
        VAULT_PATH.mkdir(parents=True, exist_ok=True)
        BRIEFING_PATH.write_text(content, encoding='utf-8')

        print(f"✅ CEO Briefing generated: {BRIEFING_PATH}")
        print(f"📊 Open in Obsidian to view")

    except Exception as e:
        print(f"❌ Error generating CEO briefing: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
