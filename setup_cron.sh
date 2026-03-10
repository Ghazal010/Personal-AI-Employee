#!/bin/bash
# Cron Setup Script for Personal AI Employee
# Installs scheduled tasks for automated operations

echo "=========================================="
echo "Personal AI Employee - Cron Setup"
echo "=========================================="
echo ""

# Get the project directory
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_BIN="python3"

echo "Project Directory: $PROJECT_DIR"
echo ""

# Check if Python is available
if ! command -v $PYTHON_BIN &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3."
    exit 1
fi

echo "✅ Python 3 found: $(which $PYTHON_BIN)"
echo ""

# Create cron jobs
echo "Creating cron jobs..."
echo ""

# Backup existing crontab
crontab -l > /tmp/crontab_backup_$(date +%Y%m%d_%H%M%S).txt 2>/dev/null
echo "✅ Existing crontab backed up"

# Create new crontab entries
CRON_FILE="/tmp/ai_employee_cron.txt"

cat > $CRON_FILE << EOF
# Personal AI Employee - Automated Tasks
# Generated: $(date)

# Gmail Watcher - Every 5 minutes
*/5 * * * * cd $PROJECT_DIR && $PYTHON_BIN watcher/gmail_watcher_enhanced.py >> logs/gmail_watcher.log 2>&1

# Twitter Monitor - Every 10 minutes
*/10 * * * * cd $PROJECT_DIR && $PYTHON_BIN twitter_integration/twitter_monitor.py >> logs/twitter_monitor.log 2>&1

# Facebook/Instagram Monitor - Every 15 minutes
*/15 * * * * cd $PROJECT_DIR && $PYTHON_BIN social_media_integration/facebook_instagram_monitor.py >> logs/social_monitor.log 2>&1

# Generate Plan.md - Daily at 6:00 AM
0 6 * * * cd $PROJECT_DIR && $PYTHON_BIN generate_plan.py >> logs/plan_generator.log 2>&1

# Generate CEO Briefing - Weekly on Monday at 8:00 AM
0 8 * * 1 cd $PROJECT_DIR && $PYTHON_BIN generate_ceo_briefing.py >> logs/ceo_briefing.log 2>&1

# Generate Audit Summary - Daily at 11:00 PM
0 23 * * * cd $PROJECT_DIR && $PYTHON_BIN generate_audit_summary.py >> logs/audit_summary.log 2>&1

# Ralph Wiggum Loop - Continuous (restart if stopped)
*/30 * * * * pgrep -f ralph_wiggum_loop.py > /dev/null || (cd $PROJECT_DIR && $PYTHON_BIN ralph_wiggum_loop.py >> logs/ralph_wiggum.log 2>&1 &)

# Cleanup old logs - Weekly on Sunday at 2:00 AM
0 2 * * 0 find $PROJECT_DIR/logs -name "*.log" -mtime +30 -delete

EOF

echo "Cron jobs to be installed:"
echo ""
cat $CRON_FILE
echo ""

# Ask for confirmation
read -p "Install these cron jobs? (y/n): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    # Install cron jobs
    (crontab -l 2>/dev/null; cat $CRON_FILE) | crontab -

    if [ $? -eq 0 ]; then
        echo "✅ Cron jobs installed successfully!"
        echo ""
        echo "Installed tasks:"
        echo "  • Gmail Watcher: Every 5 minutes"
        echo "  • Twitter Monitor: Every 10 minutes"
        echo "  • Social Media Monitor: Every 15 minutes"
        echo "  • Plan Generator: Daily at 6:00 AM"
        echo "  • CEO Briefing: Weekly on Monday at 8:00 AM"
        echo "  • Audit Summary: Daily at 11:00 PM"
        echo "  • Ralph Wiggum Loop: Continuous (auto-restart)"
        echo "  • Log Cleanup: Weekly on Sunday at 2:00 AM"
        echo ""
        echo "View installed cron jobs:"
        echo "  crontab -l"
        echo ""
        echo "Remove cron jobs:"
        echo "  crontab -r"
        echo ""
        echo "Logs will be saved to: $PROJECT_DIR/logs/"
    else
        echo "❌ Failed to install cron jobs"
        exit 1
    fi
else
    echo "❌ Installation cancelled"
    exit 0
fi

# Create logs directory if it doesn't exist
mkdir -p $PROJECT_DIR/logs
echo "✅ Logs directory created: $PROJECT_DIR/logs"

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Verify cron jobs: crontab -l"
echo "2. Monitor logs: tail -f logs/*.log"
echo "3. Check system status in Obsidian Dashboard"
echo ""
