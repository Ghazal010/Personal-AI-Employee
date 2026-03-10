#!/usr/bin/env python3
"""
Task Management Skills
Skills for managing tasks in the Obsidian vault
"""

import sys
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agent_skills.skill_framework import AgentSkill, SkillResult, register_skill


@register_skill
class GetTaskStatisticsSkill(AgentSkill):
    """Get task statistics from vault"""

    def __init__(self):
        super().__init__()
        self.vault_path = Path(__file__).parent.parent / "AI_Employee_Vault"

    def get_description(self) -> str:
        return "Get statistics about tasks across all workflow stages"

    def get_parameters(self) -> Dict[str, Dict[str, Any]]:
        return {}

    def execute(self, **kwargs) -> SkillResult:
        """Execute statistics gathering"""
        try:
            stats = {
                "needs_action": 0,
                "in_progress": 0,
                "done": 0,
                "pending_approval": 0,
                "total": 0
            }

            # Count files in each folder
            folders = {
                "needs_action": self.vault_path / "Needs_Action",
                "in_progress": self.vault_path / "In_Progress",
                "done": self.vault_path / "Done",
                "pending_approval": self.vault_path / "Pending_Approval"
            }

            for key, folder in folders.items():
                if folder.exists():
                    count = len(list(folder.glob("*.md")))
                    stats[key] = count
                    stats["total"] += count

            return SkillResult(
                success=True,
                data=stats
            )

        except Exception as e:
            return SkillResult(
                success=False,
                error=f"Error getting task statistics: {str(e)}"
            )


@register_skill
class ListTasksSkill(AgentSkill):
    """List tasks in a specific workflow stage"""

    def __init__(self):
        super().__init__()
        self.vault_path = Path(__file__).parent.parent / "AI_Employee_Vault"

    def get_description(self) -> str:
        return "List all tasks in a specific workflow stage"

    def get_parameters(self) -> Dict[str, Dict[str, Any]]:
        return {
            "stage": {
                "type": str,
                "required": True,
                "description": "Workflow stage: needs_action, in_progress, done, pending_approval"
            }
        }

    def execute(self, **kwargs) -> SkillResult:
        """Execute task listing"""
        try:
            stage = kwargs.get('stage')

            # Map stage to folder
            folder_map = {
                "needs_action": "Needs_Action",
                "in_progress": "In_Progress",
                "done": "Done",
                "pending_approval": "Pending_Approval"
            }

            if stage not in folder_map:
                return SkillResult(
                    success=False,
                    error=f"Invalid stage: {stage}. Must be one of: {', '.join(folder_map.keys())}"
                )

            folder = self.vault_path / folder_map[stage]

            if not folder.exists():
                return SkillResult(
                    success=True,
                    data={"stage": stage, "count": 0, "tasks": []}
                )

            # List task files
            task_files = list(folder.glob("*.md"))
            tasks = []

            for task_file in task_files:
                tasks.append({
                    "name": task_file.stem,
                    "file_name": task_file.name,
                    "modified": datetime.fromtimestamp(task_file.stat().st_mtime).isoformat()
                })

            return SkillResult(
                success=True,
                data={
                    "stage": stage,
                    "count": len(tasks),
                    "tasks": tasks
                }
            )

        except Exception as e:
            return SkillResult(
                success=False,
                error=f"Error listing tasks: {str(e)}"
            )


