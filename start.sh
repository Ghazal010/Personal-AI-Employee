#!/bin/bash
# Startup script for Personal AI Employee (Bronze Tier)

set -e

echo "🤖 Personal AI Employee - Bronze Tier"
echo "======================================"
echo ""

# Check prerequisites
echo "📋 Checking prerequisites..."

if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.10+"
    exit 1
fi
echo "✅ Python 3 found"

if ! command -v uv &> /dev/null; then
    echo "❌ UV not found. Please install UV package manager"
    exit 1
fi
echo "✅ UV found"

if ! command -v claude &> /dev/null; then
    echo "❌ Claude Code not found. Please install Claude Code CLI"
    exit 1
fi
echo "✅ Claude Code found"

echo ""
echo "📁 Vault structure:"
echo "   Inbox: $(ls -1 AI_Employee_Vault/Inbox/ 2>/dev/null | wc -l | xargs) items"
echo "   Needs Action: $(ls -1 AI_Employee_Vault/Needs_Action/ 2>/dev/null | wc -l | xargs) items"
echo "   Done: $(ls -1 AI_Employee_Vault/Done/ 2>/dev/null | wc -l | xargs) items"
echo ""

echo "🚀 Starting Inbox Watcher..."
echo "   Monitoring: AI_Employee_Vault/Inbox/"
echo "   Using: Simple Watcher (notification-based)"
echo "   Press Ctrl+C to stop"
echo ""

cd watcher
python3 simple_watcher.py
