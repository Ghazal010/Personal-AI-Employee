#!/bin/bash
# LinkedIn Setup Script
# First-time setup for LinkedIn posting

echo "💼 LinkedIn Integration Setup"
echo "=============================="
echo ""

PROJECT_DIR="/Users/user/Documents/GitHub/Personal AI Employee"

echo "Step 1: Check Playwright Installation"
echo "-------------------------------------"
if python3 -c "import playwright" 2>/dev/null; then
    echo "✅ Playwright already installed"
else
    echo "📝 Installing Playwright..."
    pip3 install playwright
    echo "📝 Installing browsers..."
    playwright install chromium
    echo "✅ Playwright installed!"
fi
echo ""

echo "Step 2: First-Time LinkedIn Login"
echo "---------------------------------"
echo "A browser window will open with LinkedIn."
echo ""
echo "Please:"
echo "1. Log in to your LinkedIn account"
echo "2. Complete any security checks if prompted"
echo "3. Wait for the feed to load"
echo ""
echo "The session will be saved for future use."
echo ""
read -p "Press Enter to start..."

cd "$PROJECT_DIR"
python3 watcher/linkedin_poster.py

echo ""
echo "✅ LinkedIn integration complete!"
echo ""
echo "To post to LinkedIn:"
echo "1. Generate a post: claude code"
echo "   Ask: 'Generate a LinkedIn post about [topic]'"
echo "2. Review post in Pending_Approval/"
echo "3. Move to Approved/ if you approve"
echo "4. Run: ./scripts/post-linkedin.sh"
echo ""
echo "⚠️  WARNING: LinkedIn automation may violate Terms of Service"
echo "Use at your own risk. For production, use LinkedIn API."
