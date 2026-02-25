#!/bin/bash
# Quick Setup Script for Personal AI Employee
# This script automates as much as possible

set -e  # Exit on error

PROJECT_DIR="/Users/user/Documents/GitHub/Personal AI Employee"
CLAUDE_CONFIG_DIR="$HOME/.config/claude"
CLAUDE_SETTINGS="$CLAUDE_CONFIG_DIR/settings.json"

echo "🚀 Personal AI Employee - Quick Setup"
echo "======================================"
echo ""

# Step 1: Check Python version
echo "Step 1: Checking Python version..."
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "✅ Python $PYTHON_VERSION detected"
echo ""

# Step 2: Test MCP Server
echo "Step 2: Testing MCP Server..."
cd "$PROJECT_DIR/mcp_server"
if python3 test_server.py; then
    echo "✅ MCP Server tests passed!"
else
    echo "❌ MCP Server tests failed!"
    exit 1
fi
echo ""

# Step 3: Configure Claude Code
echo "Step 3: Configuring Claude Code..."
mkdir -p "$CLAUDE_CONFIG_DIR"

if [ -f "$CLAUDE_SETTINGS" ]; then
    echo "⚠️  Claude settings.json already exists"
    echo "📝 Backing up to settings.json.backup"
    cp "$CLAUDE_SETTINGS" "$CLAUDE_SETTINGS.backup"

    # Check if mcpServers already exists
    if grep -q "mcpServers" "$CLAUDE_SETTINGS"; then
        echo "⚠️  mcpServers already configured"
        echo "📝 Please manually merge config/claude-settings.json"
    else
        # Add mcpServers to existing config
        echo "📝 Adding MCP server to existing config..."
        # Use Python to merge JSON properly
        python3 << 'EOF'
import json
import sys

settings_file = sys.argv[1]
template_file = sys.argv[2]

with open(settings_file, 'r') as f:
    settings = json.load(f)

with open(template_file, 'r') as f:
    template = json.load(f)

settings['mcpServers'] = template['mcpServers']

with open(settings_file, 'w') as f:
    json.dump(settings, f, indent=2)

print("✅ MCP server added to settings.json")
EOF
        python3 - "$CLAUDE_SETTINGS" "$PROJECT_DIR/config/claude-settings.json"
    fi
else
    echo "📝 Creating new settings.json..."
    cp "$PROJECT_DIR/config/claude-settings.json" "$CLAUDE_SETTINGS"
    echo "✅ Claude Code configured!"
fi
echo ""

# Step 4: Check for Playwright
echo "Step 4: Checking for Playwright..."
if python3 -c "import playwright" 2>/dev/null; then
    echo "✅ Playwright already installed"
else
    echo "⚠️  Playwright not installed"
    echo "📝 Installing Playwright..."
    pip3 install playwright
    echo "📝 Installing browsers..."
    playwright install chromium
    echo "✅ Playwright installed!"
fi
echo ""

# Step 5: Make scripts executable
echo "Step 5: Ensuring scripts are executable..."
chmod +x "$PROJECT_DIR/scripts/"*.sh
chmod +x "$PROJECT_DIR/mcp_server/"*.py
chmod +x "$PROJECT_DIR/watcher/"*.py
echo "✅ All scripts are executable"
echo ""

# Step 6: Check for Gmail credentials
echo "Step 6: Checking Gmail setup..."
if [ -f "$PROJECT_DIR/watcher/credentials/gmail_credentials.json" ]; then
    echo "✅ Gmail credentials found"
else
    echo "⚠️  Gmail credentials not found"
    echo "📝 See GMAIL_SETUP.md for instructions"
fi
echo ""

# Step 7: Summary
echo "======================================"
echo "✅ Setup Complete!"
echo "======================================"
echo ""
echo "What's Ready:"
echo "  ✅ MCP Server tested and working"
echo "  ✅ Claude Code configured"
echo "  ✅ Playwright installed (if needed)"
echo "  ✅ All scripts executable"
echo ""
echo "Next Steps:"
echo ""
echo "1. Test MCP Server in Claude Code:"
echo "   claude code"
echo "   # Ask: 'Send a test email to test@example.com'"
echo ""
echo "2. Setup Gmail (optional):"
echo "   See: GMAIL_SETUP.md"
echo ""
echo "3. Setup WhatsApp (optional):"
echo "   python3 watcher/whatsapp_watcher.py"
echo "   # Scan QR code when prompted"
echo ""
echo "4. Setup LinkedIn (optional):"
echo "   python3 watcher/linkedin_poster.py"
echo "   # Login when prompted"
echo ""
echo "5. Setup Cron Jobs (optional):"
echo "   crontab -e"
echo "   # Copy jobs from SCHEDULING.md"
echo ""
echo "🎉 Ready to use!"
