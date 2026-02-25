# Cron Job Setup for Personal AI Employee

## 📅 Automated Scheduling

This document explains how to set up automated scheduling for the Personal AI Employee system.

---

## 🔧 Cron Jobs (macOS/Linux)

### Installation

1. **Open crontab editor:**
   ```bash
   crontab -e
   ```

2. **Add the following lines:**
   ```bash
   # Personal AI Employee - Automated Tasks

   # File system watcher - Every 30 seconds (runs continuously, so start once)
   @reboot cd /Users/user/Documents/GitHub/Personal\ AI\ Employee && ./start.sh >> logs/watcher.log 2>&1

   # Process approvals - Every hour
   0 * * * * cd /Users/user/Documents/GitHub/Personal\ AI\ Employee && ./scripts/process-approvals.sh >> logs/approvals.log 2>&1

   # Daily briefing - Every day at 8 AM
   0 8 * * * cd /Users/user/Documents/GitHub/Personal\ AI\ Employee && ./scripts/daily-briefing.sh >> logs/daily-briefing.log 2>&1

   # Weekly audit - Every Monday at 8 AM
   0 8 * * 1 cd /Users/user/Documents/GitHub/Personal\ AI\ Employee && ./scripts/weekly-audit.sh >> logs/weekly-audit.log 2>&1

   # Gmail watcher - Every 2 minutes (when credentials available)
   # */2 * * * * cd /Users/user/Documents/GitHub/Personal\ AI\ Employee && python3 watcher/gmail_watcher.py >> logs/gmail-watcher.log 2>&1

   # WhatsApp watcher - Every 30 seconds (when credentials available)
   # * * * * * cd /Users/user/Documents/GitHub/Personal\ AI\ Employee && python3 watcher/whatsapp_watcher.py >> logs/whatsapp-watcher.log 2>&1
   ```

3. **Save and exit** (in vim: press `Esc`, type `:wq`, press Enter)

4. **Verify cron jobs:**
   ```bash
   crontab -l
   ```

---

## 📋 Schedule Overview

| Task | Frequency | Time | Purpose |
|------|-----------|------|---------|
| File Watcher | Continuous | On boot | Monitor Inbox folder |
| Process Approvals | Hourly | Every hour | Execute approved items |
| Daily Briefing | Daily | 8:00 AM | Morning CEO briefing |
| Weekly Audit | Weekly | Mon 8:00 AM | Weekly business review |
| Gmail Watcher | Every 2 min | - | Monitor email (when enabled) |
| WhatsApp Watcher | Every 30 sec | - | Monitor messages (when enabled) |

---

## 🪟 Windows Task Scheduler

### Setup Instructions

1. **Open Task Scheduler:**
   - Press `Win + R`
   - Type `taskschd.msc`
   - Press Enter

2. **Create Basic Task:**
   - Click "Create Basic Task"
   - Name: "Personal AI Employee - Daily Briefing"
   - Trigger: Daily at 8:00 AM
   - Action: Start a program
   - Program: `bash`
   - Arguments: `/c/Users/user/Documents/GitHub/Personal AI Employee/scripts/daily-briefing.sh`

3. **Repeat for other tasks:**
   - Process Approvals (Hourly)
   - Weekly Audit (Weekly, Monday 8 AM)
   - File Watcher (At startup)

---

## 📝 Log Files

All automated tasks log to the `logs/` directory:

```
logs/
├── watcher.log           # File system watcher output
├── approvals.log         # Approval processing log
├── daily-briefing.log    # Daily briefing generation log
├── weekly-audit.log      # Weekly audit log
├── gmail-watcher.log     # Gmail monitoring (when enabled)
└── whatsapp-watcher.log  # WhatsApp monitoring (when enabled)
```

**View logs:**
```bash
# View latest watcher activity
tail -f logs/watcher.log

# View daily briefing logs
tail -f logs/daily-briefing.log

# View all logs
tail -f logs/*.log
```

---

## 🔍 Monitoring

### Check if cron jobs are running:
```bash
# View cron jobs
crontab -l

# Check system logs
grep CRON /var/log/syslog

# Check if watcher is running
ps aux | grep watcher
```

### Manual execution:
```bash
# Test daily briefing
./scripts/daily-briefing.sh

# Test approval processing
./scripts/process-approvals.sh

# Test weekly audit
./scripts/weekly-audit.sh
```

---

## ⚙️ Configuration

### Adjust timing:

**Cron syntax:**
```
* * * * * command
│ │ │ │ │
│ │ │ │ └─── Day of week (0-7, 0 and 7 are Sunday)
│ │ │ └───── Month (1-12)
│ │ └─────── Day of month (1-31)
│ └───────── Hour (0-23)
└─────────── Minute (0-59)
```

**Examples:**
- `0 8 * * *` - Every day at 8 AM
- `*/30 * * * *` - Every 30 minutes
- `0 */2 * * *` - Every 2 hours
- `0 8 * * 1` - Every Monday at 8 AM
- `0 0 1 * *` - First day of every month at midnight

---

## 🚨 Troubleshooting

### Cron job not running:

1. **Check cron service:**
   ```bash
   # macOS
   sudo launchctl list | grep cron

   # Linux
   sudo systemctl status cron
   ```

2. **Check permissions:**
   ```bash
   ls -la scripts/*.sh
   # Should show -rwxr-xr-x (executable)
   ```

3. **Check paths:**
   - Use absolute paths in cron jobs
   - Verify script locations

4. **Check logs:**
   ```bash
   tail -f logs/*.log
   ```

### Script errors:

1. **Test manually:**
   ```bash
   cd "/Users/user/Documents/GitHub/Personal AI Employee"
   ./scripts/daily-briefing.sh
   ```

2. **Check Claude Code:**
   ```bash
   claude --version
   which claude
   ```

3. **Check environment:**
   - Cron runs with minimal environment
   - May need to set PATH in scripts

---

## 🎯 Silver Tier Compliance

**Requirement:** Basic scheduling via cron or Task Scheduler

**Status:** ✅ Complete

**Implemented:**
- ✅ Cron job configuration documented
- ✅ Automated scripts created
- ✅ Daily briefing scheduled
- ✅ Weekly audit scheduled
- ✅ Approval processing scheduled
- ✅ Log file management
- ✅ Monitoring instructions

---

## 📚 Additional Resources

- [Cron documentation](https://man7.org/linux/man-pages/man5/crontab.5.html)
- [Crontab generator](https://crontab.guru/)
- [Task Scheduler documentation](https://docs.microsoft.com/en-us/windows/win32/taskschd/task-scheduler-start-page)

---

**Last Updated:** 2026-02-25
**Status:** Ready for use
**Next:** Enable Gmail/WhatsApp watchers when credentials available
