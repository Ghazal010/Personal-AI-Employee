# 🧪 Complete Testing Guide - Verify Everything Works

## Quick Test Checklist

Run these tests to verify all Silver Tier features are working correctly.

---

## ✅ Test 1: File Structure (30 seconds)

```bash
cd "/Users/user/Documents/GitHub/Personal AI Employee"

# Check all folders exist
ls -la AI_Employee_Vault/

# Should show:
# - Inbox/
# - Needs_Action/
# - Pending_Approval/
# - In_Progress/
# - Approved/
# - Rejected/
# - Done/
# - Plans/
# - Logs/
```

**Expected:** All 9 folders present ✅

---

## ✅ Test 2: Agent Skills (1 minute)

```bash
# Check all 8 skills exist
ls -la .claude/skills/

# Should show:
# 1. process-inbox.json
# 2. update-dashboard.json
# 3. generate-briefing.json
# 4. create-plan.json
# 5. execute-plan.json
# 6. process-approval.json
# 7. generate-linkedin-post.json
# 8. watch-inbox.json
```

**Expected:** 8 skill files present ✅

---

## ✅ Test 3: MCP Server (2 minutes)

```bash
cd mcp_server

# Run test script
python3 test_server.py
```

**Expected output:**
```
🧪 Testing Email MCP Server...
Test 1: Initialize request
✅ Initialize: PASSED

Test 2: List tools request
✅ List tools: PASSED (found 1 tools)

Test 3: Send email request
✅ Send email: PASSED

🎉 All tests passed! MCP server is working correctly.
```

**If you see this:** MCP server works! ✅

---

## ✅ Test 4: File System Watcher (2 minutes)

```bash
cd "/Users/user/Documents/GitHub/Personal AI Employee"

# Test the watcher
python3 watcher/simple_watcher.py &
WATCHER_PID=$!

# Wait 2 seconds
sleep 2

# Create a test file
echo "Test task: Review quarterly report" > AI_Employee_Vault/Inbox/test-task.md

# Wait 5 seconds for watcher to detect
sleep 5

# Check if notification was created
ls -la AI_Employee_Vault/Needs_Action/

# Stop the watcher
kill $WATCHER_PID
```

**Expected:** You should see a notification file in Needs_Action/ ✅

---

## ✅ Test 5: Dashboard & Company Handbook (30 seconds)

```bash
# Check Dashboard exists and has content
cat AI_Employee_Vault/Dashboard.md | head -20

# Check Company Handbook exists
cat AI_Employee_Vault/Company_Handbook.md | head -20

# Check Business Goals exists
cat AI_Employee_Vault/Business_Goals.md | head -20
```

**Expected:** All three files exist with proper content ✅

---

## ✅ Test 6: Scripts (1 minute)

```bash
# Check all scripts exist and are executable
ls -la scripts/

# Should show:
# - daily-briefing.sh (executable)
# - weekly-audit.sh (executable)
# - process-approvals.sh (executable)
# - post-linkedin.sh (executable)

# Test daily briefing script (dry run)
./scripts/daily-briefing.sh
```

**Expected:** Script runs without errors ✅

---

## ✅ Test 7: Plan Generation (2 minutes)

```bash
# Start Claude Code
claude code
```

Then ask Claude:
```
"Create a plan for building a simple todo app with React"
```

**Expected:**
- Claude creates a Plan.md file in Plans/ folder
- Plan has step-by-step breakdown
- Plan has checkboxes for tracking
- Plan includes time estimates

**Check the plan:**
```bash
ls -la AI_Employee_Vault/Plans/
cat AI_Employee_Vault/Plans/PLAN-*.md
```

---

## ✅ Test 8: Briefing Generation (2 minutes)

```bash
claude code
```

Then ask Claude:
```
"Generate a daily briefing for the CEO"
```

**Expected:**
- Claude analyzes Dashboard, Business Goals, recent activity
- Creates briefing in Logs/ folder
- Briefing includes priorities, bottlenecks, recommendations

**Check the briefing:**
```bash
ls -la AI_Employee_Vault/Logs/
cat AI_Employee_Vault/Logs/BRIEFING-*.md
```

---

## ✅ Test 9: LinkedIn Post Generation (2 minutes)

```bash
claude code
```

