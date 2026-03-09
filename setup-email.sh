#!/bin/bash
# Email Configuration Helper
# Helps you set up email sending securely

echo "📧 Email Configuration Setup"
echo "============================"
echo ""

PROJECT_DIR="/Users/user/Documents/GitHub/Personal AI Employee"

echo "This script will help you configure email sending."
echo ""
echo "You need:"
echo "1. Your Gmail address"
echo "2. A Gmail App Password (NOT your regular password)"
echo ""
echo "⚠️  IMPORTANT: Never use your regular Gmail password!"
echo "   Use an App Password instead (more secure)"
echo ""

# Check if already configured
if [ -f "$HOME/.ai_employee_email_config" ]; then
    echo "⚠️  Email already configured!"
    echo ""
    read -p "Do you want to reconfigure? (y/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Setup cancelled."
        exit 0
    fi
fi

echo "Step 1: Create Gmail App Password"
echo "---------------------------------"
echo ""
echo "1. Go to: https://myaccount.google.com/security"
echo "2. Enable 2-Step Verification (if not already enabled)"
echo "3. Go to: https://myaccount.google.com/apppasswords"
echo "4. Select app: 'Mail'"
echo "5. Select device: 'Mac'"
echo "6. Click 'Generate'"
echo "7. Copy the 16-character password"
echo ""
read -p "Press Enter when you have your App Password ready..."
echo ""

echo "Step 2: Enter Your Email Configuration"
echo "--------------------------------------"
echo ""

read -p "Enter your Gmail address: " EMAIL_ADDRESS
echo ""

read -s -p "Enter your App Password (16 characters, no spaces): " APP_PASSWORD
echo ""
echo ""

# Validate inputs
if [ -z "$EMAIL_ADDRESS" ] || [ -z "$APP_PASSWORD" ]; then
    echo "❌ Error: Email or password cannot be empty!"
    exit 1
fi

# Save to config file (secure permissions)
CONFIG_FILE="$HOME/.ai_employee_email_config"
cat > "$CONFIG_FILE" << EOF
# Personal AI Employee - Email Configuration
# Created: $(date)
export EMAIL_ADDRESS="$EMAIL_ADDRESS"
export EMAIL_PASSWORD="$APP_PASSWORD"
export SMTP_SERVER="smtp.gmail.com"
export SMTP_PORT="587"
EOF

# Set secure permissions (only you can read)
chmod 600 "$CONFIG_FILE"

echo "✅ Configuration saved securely to: $CONFIG_FILE"
echo ""

# Update shell profile to load config
SHELL_PROFILE=""
if [ -f "$HOME/.zshrc" ]; then
    SHELL_PROFILE="$HOME/.zshrc"
elif [ -f "$HOME/.bash_profile" ]; then
    SHELL_PROFILE="$HOME/.bash_profile"
fi

if [ -n "$SHELL_PROFILE" ]; then
    if ! grep -q ".ai_employee_email_config" "$SHELL_PROFILE"; then
        echo "" >> "$SHELL_PROFILE"
        echo "# Personal AI Employee - Email Config" >> "$SHELL_PROFILE"
        echo "[ -f ~/.ai_employee_email_config ] && source ~/.ai_employee_email_config" >> "$SHELL_PROFILE"
        echo "✅ Added to $SHELL_PROFILE"
    fi
fi

echo ""
echo "Step 3: Update Claude Code Settings"
echo "-----------------------------------"
echo ""

# Update Claude Code settings to use production server
CLAUDE_SETTINGS="$HOME/.config/claude/settings.json"

if [ -f "$CLAUDE_SETTINGS" ]; then
    # Backup existing settings
    cp "$CLAUDE_SETTINGS" "$CLAUDE_SETTINGS.backup"

    # Update to use production server
    cat > "$CLAUDE_SETTINGS" << EOF
{
  "mcpServers": {
    "email": {
      "command": "python3",
      "args": [
        "$PROJECT_DIR/mcp_server/email_server_production.py"
      ],
      "env": {
        "EMAIL_ADDRESS": "$EMAIL_ADDRESS",
        "EMAIL_PASSWORD": "$APP_PASSWORD",
        "SMTP_SERVER": "smtp.gmail.com",
        "SMTP_PORT": "587"
      }
    }
  }
}
EOF

    echo "✅ Claude Code settings updated"
else
    echo "⚠️  Claude Code settings not found"
    echo "Creating new settings file..."
    mkdir -p "$HOME/.config/claude"
    cat > "$CLAUDE_SETTINGS" << EOF
{
  "mcpServers": {
    "email": {
      "command": "python3",
      "args": [
        "$PROJECT_DIR/mcp_server/email_server_production.py"
      ],
      "env": {
        "EMAIL_ADDRESS": "$EMAIL_ADDRESS",
        "EMAIL_PASSWORD": "$APP_PASSWORD",
        "SMTP_SERVER": "smtp.gmail.com",
        "SMTP_PORT": "587"
      }
    }
  }
}
EOF
    echo "✅ Claude Code settings created"
fi

echo ""
echo "Step 4: Test Email Sending"
echo "--------------------------"
echo ""

read -p "Send a test email to yourself? (y/n) " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "Testing email..."

    # Source the config
    source "$CONFIG_FILE"

    # Test with Python
    python3 << EOF
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

try:
    msg = MIMEMultipart()
    msg['From'] = os.environ['EMAIL_ADDRESS']
    msg['To'] = os.environ['EMAIL_ADDRESS']
    msg['Subject'] = 'Test Email from Personal AI Employee'
    msg.attach(MIMEText('This is a test email. Your email configuration is working!', 'plain'))

    server = smtplib.SMTP(os.environ['SMTP_SERVER'], int(os.environ['SMTP_PORT']))
    server.starttls()
    server.login(os.environ['EMAIL_ADDRESS'], os.environ['EMAIL_PASSWORD'])
    server.send_message(msg)
    server.quit()

    print("✅ Test email sent successfully!")
    print(f"Check your inbox: {os.environ['EMAIL_ADDRESS']}")
except Exception as e:
    print(f"❌ Error sending test email: {e}")
    print("\nPlease check:")
    print("1. Your email address is correct")
    print("2. Your App Password is correct (16 characters)")
    print("3. 2-Step Verification is enabled")
    print("4. App Password was generated correctly")
EOF
fi

echo ""
echo "======================================"
echo "✅ Email Configuration Complete!"
echo "======================================"
echo ""
echo "What's configured:"
echo "  ✅ Gmail App Password saved securely"
echo "  ✅ Claude Code updated to use production mode"
echo "  ✅ Environment variables configured"
echo ""
echo "Next steps:"
echo ""
echo "1. Restart your terminal (to load new config)"
echo "2. Start Claude Code: claude code"
echo "3. Test: 'Send an email to $EMAIL_ADDRESS'"
echo ""
echo "Security notes:"
echo "  - Config saved to: $CONFIG_FILE (permissions: 600)"
echo "  - Only you can read this file"
echo "  - Never commit this file to git"
echo "  - App Password is NOT your regular password"
echo ""
echo "🎉 Ready to send real emails!"
