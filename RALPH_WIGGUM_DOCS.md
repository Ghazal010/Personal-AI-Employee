# Ralph Wiggum Loop - Autonomous Agent Documentation

**Version:** 1.0.0
**Last Updated:** 2026-03-10
**Status:** Production Ready

---

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Features](#features)
4. [How It Works](#how-it-works)
5. [Usage](#usage)
6. [Configuration](#configuration)
7. [Autonomous Actions](#autonomous-actions)
8. [Monitoring](#monitoring)
9. [Best Practices](#best-practices)
10. [Troubleshooting](#troubleshooting)

---

## Overview

The Ralph Wiggum Loop is an autonomous agent that continuously monitors the Personal AI Employee system, analyzes pending tasks, and executes automated actions without human intervention.

### Why "Ralph Wiggum"?

Named after Ralph Wiggum from The Simpsons - simple, persistent, and always working. The agent embodies these qualities:
- **Simple** - Straightforward logic, easy to understand
- **Persistent** - Runs continuously without stopping
- **Always Working** - Constantly monitoring and executing tasks

### Key Features

- **Autonomous Operation** - Runs continuously without human intervention
- **Task Analysis** - Automatically analyzes pending tasks by type and priority
- **Automated Actions** - Executes routine tasks (report generation, health checks)
- **Self-Monitoring** - Checks system health and logs all activities
- **Graceful Degradation** - Continues operating even when errors occur
- **Comprehensive Logging** - All actions logged to audit system

---

## Architecture

### System Design

```
┌─────────────────────────────────────────────────────────┐
│           Ralph Wiggum Loop Architecture                 │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                    Main Loop                             │
│  ┌────────────────────────────────────────────────┐    │
│  │  while running:                                 │    │
│  │    1. Check system health                       │    │
│  │    2. Get pending tasks                         │    │
│  │    3. Analyze tasks                             │    │
│  │    4. Execute automated actions                 │    │
│  │    5. Log results                               │    │
│  │    6. Sleep (check_interval)                    │    │
│  └────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                  Agent Skills                            │
│  ┌──────────────────┐  ┌──────────────────┐           │
│  │ GetAuditStats    │  │ GenerateCEO      │           │
│  │ Skill            │  │ BriefingSkill    │           │
│  └──────────────────┘  └──────────────────┘           │
│  ┌──────────────────┐  ┌──────────────────┐           │
│  │ GenerateAudit    │  │ GetTaskStats     │           │
│  │ SummarySkill     │  │ Skill            │           │
│  └──────────────────┘  └──────────────────┘           │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                  Data Sources                            │
│  ┌──────────────────┐  ┌──────────────────┐           │
│  │ Needs_Action/    │  │ Audit Logs       │           │
│  │ (Pending Tasks)  │  │ (System Events)  │           │
│  └──────────────────┘  └──────────────────┘           │
└─────────────────────────────────────────────────────────┘
```

### Component Interaction

```
Ralph Wiggum Loop
    ├─> Agent Skills Framework
    │   ├─> GetAuditStatisticsSkill
    │   ├─> GenerateCEOBriefingSkill
    │   ├─> GenerateAuditSummarySkill
    │   └─> GetTaskStatisticsSkill
    │
    ├─> Audit Logger
    │   └─> logs/audit.jsonl
    │
    └─> Obsidian Vault
        ├─> Needs_Action/ (read)
        ├─> CEO_Briefing.md (write)
        └─> Audit_Logs.md (write)
```

---

## Features

### 1. Continuous Monitoring

- Runs in an infinite loop with configurable check interval
- Default: 5 minutes between cycles
- Gracefully handles interruptions (Ctrl+C)

### 2. Task Analysis

**Automatic Task Type Detection:**
- `EMAIL-*` → Email tasks
- `WHATSAPP-*` → WhatsApp tasks
- `TASK-*` → General tasks
- `CRITICAL-*` → Critical/urgent tasks

**Priority Detection:**
- 🔴 Critical - Requires immediate attention
- 🟠 High - Important, address soon
- 🟡 Normal - Standard priority
- 🔵 Low - Can wait

### 3. Automated Actions

**Every Cycle:**
- System health check
- CEO briefing generation
- Audit summary generation

**Future Actions (Planned):**
- Auto-respond to routine emails
- Auto-categorize tasks
- Auto-escalate critical issues
- Auto-archive completed tasks

### 4. Self-Monitoring

- Tracks cycle count
- Measures cycle duration
- Logs all activities to audit system
- Reports errors without crashing

### 5. Comprehensive Logging

**Console Output:**
- Timestamped log messages
- Color-coded by severity
- Real-time progress updates

**Audit Logs:**
- All cycles logged to audit.jsonl
- Includes cycle results and errors
- Queryable via Agent Skills

---

## How It Works

### Cycle Execution Flow

```
1. START CYCLE
   ↓
2. CHECK SYSTEM HEALTH
   - Execute GetAuditStatisticsSkill
   - Calculate success rate
   - Log health status
   ↓
3. GET PENDING TASKS
   - Scan Needs_Action/ folder
   - List all .md files
   - Sort by modified time (oldest first)
   ↓
4. ANALYZE TASKS
   - Determine task type from filename
   - Read content to detect priority
   - Generate recommended actions
   - Analyze top 5 tasks
   ↓
5. EXECUTE AUTOMATED ACTIONS
   - Generate CEO briefing
   - Generate audit summary
   - (Future: more automated actions)
   ↓
6. LOG RESULTS
   - Log to console
   - Log to audit.jsonl
   - Track cycle metrics
   ↓
7. SLEEP
   - Wait check_interval seconds
   - Go to step 1
```

### Task Analysis Logic

```python
# Determine task type
if filename.startswith("EMAIL-"):
    task_type = "email"
elif filename.startswith("WHATSAPP-"):
    task_type = "whatsapp"
elif filename.startswith("TASK-"):
    task_type = "task"
elif filename.startswith("CRITICAL-"):
    task_type = "critical"

# Determine priority from content
if "🔴" in content or "CRITICAL" in content:
    priority = "critical"
elif "🟠" in content or "IMPORTANT" in content:
    priority = "high"
elif "🟡" in content or "URGENT" in content:
    priority = "high"
else:
    priority = "normal"
```

---

## Usage

### Starting the Agent

**Foreground (for testing):**
```bash
python3 ralph_wiggum_loop.py
```

**With custom interval:**
```bash
python3 ralph_wiggum_loop.py --interval 600  # 10 minutes
```

**Background (production):**
```bash
nohup python3 ralph_wiggum_loop.py > logs/ralph-wiggum.log 2>&1 &
```

**With systemd (Linux):**
```bash
sudo systemctl start ralph-wiggum
sudo systemctl enable ralph-wiggum  # Start on boot
```

### Stopping the Agent

**Foreground:**
```
Press Ctrl+C
```

**Background:**
```bash
pkill -f ralph_wiggum_loop
```

**With systemd:**
```bash
sudo systemctl stop ralph-wiggum
```

### Checking Status

**Is it running?**
```bash
ps aux | grep ralph_wiggum_loop | grep -v grep
```

**View logs:**
```bash
tail -f logs/ralph-wiggum.log
```

**View audit logs:**
```bash
python3 skills_cli.py --skill QueryAuditLogsSkill --params '{"component": "ralph_wiggum_loop", "limit": 20}'
```

---

## Configuration

### Environment Variables

```bash
# Check interval (seconds)
export RALPH_CHECK_INTERVAL=300

# Vault path (optional)
export RALPH_VAULT_PATH="/path/to/AI_Employee_Vault"
```

### Command-Line Arguments

```bash
python3 ralph_wiggum_loop.py --help

Options:
  --interval SECONDS    Check interval in seconds (default: 300)
```

### Code Configuration

Edit `ralph_wiggum_loop.py`:

```python
# Default check interval
DEFAULT_CHECK_INTERVAL = 300  # 5 minutes

# Number of tasks to analyze per cycle
MAX_TASKS_TO_ANALYZE = 5

# Enable/disable specific automated actions
ENABLE_CEO_BRIEFING = True
ENABLE_AUDIT_SUMMARY = True
```

---

## Autonomous Actions

### Current Actions

#### 1. System Health Check

**Frequency:** Every cycle
**Skill:** GetAuditStatisticsSkill
**Purpose:** Monitor system health and success rate

**Output:**
```
System health: 82.4% success rate, 74 events
```

#### 2. CEO Briefing Generation

**Frequency:** Every cycle
**Skill:** GenerateCEOBriefingSkill
**Purpose:** Keep executive summary up-to-date

**Output:**
```
✅ CEO briefing generated
```

#### 3. Audit Summary Generation

**Frequency:** Every cycle
**Skill:** GenerateAuditSummarySkill
**Purpose:** Keep audit log dashboard current

**Output:**
```
✅ Audit summary generated
```

### Planned Actions

#### 4. Auto-Categorization (Future)

- Analyze task content
- Assign categories and tags
- Move to appropriate folders

#### 5. Auto-Response (Future)

- Detect routine emails
- Generate appropriate responses
- Send via email skill

#### 6. Auto-Escalation (Future)

- Detect critical issues
- Create high-priority tasks
- Send notifications

#### 7. Auto-Archival (Future)

- Detect completed tasks
- Move to Done/ folder
- Update statistics

---

## Monitoring

### Key Metrics

**Cycle Metrics:**
- Cycle count
- Cycle duration
- Tasks found per cycle
- Tasks analyzed per cycle
- Actions taken per cycle
- Errors per cycle

**System Metrics:**
- System health (success rate)
- Total events logged
- Pending task count
- Completed task count

### Viewing Metrics

**Console Output:**
```
[2026-03-10 20:25:21] [INFO] 🔄 Starting autonomous cycle #1
[2026-03-10 20:25:21] [INFO] 🏥 Checking system health...
[2026-03-10 20:25:21] [INFO]    System health: 82.4% success rate, 74 events
[2026-03-10 20:25:21] [INFO] 📋 Checking for pending tasks...
[2026-03-10 20:25:21] [INFO]    Found 5 pending task(s)
[2026-03-10 20:25:21] [INFO] ✅ Cycle #1 completed in 0.0s
```

**Audit Logs:**
```bash
python3 skills_cli.py --skill QueryAuditLogsSkill --params '{
  "component": "ralph_wiggum_loop",
  "event_type": "system_health_check",
  "limit": 10
}'
```

**Dashboard:**
- Open Obsidian vault
- View [[CEO Briefing]] for weekly summary
- View [[Audit Logs]] for system events

---

## Best Practices

### 1. Set Appropriate Check Interval

**Too Frequent (< 1 minute):**
- Wastes CPU resources
- Generates excessive logs
- No benefit for most use cases

**Recommended (5-10 minutes):**
- Good balance
- Timely task processing
- Reasonable resource usage

**Too Infrequent (> 30 minutes):**
- Delayed task processing
- May miss time-sensitive items

### 2. Monitor System Health

Check regularly:
```bash
# View recent cycles
tail -50 logs/ralph-wiggum.log

# Check for errors
grep ERROR logs/ralph-wiggum.log

# View audit logs
python3 skills_cli.py --skill GetAuditStatisticsSkill
```

### 3. Handle Errors Gracefully

The agent is designed to continue running despite errors:
- Individual action failures don't stop the cycle
- Errors are logged but don't crash the agent
- Next cycle will retry failed actions

### 4. Run in Background

For production use:
```bash
# Start in background
nohup python3 ralph_wiggum_loop.py > logs/ralph-wiggum.log 2>&1 &

# Save PID for later
echo $! > logs/ralph-wiggum.pid

# Stop later
kill $(cat logs/ralph-wiggum.pid)
```

### 5. Rotate Logs

Prevent log files from growing too large:
```bash
# Manual rotation
mv logs/ralph-wiggum.log logs/ralph-wiggum.log.old
gzip logs/ralph-wiggum.log.old

# Or use logrotate (Linux)
# Add to /etc/logrotate.d/ralph-wiggum
```

---

## Troubleshooting

### Issue: Agent not starting

**Symptoms:** Script exits immediately

**Solutions:**
1. Check Python version: `python3 --version` (need 3.13+)
2. Check dependencies: `pip3 list | grep google`
3. Check vault path exists: `ls AI_Employee_Vault/`
4. Check permissions: `ls -la ralph_wiggum_loop.py`

### Issue: No tasks found

**Symptoms:** "No pending tasks found" every cycle

**Solutions:**
1. Check Needs_Action folder: `ls AI_Employee_Vault/Needs_Action/`
2. Verify task files are .md format
3. Check file permissions

### Issue: Actions failing

**Symptoms:** "❌ Failed: ..." in logs

**Solutions:**
1. Check audit logs: `tail logs/audit.jsonl`
2. Verify Agent Skills working: `python3 skills_cli.py --list`
3. Test individual skills: `python3 skills_cli.py --skill GenerateCEOBriefingSkill`

### Issue: High CPU usage

**Symptoms:** Python process using excessive CPU

**Solutions:**
1. Increase check interval: `--interval 600`
2. Check for infinite loops in custom actions
3. Monitor with: `top -p $(pgrep -f ralph_wiggum)`

### Issue: Agent stops unexpectedly

**Symptoms:** Process no longer running

**Solutions:**
1. Check logs for errors: `tail -100 logs/ralph-wiggum.log`
2. Check system logs: `dmesg | grep python`
3. Run in foreground to see errors: `python3 ralph_wiggum_loop.py`

---

## Testing

### Single Cycle Test

```bash
python3 test_ralph_wiggum.py
```

**Expected Output:**
```
Testing Ralph Wiggum Loop - Single Cycle

[2026-03-10 20:25:21] [INFO] 🔄 Starting autonomous cycle #1
...
✅ Test completed successfully!
```

### Integration Test

```bash
# Run for 1 minute then stop
python3 ralph_wiggum_loop.py --interval 10 &
RALPH_PID=$!
sleep 60
kill $RALPH_PID
```

### Load Test

```bash
# Run with very short interval
python3 ralph_wiggum_loop.py --interval 1
# Monitor CPU and memory usage
# Press Ctrl+C after a few minutes
```

---

## Future Enhancements

### Phase 1: Enhanced Task Processing

- [ ] Auto-categorize tasks by content analysis
- [ ] Auto-assign priorities based on keywords
- [ ] Auto-move tasks between workflow stages
- [ ] Auto-create subtasks for complex tasks

### Phase 2: Intelligent Actions

- [ ] Auto-respond to routine emails
- [ ] Auto-schedule meetings based on calendar
- [ ] Auto-generate invoices from templates
- [ ] Auto-approve low-value expenses

### Phase 3: Learning & Adaptation

- [ ] Learn from user actions
- [ ] Adapt priorities based on patterns
- [ ] Suggest workflow improvements
- [ ] Predict task completion times

### Phase 4: Multi-Agent Coordination

- [ ] Multiple specialized agents
- [ ] Agent-to-agent communication
- [ ] Distributed task processing
- [ ] Load balancing across agents

---

## Summary

The Ralph Wiggum Loop provides:

- ✅ **Autonomous Operation** - Runs continuously without intervention
- ✅ **Task Analysis** - Automatically categorizes and prioritizes tasks
- ✅ **Automated Actions** - Executes routine tasks automatically
- ✅ **Self-Monitoring** - Tracks health and logs all activities
- ✅ **Graceful Degradation** - Continues operating despite errors
- ✅ **Comprehensive Logging** - All actions auditable
- ✅ **Easy Configuration** - Simple command-line interface
- ✅ **Production Ready** - Tested and documented

**Status:** Production Ready
**Version:** 1.0.0
**Last Updated:** 2026-03-10

---

**"I'm helping!" - Ralph Wiggum**