Then ask Claude:
```
"Generate a LinkedIn post about completing our AI automation project"
```

**Expected:**
- Claude creates post in Pending_Approval/ folder
- Post has engaging content
- Post includes hashtags
- Post references Business Goals

**Check the post:**
```bash
ls -la AI_Employee_Vault/Pending_Approval/
cat AI_Employee_Vault/Pending_Approval/LINKEDIN-POST-*.md
```

---

## ✅ Test 10: Approval Workflow (2 minutes)

```bash
# Move the LinkedIn post to Approved
mv AI_Employee_Vault/Pending_Approval/LINKEDIN-POST-*.md AI_Employee_Vault/Approved/

# Run approval processing
./scripts/process-approvals.sh

# Check if post was processed
ls -la AI_Employee_Vault/Approved/
ls -la AI_Employee_Vault/Done/
```

**Expected:** Post moved to Done/ after processing ✅

---

## ✅ Test 11: Git Repository (1 minute)

```bash
# Check git status
git status

# Check recent commits
git log --oneline -5

# Verify remote
git remote -v
```

**Expected:**
- Repository is clean or has only untracked files
- Recent commits show Silver Tier work
- Remote points to your GitHub repo

---

## ✅ Test 12: Documentation (1 minute)

```bash
# Check all key documentation exists
ls -la *.md

# Should include:
# - README.md
# - BRONZE_TIER_COMPLETE.md
# - SILVER_TIER_COMPLETE.md
# - SILVER_TIER_READY.md
# - SILVER_TIER_100_PERCENT.md
# - SETUP_GUIDE.md
# - SCHEDULING.md
# - GMAIL_SETUP.md
```

**Expected:** All documentation files present ✅

---

## 🎯 Quick Test Summary

Run this one command to test multiple things at once:

```bash
cd "/Users/user/Documents/GitHub/Personal AI Employee"

echo "=== Testing File Structure ==="
ls AI_Employee_Vault/ | wc -l
# Should show: 9 (folders)

echo "=== Testing Agent Skills ==="
ls .claude/skills/ | wc -l
# Should show: 8 (skills)

echo "=== Testing MCP Server ==="
python3 mcp_server/test_server.py

echo "=== Testing Scripts ==="
ls scripts/*.sh | wc -l
# Should show: 4 (scripts)

echo "=== Testing Watchers ==="
ls watcher/*.py | wc -l
# Should show: 4 (watchers)

echo "=== Testing Documentation ==="
ls *.md | wc -l
# Should show: 25+ (docs)

echo "=== All Tests Complete ==="
```

---

## 🚨 Troubleshooting

### MCP Server Test Fails:
```bash
# Check Python version
python3 --version
# Needs 3.8+

# Try running server manually
cd mcp_server
python3 email_server.py
# Press Ctrl+C to stop
```

### Watcher Not Detecting Files:
```bash
# Check watcher is running
ps aux | grep watcher

# Check file permissions
ls -la watcher/simple_watcher.py
# Should be executable
```

### Claude Code Not Finding Skills:
```bash
# Check skills directory
ls -la .claude/skills/

# Verify JSON syntax
python3 -m json.tool .claude/skills/create-plan.json
```

### Scripts Not Executable:
```bash
# Make scripts executable
chmod +x scripts/*.sh
```

---

## ✅ Success Criteria

**Bronze Tier (100%):**
- [x] 9 folders in AI_Employee_Vault
- [x] Dashboard.md, Company_Handbook.md, Business_Goals.md exist
- [x] File system watcher works
- [x] 3 Agent Skills (process-inbox, update-dashboard, watch-inbox)
- [x] Items processed with Company Handbook compliance

**Silver Tier (100%):**
- [x] All Bronze requirements
- [x] 3 watchers (file, gmail, whatsapp)
- [x] LinkedIn auto-posting
- [x] Plan.md generation works
- [x] MCP server tests pass
- [x] Approval workflow works
- [x] Scheduling scripts exist
- [x] 8 total Agent Skills

---

## 🎉 If All Tests Pass:

**You're ready to:**
1. ✅ Submit to hackathon
2. ✅ Record demo video
3. ✅ Deploy to production (with setup)

**Silver Tier Status:** 100% Complete and Verified! 🚀

---

**Testing Time:** 15-20 minutes total
**Last Updated:** 2026-02-25
