#!/bin/bash
# Quick demo script - Shows Bronze Tier in action

echo "🤖 Personal AI Employee - Bronze Tier Demo"
echo "=========================================="
echo ""

# Check if vault exists
if [ ! -d "AI_Employee_Vault" ]; then
    echo "❌ Error: AI_Employee_Vault not found"
    exit 1
fi

echo "✅ Vault found: AI_Employee_Vault"
echo ""

# Show current status
echo "📊 Current Status:"
echo "  Inbox: $(find AI_Employee_Vault/Inbox -type f 2>/dev/null | wc -l | xargs) items"
echo "  Needs Action: $(find AI_Employee_Vault/Needs_Action -type f 2>/dev/null | wc -l | xargs) items"
echo "  Plans: $(find AI_Employee_Vault/Plans -type f 2>/dev/null | wc -l | xargs) items"
echo "  Pending Approval: $(find AI_Employee_Vault/Pending_Approval -type f 2>/dev/null | wc -l | xargs) items"
echo "  In Progress: $(find AI_Employee_Vault/In_Progress -type f 2>/dev/null | wc -l | xargs) items"
echo "  Done: $(find AI_Employee_Vault/Done -type f 2>/dev/null | wc -l | xargs) items"
echo "  Logs: $(find AI_Employee_Vault/Logs -type f 2>/dev/null | wc -l | xargs) items"
echo ""

# Show Dashboard
echo "📋 Dashboard Preview:"
echo "-------------------"
head -20 AI_Employee_Vault/Dashboard.md
echo ""
echo "-------------------"
echo ""

# Show action items
echo "⚡ Action Items:"
if [ -d "AI_Employee_Vault/Needs_Action" ]; then
    for file in AI_Employee_Vault/Needs_Action/*.md; do
        if [ -f "$file" ]; then
            echo "  - $(basename "$file")"
        fi
    done
else
    echo "  (none)"
fi
echo ""

# Show recent completions
echo "✅ Recent Completions:"
if [ -d "AI_Employee_Vault/Done" ]; then
    for file in AI_Employee_Vault/Done/*.md; do
        if [ -f "$file" ]; then
            echo "  - $(basename "$file")"
        fi
    done
else
    echo "  (none)"
fi
echo ""

echo "🎉 Bronze Tier is fully operational!"
echo ""
echo "Next steps:"
echo "  1. Run: ./start.sh (to start the watcher)"
echo "  2. Run: python3 create_samples.py (to create test data)"
echo "  3. Record your demo video"
echo "  4. Submit to hackathon!"
