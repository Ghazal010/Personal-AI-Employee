# 🚀 Personal AI Employee - Quick Start

## Current Status: 50% Complete ✅

### ✅ What's Working:
1. **Email Sending** - Send emails via Claude Code or Python
2. **Dashboard Structure** - Vault folders ready
3. **MCP Server** - Email integration configured
4. **Documentation** - Complete setup guides

### ⏳ What Needs Setup:
1. **Gmail Watcher** - To receive and monitor emails
2. **Obsidian App** - To view dashboard visually

---

## 🎯 Next Steps (15 minutes)

### Step 1: Install Obsidian (5 min)
```bash
# Download and install
open https://obsidian.md/download

# After installation, open vault:
# Obsidian → Open folder as vault
# Select: /Users/user/Documents/GitHub/Personal AI Employee/AI_Employee_Vault
```

### Step 2: Gmail Watcher Setup (10 min)
Follow: `GMAIL_WATCHER_SETUP.md`

Quick version:
1. Go to: https://console.cloud.google.com/
2. Create project: "Personal AI Employee"
3. Enable Gmail API
4. Create OAuth credentials (Desktop app)
5. Download as `gmail_credentials.json`
6. Move to: `watcher/credentials/`
7. Run: `python3 watcher/gmail_watcher.py`

---

## 📧 How to Use (Daily Workflow)

### Morning:
```bash
# 1. Start Gmail Watcher
cd "/Users/user/Documents/GitHub/Personal AI Employee/watcher"
python3 gmail_watcher.py &

# 2. Open Dashboard
open -a Obsidian
```

### Send Email:
```bash
claude code
# Then type:
"Send email to someone@example.com with subject 'Hello' and body 'Message'"
```

### Check Status:
```bash
claude code
# Then type:
/vault-status
```

---

## 🎮 Quick Commands

### Email Sending (Terminal):
```bash
source ~/.ai_employee_email_config
python3 -c "
import smtplib, os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

msg = MIMEMultipart()
msg['From'] = os.environ['EMAIL_ADDRESS']
msg['To'] = 'recipient@example.com'
msg['Subject'] = 'Your Subject'
msg.attach(MIMEText('Your message', 'plain'))

server = smtplib.SMTP(os.environ['SMTP_SERVER'], int(os.environ['SMTP_PORT']))
server.starttls()
server.login(os.environ['EMAIL_ADDRESS'], os.environ['EMAIL_PASSWORD'])
server.send_message(msg)
server.quit()
print('✅ Sent!')
"
```

### Check Pending Items:
```bash
ls -la "AI_Employee_Vault/Needs_Action/"
```

### View Dashboard:
```bash
cat "AI_Employee_Vault/Dashboard.md"
```

---

## 📚 Documentation Files

- **GMAIL_WATCHER_SETUP.md** - Email receiving setup
- **DASHBOARD_GUIDE.md** - Dashboard usage guide
- **GMAIL_SETUP.md** - Email sending setup
- **QUICK_START.md** - This file

---

## 🆘 Troubleshooting

### Email not sending?
```bash
# Test credentials
source ~/.ai_employee_email_config
echo "Email: $EMAIL_ADDRESS"
echo "SMTP: $SMTP_SERVER:$SMTP_PORT"
```

### Gmail Watcher not working?
```bash
# Check if running
ps aux | grep gmail_watcher

# View logs
tail -f logs/gmail-watcher.log
```

### Dashboard not visible?
```bash
# Check vault exists
ls -la "AI_Employee_Vault/"

# Open in VS Code as alternative
code "AI_Employee_Vault/"
```

---

## ✅ Success Checklist

- [x] Email sending configured
- [x] Test email sent successfully
- [x] Dashboard structure created
- [x] Documentation complete
- [ ] Obsidian installed
- [ ] Gmail Watcher configured
- [ ] Test email received and detected
- [ ] Daily workflow established

---

## 🎉 When Everything is Setup

Your AI Employee will:
1. ✅ Monitor Gmail for important emails (every 2 min)
2. ✅ Create action items automatically
3. ✅ Update dashboard in real-time
4. ✅ Send emails on your command
5. ✅ Track all tasks and activities

**You will:**
1. Open Obsidian dashboard each morning
2. See all pending items
3. Use Claude Code to send emails
4. Move completed items to Done/
5. Stay organized effortlessly!

---

**Ready to complete setup? Start with Obsidian installation!**

Download: https://obsidian.md/download
