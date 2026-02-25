#!/usr/bin/env python3
"""
Quick demo script to show Bronze Tier functionality
Creates sample inbox items and shows processing
"""

from pathlib import Path
from datetime import datetime, timedelta

INBOX = Path("AI_Employee_Vault/Inbox")

# Sample inbox items
samples = [
    {
        "filename": "meeting-request.md",
        "content": """# Meeting Request

**Date:** {date}
**From:** Sarah Johnson
**Type:** Meeting Request

## Details

Hi,

Can we schedule a meeting next week to discuss the Q1 marketing strategy?
I'm available Tuesday or Thursday afternoon.

Best regards,
Sarah

---

**Priority:** Medium
**Action Required:** Schedule meeting
""".format(date=datetime.now().strftime("%Y-%m-%d"))
    },
    {
        "filename": "expense-report.md",
        "content": """# Expense Report Submission

**Date:** {date}
**From:** Finance Department
**Type:** Expense Report

## Summary

Please review and approve the following expense report:

- **Employee:** Mike Chen
- **Period:** February 2026
- **Total:** $450.00
- **Categories:** Travel, Meals, Office Supplies

Attached: expense_report_feb2026.pdf

---

**Priority:** Medium
**Deadline:** End of month
**Action Required:** Review and approve
""".format(date=datetime.now().strftime("%Y-%m-%d"))
    },
    {
        "filename": "urgent-bug-report.md",
        "content": """# URGENT: Production Bug Report

**Date:** {date}
**From:** DevOps Team
**Type:** Bug Report

## Issue

Critical bug detected in production environment:

- **System:** Payment Gateway
- **Impact:** HIGH - Transactions failing
- **Affected Users:** ~50 users in last hour
- **Error:** Connection timeout to payment processor

## Immediate Action Needed

1. Investigate root cause
2. Implement hotfix
3. Monitor system stability
4. Notify affected customers

---

**Priority:** 🔴 CRITICAL
**Action Required:** Immediate investigation and fix
""".format(date=datetime.now().strftime("%Y-%m-%d"))
    }
]

def create_samples():
    """Create sample inbox items"""
    INBOX.mkdir(parents=True, exist_ok=True)

    print("📝 Creating sample inbox items...\n")

    for sample in samples:
        filepath = INBOX / sample["filename"]
        filepath.write_text(sample["content"])
        print(f"✅ Created: {sample['filename']}")

    print(f"\n✨ Created {len(samples)} sample items in {INBOX}")
    print("\nNext steps:")
    print("1. Run: ./start.sh (to start the watcher)")
    print("2. Or manually process with Claude Code")
    print("3. Check Dashboard.md for updates")

if __name__ == "__main__":
    create_samples()
