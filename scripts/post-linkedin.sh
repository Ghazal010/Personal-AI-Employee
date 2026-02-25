#!/bin/bash
# LinkedIn posting script
# Run this to check for approved LinkedIn posts and publish them

cd "/Users/user/Documents/GitHub/Personal AI Employee"

echo "[$(date)] Checking for approved LinkedIn posts..."

# Check if there are any approved LinkedIn posts
APPROVED_COUNT=$(find AI_Employee_Vault/Approved -name "LINKEDIN-POST-*.md" 2>/dev/null | wc -l | xargs)

if [ "$APPROVED_COUNT" -gt 0 ]; then
    echo "[$(date)] Found $APPROVED_COUNT approved LinkedIn posts"

    # Post to LinkedIn
    python3 watcher/linkedin_poster.py

    echo "[$(date)] LinkedIn posting complete"
else
    echo "[$(date)] No approved LinkedIn posts to publish"
fi
