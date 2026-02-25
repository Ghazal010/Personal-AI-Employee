#!/bin/bash
# Cron Jobs Setup Script
# Adds all automation jobs to crontab

echo "⏰ Cron Jobs Setup"
echo "=================="
echo ""

PROJECT_DIR="/Users/user/Documents/GitHub/Personal AI Employee"

echo "This will add the following cron jobs:"
echo ""
echo "1. File watcher - Continuous (on boot)"
echo "2. Process approvals - Every hour"
echo "3. Daily briefing - 8 AM daily"
echo "4. Weekly audit - Monday 8 AM"
echo ""
read -p "Continue? (y/n) " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Setup cancelled."
    exit 0
fi

# Create temporary cron file
TEMP_CRON=$(mktemp)

# Get existing crontab (if any)
crontab -l > "$TEMP_CRON" 2>/dev/null || true

# Add our cron jobs (if not already present)
if ! grep -q "Personal AI Employee" "$TEMP_CRON"; then
    cat >> "$TEMP_CRON" << EOF

# Personal AI Employee - Automation Jobs
# Added: $(date)

# File watcher - runs continuously on boot
@reboot cd "$PROJECT_DIR" && python3 watcher/simple_watcher.py >> watcher/logs/watcher.log 2>&1

# Process approvals - every hour
0 * * * * cd "$PROJECT_DIR" && ./scripts/process-approvals.sh >> watcher/logs/approvals.log 2>&1

# Daily briefing - 8 AM every day
0 8 * * * cd "$PROJECT_DIR" && ./scripts/daily-briefing.sh >> watcher/logs/briefing.log 2>&1

# Weekly audit - Monday 8 AM
0 8 * * 1 cd "$PROJECT_DIR" && ./scripts/weekly-audit.sh >> watcher/logs/audit.log 2>&1

EOF

    # Install new crontab
    crontab "$TEMP_CRON"

    echo "✅ Cron jobs installed!"
    echo ""
    echo "Installed jobs:"
    echo "  - File watcher (on boot)"
    echo "  - Process approvals (hourly)"
    echo "  - Daily briefing (8 AM)"
    echo "  - Weekly audit (Monday 8 AM)"
    echo ""
    echo "View cron jobs:"
    echo "  crontab -l"
    echo ""
    echo "Logs will be saved to:"
    echo "  $PROJECT_DIR/watcher/logs/"

else
    echo "⚠️  Cron jobs already installed!"
    echo ""
    echo "Current crontab:"
    crontab -l | grep -A 10 "Personal AI Employee"
fi

# Cleanup
rm "$TEMP_CRON"

# Create logs directory
mkdir -p "$PROJECT_DIR/watcher/logs"

echo ""
echo "✅ Setup complete!"
