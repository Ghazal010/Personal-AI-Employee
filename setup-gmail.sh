#!/bin/bash
# Gmail Setup Helper Script
# Guides you through Gmail API setup

echo "📧 Gmail Integration Setup"
echo "=========================="
echo ""
echo "This script will guide you through setting up Gmail integration."
echo ""

PROJECT_DIR="/Users/user/Documents/GitHub/Personal AI Employee"
CREDS_DIR="$PROJECT_DIR/watcher/credentials"

# Create credentials directory
mkdir -p "$CREDS_DIR"

echo "Step 1: Create Google Cloud Project"
echo "-----------------------------------"
echo "1. Go to: https://console.cloud.google.com"
echo "2. Click 'Select a project' → 'New Project'"
echo "3. Name: 'Personal AI Employee'"
echo "4. Click 'Create'"
echo ""
read -p "Press Enter when project is created..."
echo ""

echo "Step 2: Enable Gmail API"
echo "------------------------"
echo "1. In Google Cloud Console, go to 'APIs & Services' → 'Library'"
echo "2. Search for 'Gmail API'"
echo "3. Click 'Gmail API' → 'Enable'"
echo ""
read -p "Press Enter when Gmail API is enabled..."
echo ""

echo "Step 3: Create OAuth Credentials"
echo "--------------------------------"
echo "1. Go to 'APIs & Services' → 'Credentials'"
echo "2. Click 'Create Credentials' → 'OAuth client ID'"
echo "3. If prompted, configure OAuth consent screen:"
echo "   - User Type: External"
echo "   - App name: Personal AI Employee"
echo "   - User support email: Your email"
echo "   - Developer contact: Your email"
echo "   - Click 'Save and Continue' through all steps"
echo "4. Back to 'Create OAuth client ID':"
echo "   - Application type: Desktop app"
echo "   - Name: Personal AI Employee Desktop"
echo "5. Click 'Create'"
echo "6. Click 'Download JSON'"
echo ""
read -p "Press Enter when you've downloaded the JSON file..."
echo ""

echo "Step 4: Move Credentials File"
echo "-----------------------------"
echo "Move the downloaded JSON file to:"
echo "$CREDS_DIR/gmail_credentials.json"
echo ""
echo "You can do this with:"
echo "mv ~/Downloads/client_secret_*.json $CREDS_DIR/gmail_credentials.json"
echo ""
read -p "Press Enter when file is moved..."
echo ""

# Check if file exists
if [ -f "$CREDS_DIR/gmail_credentials.json" ]; then
    echo "✅ Credentials file found!"
    echo ""

    echo "Step 5: First-Time Authentication"
    echo "---------------------------------"
    echo "Running Gmail watcher for first-time auth..."
    echo "A browser window will open. Please:"
    echo "1. Select your Google account"
    echo "2. Click 'Advanced' → 'Go to Personal AI Employee (unsafe)'"
    echo "3. Click 'Allow' to grant permissions"
    echo ""
    read -p "Press Enter to start authentication..."

    cd "$PROJECT_DIR"
    python3 watcher/gmail_watcher.py

    echo ""
    echo "✅ Gmail integration complete!"
    echo ""
    echo "The watcher will now check Gmail every 2 minutes."
    echo "To run it continuously:"
    echo "  python3 watcher/gmail_watcher.py"
    echo ""
    echo "Or add to cron (see SCHEDULING.md)"

else
    echo "❌ Credentials file not found!"
    echo "Please move the downloaded JSON file to:"
    echo "$CREDS_DIR/gmail_credentials.json"
    exit 1
fi
