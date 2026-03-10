# Agent Skills System - Documentation

**Version:** 1.0.0
**Last Updated:** 2026-03-10
**Status:** Production Ready

---

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Available Skills](#available-skills)
4. [Usage](#usage)
5. [Creating Custom Skills](#creating-custom-skills)
6. [CLI Reference](#cli-reference)
7. [Integration Guide](#integration-guide)
8. [Best Practices](#best-practices)

---

## Overview

The Agent Skills System is a modular framework that converts existing functionality into reusable, composable capabilities that can be executed by AI agents, scripts, or other automation tools.

### Key Features

- **Modular Design** - Each skill is self-contained and independent
- **Standard Interface** - All skills follow the same execution pattern
- **Type Safety** - Parameter validation with type checking
- **Result Format** - Consistent SkillResult format for all outputs
- **Registry System** - Automatic skill registration and discovery
- **CLI Tool** - Command-line interface for manual execution
- **Audit Logging** - All skill executions are logged

### Design Principles

1. **Single Responsibility** - Each skill does one thing well
2. **Composability** - Skills can be chained together
3. **Idempotency** - Skills can be safely re-executed
4. **Error Handling** - Graceful failure with clear error messages
5. **Observability** - All actions are logged and auditable

---

## Architecture

### Core Components

```
agent_skills/
├── skill_framework.py      # Base classes and registry
├── email_skills.py          # Email-related skills
├── whatsapp_skills.py       # WhatsApp-related skills
├── audit_skills.py          # Audit and reporting skills
├── task_skills.py           # Task management skills
└── __init__.py              # Package initialization

skills_cli.py                # Command-line interface
```

### Class Hierarchy

```
AgentSkill (ABC)
├── ReadEmailsSkill
├── ProcessEmailSkill
├── GetEmailStatisticsSkill
├── ProcessWhatsAppChatSkill
├── GetWhatsAppStatisticsSkill
├── ListPendingWhatsAppChatsSkill
├── GetAuditStatisticsSkill
├── GenerateCEOBriefingSkill
├── GenerateAuditSummarySkill
├── QueryAuditLogsSkill
├── GetTaskStatisticsSkill
├── ListTasksSkill
├── MoveTaskSkill
└── CreateTaskSkill
```

### Skill Execution Flow

```
1. User/Agent calls execute_skill(name, **params)
   ↓
2. SkillRegistry looks up skill by name
   ↓
3. Validate parameters against schema
   ↓
4. Execute skill.execute(**params)
   ↓
5. Return SkillResult (success/failure + data)
   ↓
6. Log execution to audit log
```

---

## Available Skills

### Email Skills (3)

#### 1. ReadEmailsSkill

**Description:** Read unread important emails from Gmail inbox

**Parameters:**
- `max_results` (int, optional, default=10) - Maximum number of emails to fetch
- `mark_as_read` (bool, optional, default=False) - Mark emails as read after fetching

**Returns:**
```json
{
  "count": 5,
  "emails": [
    {"id": "19c85882"},
    {"id": "19c5c04d"}
  ]
}
```

**Example:**
```bash
python3 skills_cli.py --skill ReadEmailsSkill --params '{"max_results": 5}'
```

---

#### 2. ProcessEmailSkill

**Description:** Process a specific email and create action file in Obsidian vault

**Parameters:**
- `email_id` (str, required) - Gmail message ID to process

**Returns:**
```json
{
  "email_id": "19c85882",
  "file_path": "/path/to/EMAIL-19c85882-Subject.md",
  "subject": "Email Subject",
  "from": "sender@example.com"
}
```

**Example:**
```bash
python3 skills_cli.py --skill ProcessEmailSkill --params '{"email_id": "19c85882"}'
```

---

#### 3. GetEmailStatisticsSkill

**Description:** Get statistics about emails in the vault

**Parameters:** None

**Returns:**
```json
{
  "total_emails": 10,
  "email_files": ["EMAIL-19c85882-Subject.md", ...]
}
```

**Example:**
```bash
python3 skills_cli.py --skill GetEmailStatisticsSkill
```

---

### WhatsApp Skills (3)

#### 4. ProcessWhatsAppChatSkill

**Description:** Process a WhatsApp chat export file and create action file

**Parameters:**
- `file_path` (str, required) - Path to WhatsApp chat export .txt file

**Returns:**
```json
{
  "file_name": "chat.txt",
  "chat_name": "Contact Name",
  "total_messages": 50
}
```

**Example:**
```bash
python3 skills_cli.py --skill ProcessWhatsAppChatSkill --params '{"file_path": "whatsapp_integration/whatsapp_inbox/chat.txt"}'
```

---

#### 5. GetWhatsAppStatisticsSkill

**Description:** Get statistics about WhatsApp chats in the vault

**Parameters:** None

**Returns:**
```json
{
  "total_chats": 1,
  "chat_files": ["WHATSAPP-20260310-Contact.md"]
}
```

**Example:**
```bash
python3 skills_cli.py --skill GetWhatsAppStatisticsSkill
```

---

#### 6. ListPendingWhatsAppChatsSkill

**Description:** List pending WhatsApp chat exports waiting to be processed

**Parameters:** None

**Returns:**
```json
{
  "pending_chats": 2,
  "files": ["chat1.txt", "chat2.txt"]
}
```

**Example:**
```bash
python3 skills_cli.py --skill ListPendingWhatsAppChatsSkill
```

---

### Audit & Reporting Skills (4)

#### 7. GetAuditStatisticsSkill

**Description:** Get statistics from audit logs for a specified time period

**Parameters:**
- `days` (int, optional, default=7) - Number of days to analyze

**Returns:**
```json
{
  "total_events": 35,
  "success_count": 35,
  "failure_count": 0,
  "warning_count": 0,
  "events_by_type": {...},
  "events_by_component": {...}
}
```

**Example:**
```bash
python3 skills_cli.py --skill GetAuditStatisticsSkill --params '{"days": 30}'
```

---

#### 8. GenerateCEOBriefingSkill

**Description:** Generate comprehensive weekly CEO briefing with metrics and recommendations

**Parameters:**
- `days` (int, optional, default=7) - Number of days to include in report

**Returns:**
```json
{
  "file_path": "/path/to/CEO_Briefing.md",
  "days": 7,
  "generated_at": "2026-03-10T20:00:00"
}
```

**Example:**
```bash
python3 skills_cli.py --skill GenerateCEOBriefingSkill
```

---

#### 9. GenerateAuditSummarySkill

**Description:** Generate audit log summary for Obsidian dashboard

**Parameters:** None

**Returns:**
```json
{
  "file_path": "/path/to/Audit_Logs.md",
  "generated_at": "2026-03-10T20:00:00"
}
```

**Example:**
```bash
python3 skills_cli.py --skill GenerateAuditSummarySkill
```

---

#### 10. QueryAuditLogsSkill

**Description:** Query audit logs with optional filters

**Parameters:**
- `limit` (int, optional, default=20) - Maximum number of logs to return
- `event_type` (str, optional) - Filter by event type
- `component` (str, optional) - Filter by component name
- `days` (int, optional) - Only return logs from last N days

**Returns:**
```json
{
  "count": 10,
  "logs": [
    {
      "timestamp": "2026-03-10T19:57:25",
      "component": "gmail_watcher",
      "event_type": "email_received",
      "action": "New important email detected",
      "status": "success"
    }
  ]
}
```

**Example:**
```bash
python3 skills_cli.py --skill QueryAuditLogsSkill --params '{"event_type": "email_received", "limit": 10}'
```

---

### Task Management Skills (5)

#### 11. GetTaskStatisticsSkill

**Description:** Get statistics about tasks across all workflow stages

**Parameters:** None

**Returns:**
```json
{
  "needs_action": 5,
  "in_progress": 0,
  "done": 8,
  "pending_approval": 3,
  "total": 16
}
```

**Example:**
```bash
python3 skills_cli.py --skill GetTaskStatisticsSkill
```

---

#### 12. ListTasksSkill

**Description:** List all tasks in a specific workflow stage

**Parameters:**
- `stage` (str, required) - Workflow stage: needs_action, in_progress, done, pending_approval

**Returns:**
```json
{
  "stage": "needs_action",
  "count": 5,
  "tasks": [
    {
      "name": "TASK-20260310-Review",
      "file_name": "TASK-20260310-Review.md",
      "modified": "2026-03-10T15:30:00"
    }
  ]
}
```

**Example:**
```bash
python3 skills_cli.py --skill ListTasksSkill --params '{"stage": "needs_action"}'
```

---

#### 13. MoveTaskSkill

**Description:** Move a task file from one workflow stage to another

**Parameters:**
- `task_name` (str, required) - Name of the task file (without .md extension)
- `from_stage` (str, required) - Source stage
- `to_stage` (str, required) - Destination stage

**Returns:**
```json
{
  "task_name": "TASK-20260310-Review",
  "from_stage": "needs_action",
  "to_stage": "in_progress",
  "new_path": "/path/to/In_Progress/TASK-20260310-Review.md"
}
```

**Example:**
```bash
python3 skills_cli.py --skill MoveTaskSkill --params '{"task_name": "TASK-20260310-Review", "from_stage": "needs_action", "to_stage": "in_progress"}'
```

---

#### 14. CreateTaskSkill

**Description:** Create a new task file in the specified workflow stage

**Parameters:**
- `title` (str, required) - Task title
- `description` (str, required) - Task description
- `stage` (str, optional, default="needs_action") - Initial workflow stage
- `priority` (str, optional, default="normal") - Priority: low, normal, high, critical

**Returns:**
```json
{
  "title": "Review code",
  "file_name": "TASK-20260310-Review code.md",
  "file_path": "/path/to/Needs_Action/TASK-20260310-Review code.md",
  "stage": "needs_action",
  "priority": "high"
}
```

**Example:**
```bash
python3 skills_cli.py --skill CreateTaskSkill --params '{"title": "Review code", "description": "Review PR #123", "priority": "high"}'
```

---

## Usage

### Python API

```python
from agent_skills import execute_skill, list_skills

# List all available skills
skills = list_skills()
for skill in skills:
    print(f"{skill['name']}: {skill['description']}")

# Execute a skill
result = execute_skill("GetEmailStatisticsSkill")

if result.success:
    print(f"Total emails: {result.data['total_emails']}")
else:
    print(f"Error: {result.error}")

# Execute with parameters
result = execute_skill(
    "CreateTaskSkill",
    title="Review documentation",
    description="Review and update all docs",
    priority="high"
)
```

### Command-Line Interface

```bash
# List all skills
python3 skills_cli.py --list

# Execute a skill without parameters
python3 skills_cli.py --skill GetEmailStatisticsSkill

# Execute a skill with parameters
python3 skills_cli.py --skill CreateTaskSkill --params '{
  "title": "Review code",
  "description": "Review PR #123",
  "priority": "high"
}'
```

---

## Creating Custom Skills

### Step 1: Create Skill Class

```python
from agent_skills.skill_framework import AgentSkill, SkillResult, register_skill
from typing import Dict, Any

@register_skill
class MyCustomSkill(AgentSkill):
    """My custom skill description"""

    def get_description(self) -> str:
        return "Description of what this skill does"

    def get_parameters(self) -> Dict[str, Dict[str, Any]]:
        return {
            "param1": {
                "type": str,
                "required": True,
                "description": "Description of param1"
            },
            "param2": {
                "type": int,
                "required": False,
                "default": 10,
                "description": "Description of param2"
            }
        }

    def execute(self, **kwargs) -> SkillResult:
        """Execute the skill"""
        try:
            param1 = kwargs.get('param1')
            param2 = kwargs.get('param2', 10)

            # Your skill logic here
            result_data = {"output": "success"}

            return SkillResult(
                success=True,
                data=result_data
            )

        except Exception as e:
            return SkillResult(
                success=False,
                error=str(e)
            )
```

### Step 2: Import in __init__.py

```python
# In agent_skills/__init__.py
import agent_skills.my_custom_skills
```

### Step 3: Test Your Skill

```bash
python3 skills_cli.py --list
python3 skills_cli.py --skill MyCustomSkill --params '{"param1": "value"}'
```

---

## CLI Reference

### Commands

```bash
# List all available skills
python3 skills_cli.py --list

# Execute a skill
python3 skills_cli.py --skill <SkillName>

# Execute with parameters
python3 skills_cli.py --skill <SkillName> --params '<JSON>'
```

### Output Format

```
🚀 Executing skill: SkillName
📋 Parameters: {...}

============================================================
RESULT
============================================================
✅ Status: SUCCESS

📊 Data:
{...}

📝 Metadata:
{...}

⏰ Timestamp: 2026-03-10T20:00:00
```

---

## Integration Guide

### With MCP Servers (Future)

```python
# MCP tool definition
{
    "name": "execute_agent_skill",
    "description": "Execute an agent skill",
    "input_schema": {
        "type": "object",
        "properties": {
            "skill_name": {"type": "string"},
            "parameters": {"type": "object"}
        }
    }
}

# MCP tool handler
def handle_execute_skill(skill_name, parameters):
    result = execute_skill(skill_name, **parameters)
    return result.to_dict()
```

### With Automation Scripts

```python
#!/usr/bin/env python3
"""Daily automation script"""

from agent_skills import execute_skill

# Generate daily reports
execute_skill("GenerateCEOBriefingSkill", days=1)
execute_skill("GenerateAuditSummarySkill")

# Check for pending items
emails = execute_skill("GetEmailStatisticsSkill")
tasks = execute_skill("GetTaskStatisticsSkill")

print(f"Emails: {emails.data['total_emails']}")
print(f"Tasks: {tasks.data['total']}")
```

### With Cron Jobs

```bash
# Daily CEO briefing at 9 AM
0 9 * * * cd /path/to/project && python3 skills_cli.py --skill GenerateCEOBriefingSkill

# Hourly audit summary
0 * * * * cd /path/to/project && python3 skills_cli.py --skill GenerateAuditSummarySkill
```

---

## Best Practices

### 1. Error Handling

Always wrap skill logic in try-except:

```python
def execute(self, **kwargs) -> SkillResult:
    try:
        # Skill logic
        return SkillResult(success=True, data=result)
    except Exception as e:
        return SkillResult(success=False, error=str(e))
```

### 2. Parameter Validation

Use the built-in validation:

```python
def get_parameters(self) -> Dict[str, Dict[str, Any]]:
    return {
        "email": {
            "type": str,
            "required": True,
            "description": "Email address"
        }
    }
```

### 3. Audit Logging

Log important actions:

```python
from audit_logger import AuditLogger, EventType

class MySkill(AgentSkill):
    def __init__(self):
        super().__init__()
        self.audit_logger = AuditLogger("my_skill")

    def execute(self, **kwargs):
        # ... do work ...
        self.audit_logger.log_event(
            EventType.SYSTEM_START,
            "MySkill executed successfully"
        )
```

### 4. Idempotency

Make skills safe to re-execute:

```python
def execute(self, **kwargs):
    # Check if already done
    if self.already_processed(item_id):
        return SkillResult(success=True, data={"status": "already_processed"})

    # Do work
    self.process(item_id)
```

### 5. Clear Documentation

Provide clear descriptions and examples:

```python
def get_description(self) -> str:
    return """
    Process email and create action file.

    This skill fetches an email by ID, extracts key information,
    and creates a markdown action file in the Obsidian vault.
    """
```

---

## Troubleshooting

### Skill Not Found

**Error:** `Skill not found: SkillName`

**Solution:** Ensure the skill is imported in `__init__.py`

### Parameter Validation Failed

**Error:** `Missing required parameter: param_name`

**Solution:** Check parameter definitions and provide all required parameters

### Import Errors

**Error:** `ModuleNotFoundError: No module named 'agent_skills'`

**Solution:** Run from project root or add to PYTHONPATH:
```bash
export PYTHONPATH=/path/to/project:$PYTHONPATH
```

---

## Summary

The Agent Skills System provides:

- ✅ **15 Production-Ready Skills** across 4 categories
- ✅ **Modular Architecture** for easy extension
- ✅ **CLI Tool** for manual execution
- ✅ **Python API** for programmatic access
- ✅ **Audit Logging** for all executions
- ✅ **Type Safety** with parameter validation
- ✅ **Comprehensive Documentation** with examples

**Status:** Production Ready
**Version:** 1.0.0
**Last Updated:** 2026-03-10
