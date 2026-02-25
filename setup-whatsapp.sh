#!/bin/bash
# WhatsApp Setup Script
# First-time setup for WhatsApp watcher

echo "💬 WhatsApp Integration Setup"
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

echo "Step 2: First-Time WhatsApp Login"
echo "---------------------------------"
echo "A browser window will open with WhatsApp Web."
echo ""
echo "Please:"
echo "1. Open WhatsApp on your phone"
echo "2. Tap 'Settings' → 'Linked Devices'"
echo "3. Tap 'Link a Device'"
echo "4. Scan the QR code shown in the browser"
echo ""
echo "The session will be saved for future use."
echo ""
read -p "Press Enter to start..."

cd "$PROJECT_DIR"
python3 watcher/whatsapp_watcher.py

echo ""
echo "✅ WhatsApp integration complete!"
echo ""
echo "The watcher will now check WhatsApp every 30 seconds."
echo "To run it continuously:"
echo "  python3 watcher/whatsapp_watcher.py"
echo ""
echo "⚠️  WARNING: WhatsApp automation may violate Terms of Service"
echo "Use at your own risk. For production, use WhatsApp Business API."
