#!/bin/bash
# Weekly audit and CEO briefing script
# Run this every Monday at 8 AM via cron

cd "/Users/user/Documents/GitHub/Personal AI Employee"

echo "[$(date)] Starting weekly audit..."

# Generate weekly briefing
claude code --prompt "Generate a weekly CEO briefing. Review all activity from the last 7 days, analyze Business Goals progress, identify bottlenecks, calculate revenue and expenses, and create a comprehensive weekly audit report in AI_Employee_Vault/Logs/Weekly-Briefing-$(date +%Y-%m-%d).md"

echo "[$(date)] Weekly audit complete"
