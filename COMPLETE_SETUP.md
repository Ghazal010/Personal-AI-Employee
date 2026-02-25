# 🚀 Complete Setup Guide - Option 2 & 3

**Everything you need to get fully set up in 30 minutes!**

---

## 📋 Quick Overview

I've created automated setup scripts for you. Just run them in order:

```bash
cd "/Users/user/Documents/GitHub/Personal AI Employee"

# Option 2: MCP Server (5 min)
./setup.sh

# Option 3: Full Setup (25 min)
./setup-gmail.sh        # Gmail integration (7 min)
./setup-whatsapp.sh     # WhatsApp integration (5 min)
./setup-linkedin.sh     # LinkedIn integration (5 min)
./setup-cron.sh         # Cron jobs (5 min)
```

---

## 🎯 Option 2: MCP Server Setup (5 minutes)

### Automated Script:
```bash
./setup.sh
```

**What it does:**
- ✅ Tests MCP server
- ✅ Configures Claude Code settings.json
- ✅ Installs Playwright (if needed)
- ✅ Makes all scripts executable
- ✅ Checks for Gmail credentials

**Manual verification:**
```bash
# Test in Claude Code
claude code
# Ask: "Send a test email to test@example.com"
```

---

## 🎯 Option 3: Full Setup (25 minutes)

### 1. Gmail Integration (7 minutes)

```bash
./setup-gmail.sh
```

**What it does:**
- Guides you through Google Cloud setup
- Helps you enable Gmail API
- Helps you create OAuth credentials
- Runs first-time authentication
- Tests the Gmail watcher

**You need to:**
- Create Google Cloud project (2 min)
- Enable Gmail API (1 min)
- Create OAuth credentials (2 min)
- Download credentials.json (1 min)
- Authenticate in browser (1 min)

---

### 2. WhatsApp Integration (5 minutes)

```bash
./setup-whatsapp.sh
```

**What it does:**
- Installs Playwright (if needed)
- Opens WhatsApp Web in browser
- Saves session for future use

**You need to:**
- Scan QR code with your phone (1 min)
- Wait for WhatsApp to load (1 min)

---

### 3. LinkedIn Integration (5 minutes)

```bash
./setup-linkedin.sh
```

**What it does:**
- Installs Playwright (if needed)
- Opens LinkedIn in browser
- Saves session for future use

**You need to:**
- Log in to LinkedIn (2 min)
- Complete security checks if any (1 min)

---

### 4. Cron Jobs (5 minutes)

```bash
./setup-cron.sh
```

**What it does:**
- Adds all automation jobs to crontab
- Creates log directories
- Shows installed jobs

**Cron jobs installed:**
- File watcher (on boot)
- Process approvals (hourly)
- Daily briefing (8 AM)
- Weekly audit (Monday 8 AM)

---

## 📊 Setup Progress Tracker

```bash
# Check what's already set up
cd "/Users/user/Documents/GitHub/Personal AI Employee"

# MCP Server
python3 mcp_server/test_server.py

# Claude Code config
cat ~/.config/claude/settings.json

# Playwright
python3 -c "import playwright; print('✅ Installed')" 2>/dev/null || echo "❌ Not installed"

# Gmail credentials
[ -f watcher/credentials/gmail_credentials.json ] && echo "✅ Gmail ready" || echo "❌ Gmail not set up"

# Cron jobs
crontab -l | grep "Personal AI Employee" && echo "✅ Cron jobs installed" || echo "❌ Cron not set up"
```

---

## 🎯 Complete Setup Checklist

### Option 2: MCP Server ✅
- [ ] Run `./setup.sh`
- [ ] Test in Claude Code
- [ ] Verify email sending works

### Option 3: Full Setup ✅

**Gmail:**
- [ ] Run `./setup-gmail.sh`
- [ ] Create Google Cloud project
- [ ] Enable Gmail API
- [ ] Download credentials
- [ ] Authenticate
- [ ] Test watcher

**WhatsApp:**
- [ ] Run `./setup-whatsapp.sh`
- [ ] Scan QR code
- [ ] Verify connection
- [ ] Test watcher

**LinkedIn:**
- [ ] Run `./setup-linkedin.sh`
- [ ] Log in to LinkedIn
- [ ] Verify session saved
- [ ] Test posting

**Cron Jobs:**
- [ ] Run `./setup-cron.sh`
- [ ] Verify jobs installed
- [ ] Check logs directory
- [ ] Test one job manually

---

## 🚀 Quick Start (All at Once)

If you want to run everything in sequence:

```bash
cd "/Users/user/Documents/GitHub/Personal AI Employee"

# Run all setup scripts
./setup.sh && \
./setup-gmail.sh && \
./setup-whatsapp.sh && \
./setup-linkedin.sh && \
./setup-cron.sh

echo "🎉 Complete setup done!"
```

**Total time:** ~30 minutes

---

## 🧪 Verify Everything Works

After setup, test each feature:

```bash
# 1. MCP Server
claude code
# Ask: "Send a test email"

# 2. Gmail Watcher
python3 watcher/gmail_watcher.py
# Check for new emails

# 3. WhatsApp Watcher
python3 watcher/whatsapp_watcher.py
# Check for messages

# 4. LinkedIn Posting
claude code
# Ask: "Generate a LinkedIn post"
# Move to Approved/
./scripts/post-linkedin.sh

# 5. Cron Jobs
crontab -l
# Verify all jobs listed

# 6. Daily Briefing
./scripts/daily-briefing.sh
# Check Logs/ folder

# 7. Process Approvals
./scripts/process-approvals.sh
# Check Done/ folder
```

---

## 📝 What Each Script Does

### setup.sh
- Tests MCP server
- Configures Claude Code
- Installs Playwright
- Makes scripts executable

### setup-gmail.sh
- Guides through Google Cloud setup
- Helps with OAuth credentials
- Runs first-time auth
- Tests Gmail watcher

### setup-whatsapp.sh
- Installs Playwright
- Opens WhatsApp Web
- Saves session
- Tests watcher

### setup-linkedin.sh
- Installs Playwright
- Opens LinkedIn
- Saves session
- Tests posting

### setup-cron.sh
- Adds cron jobs
- Creates log directories
- Verifies installation

---

## 🎊 After Setup

**You'll have:**
- ✅ MCP server working in Claude Code
- ✅ Gmail monitoring every 2 minutes
- ✅ WhatsApp monitoring every 30 seconds
- ✅ LinkedIn auto-posting capability
- ✅ Automated daily briefings (8 AM)
- ✅ Automated approval processing (hourly)
- ✅ Automated weekly audits (Monday 8 AM)

**Silver Tier:** 100% Complete and Fully Operational! 🚀

---

## 🆘 Need Help?

**Script fails?**
- Check error message
- Verify Python version: `python3 --version`
- Check permissions: `ls -la setup.sh`

**Gmail setup issues?**
- See: GMAIL_SETUP.md
- Verify credentials file location
- Check OAuth consent screen

**Playwright issues?**
- Reinstall: `pip3 install --force-reinstall playwright`
- Install browsers: `playwright install chromium`

**Cron not working?**
- Check crontab: `crontab -l`
- Check logs: `ls -la watcher/logs/`
- Test script manually first

---

**Created:** 2026-02-25
**Status:** Ready to run!
**Time:** 30 minutes total
