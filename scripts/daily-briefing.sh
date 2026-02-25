#!/bin/bash
# Daily briefing generation script
# Run this every morning at 8 AM via cron

cd "/Users/user/Documents/GitHub/Personal AI Employee"

echo "[$(date)] Starting daily briefing generation..."

# Generate briefing using Claude Code
claude code --prompt "Generate a daily CEO briefing. Review all activity from the last 24 hours, check pending approvals, analyze Business Goals progress, and create a comprehensive briefing report in AI_Employee_Vault/Logs/Briefing-$(date +%Y-%m-%d).md"

echo "[$(date)] Daily briefing complete"