@register_skill
class MoveTaskSkill(AgentSkill):
    """Move a task from one workflow stage to another"""

    def __init__(self):
        super().__init__()
        self.vault_path = Path(__file__).parent.parent / "AI_Employee_Vault"

    def get_description(self) -> str:
        return "Move a task file from one workflow stage to another"

    def get_parameters(self) -> Dict[str, Dict[str, Any]]:
        return {
            "task_name": {
                "type": str,
                "required": True,
                "description": "Name of the task file (without .md extension)"
            },
            "from_stage": {
                "type": str,
                "required": True,
                "description": "Source stage: needs_action, in_progress, done, pending_approval"
            },
            "to_stage": {
                "type": str,
                "required": True,
                "description": "Destination stage: needs_action, in_progress, done, pending_approval"
            }
        }

    def execute(self, **kwargs) -> SkillResult:
        """Execute task move"""
        try:
            task_name = kwargs.get('task_name')
            from_stage = kwargs.get('from_stage')
            to_stage = kwargs.get('to_stage')

            # Map stages to folders
            folder_map = {
                "needs_action": "Needs_Action",
                "in_progress": "In_Progress",
                "done": "Done",
                "pending_approval": "Pending_Approval"
            }

            if from_stage not in folder_map or to_stage not in folder_map:
                return SkillResult(
                    success=False,
                    error=f"Invalid stage. Must be one of: {', '.join(folder_map.keys())}"
                )

            # Get source and destination paths
            from_folder = self.vault_path / folder_map[from_stage]
            to_folder = self.vault_path / folder_map[to_stage]

            source_file = from_folder / f"{task_name}.md"
            dest_file = to_folder / f"{task_name}.md"

            if not source_file.exists():
                return SkillResult(
                    success=False,
                    error=f"Task not found: {task_name} in {from_stage}"
                )

            # Ensure destination folder exists
            to_folder.mkdir(parents=True, exist_ok=True)

            # Move file
            source_file.rename(dest_file)

            return SkillResult(
                success=True,
                data={
                    "task_name": task_name,
                    "from_stage": from_stage,
                    "to_stage": to_stage,
                    "new_path": str(dest_file)
                }
            )

        except Exception as e:
            return SkillResult(
                success=False,
                error=f"Error moving task: {str(e)}"
            )


@register_skill
class CreateTaskSkill(AgentSkill):
    """Create a new task in the vault"""

    def __init__(self):
        super().__init__()
        self.vault_path = Path(__file__).parent.parent / "AI_Employee_Vault"

    def get_description(self) -> str:
        return "Create a new task file in the specified workflow stage"

    def get_parameters(self) -> Dict[str, Dict[str, Any]]:
        return {
            "title": {
                "type": str,
                "required": True,
                "description": "Task title"
            },
            "description": {
                "type": str,
                "required": True,
                "description": "Task description"
            },
            "stage": {
                "type": str,
                "required": False,
                "default": "needs_action",
                "description": "Initial workflow stage"
            },
            "priority": {
                "type": str,
                "required": False,
                "default": "normal",
                "description": "Priority: low, normal, high, critical"
            }
        }

    def execute(self, **kwargs) -> SkillResult:
        """Execute task creation"""
        try:
            title = kwargs.get('title')
            description = kwargs.get('description')
            stage = kwargs.get('stage', 'needs_action')
            priority = kwargs.get('priority', 'normal')

            # Map stage to folder
            folder_map = {
                "needs_action": "Needs_Action",
                "in_progress": "In_Progress",
                "done": "Done",
                "pending_approval": "Pending_Approval"
            }

            if stage not in folder_map:
                return SkillResult(
                    success=False,
                    error=f"Invalid stage: {stage}"
                )

            folder = self.vault_path / folder_map[stage]
            folder.mkdir(parents=True, exist_ok=True)

            # Create safe filename
            safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_'))[:50]
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            filename = f"TASK-{timestamp}-{safe_title}.md"
            filepath = folder / filename

            # Priority emoji
            priority_emoji = {
                "low": "🔵",
                "normal": "🟢",
                "high": "🟠",
                "critical": "🔴"
            }.get(priority, "🟢")

            # Create content
            content = f"""# {priority_emoji} {title}

**Created:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Priority:** {priority.title()}
**Status:** {stage.replace('_', ' ').title()}

## Description

{description}

## Action Items

- [ ] Review task requirements
- [ ] Plan implementation
- [ ] Execute task
- [ ] Verify completion

## Notes

*Add notes here as you work on this task*

---

**Created by:** Agent Skills System
"""

            # Write file
            filepath.write_text(content, encoding='utf-8')

            return SkillResult(
                success=True,
                data={
                    "title": title,
                    "file_name": filename,
                    "file_path": str(filepath),
                    "stage": stage,
                    "priority": priority
                }
            )

        except Exception as e:
            return SkillResult(
                success=False,
                error=f"Error creating task: {str(e)}"
            )
