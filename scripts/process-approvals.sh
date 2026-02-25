#!/bin/bash
# Process pending approvals script
# Run this every hour to check for approved/rejected items

cd "/Users/user/Documents/GitHub/Personal AI Employee"

echo "[$(date)] Checking for approval decisions..."

# Check if there are any items in Approved or Rejected folders
APPROVED_COUNT=$(find AI_Employee_Vault/Approved -type f 2>/dev/null | wc -l | xargs)
REJECTED_COUNT=$(find AI_Employee_Vault/Rejected -type f 2>/dev/null | wc -l | xargs)

if [ "$APPROVED_COUNT" -gt 0 ] || [ "$REJECTED_COUNT" -gt 0 ]; then
    echo "[$(date)] Found $APPROVED_COUNT approved and $REJECTED_COUNT rejected items"

    # Process approvals using Claude Code
    claude code --prompt "Process all approval decisions. Check Approved/ and Rejected/ folders, execute approved actions, log rejections, and update the Dashboard."

    echo "[$(date)] Approval processing complete"
else
    echo "[$(date)] No approval decisions to process"
fi
