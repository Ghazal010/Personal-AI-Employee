#!/usr/bin/env python3
"""
Audit & Reporting Skills
Skills for audit logs and report generation
"""

import sys
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime, timedelta

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agent_skills.skill_framework import AgentSkill, SkillResult, register_skill
from audit_logger import AuditLogReader


@register_skill
class GetAuditStatisticsSkill(AgentSkill):
    """Get audit log statistics"""

    def __init__(self):
        super().__init__()
        self.reader = AuditLogReader()

    def get_description(self) -> str:
        return "Get statistics from audit logs for a specified time period"

    def get_parameters(self) -> Dict[str, Dict[str, Any]]:
        return {
            "days": {
                "type": int,
                "required": False,
                "default": 7,
                "description": "Number of days to analyze"
            }
        }

    def execute(self, **kwargs) -> SkillResult:
        """Execute statistics gathering"""
        try:
            days = kwargs.get('days', 7)
            stats = self.reader.get_statistics(days=days)

            return SkillResult(
                success=True,
                data=stats,
                metadata={"days": days}
            )

        except Exception as e:
            return SkillResult(
                success=False,
                error=f"Error getting audit statistics: {str(e)}"
            )


@register_skill
class GenerateCEOBriefingSkill(AgentSkill):
    """Generate weekly CEO briefing"""

    def __init__(self):
        super().__init__()

    def get_description(self) -> str:
        return "Generate comprehensive weekly CEO briefing with metrics and recommendations"

    def get_parameters(self) -> Dict[str, Dict[str, Any]]:
        return {
            "days": {
                "type": int,
                "required": False,
                "default": 7,
                "description": "Number of days to include in report"
            }
        }

    def execute(self, **kwargs) -> SkillResult:
        """Execute briefing generation"""
        try:
            days = kwargs.get('days', 7)

            # Import and run generator
            from generate_ceo_briefing import generate_briefing
            content = generate_briefing(days=days)

            # Write to vault
            vault_path = Path(__file__).parent.parent / "AI_Employee_Vault"
            briefing_path = vault_path / "CEO_Briefing.md"
            briefing_path.write_text(content, encoding='utf-8')

            return SkillResult(
                success=True,
                data={
                    "file_path": str(briefing_path),
                    "days": days,
                    "generated_at": datetime.now().isoformat()
                }
            )

        except Exception as e:
            return SkillResult(
                success=False,
                error=f"Error generating CEO briefing: {str(e)}"
            )


@register_skill
class GenerateAuditSummarySkill(AgentSkill):
    """Generate audit log summary"""

    def __init__(self):
        super().__init__()

    def get_description(self) -> str:
        return "Generate audit log summary for Obsidian dashboard"

    def get_parameters(self) -> Dict[str, Dict[str, Any]]:
        return {}

    def execute(self, **kwargs) -> SkillResult:
        """Execute summary generation"""
        try:
            # Import and run generator
            from generate_audit_summary import generate_audit_summary
            content = generate_audit_summary()

            # Write to vault
            vault_path = Path(__file__).parent.parent / "AI_Employee_Vault"
            summary_path = vault_path / "Audit_Logs.md"
            summary_path.write_text(content, encoding='utf-8')

            return SkillResult(
                success=True,
                data={
                    "file_path": str(summary_path),
                    "generated_at": datetime.now().isoformat()
                }
            )

        except Exception as e:
            return SkillResult(
                success=False,
                error=f"Error generating audit summary: {str(e)}"
            )


@register_skill
class QueryAuditLogsSkill(AgentSkill):
    """Query audit logs with filters"""

    def __init__(self):
        super().__init__()
        self.reader = AuditLogReader()

    def get_description(self) -> str:
        return "Query audit logs with optional filters (event type, component, date range)"

    def get_parameters(self) -> Dict[str, Dict[str, Any]]:
        return {
            "limit": {
                "type": int,
                "required": False,
                "default": 20,
                "description": "Maximum number of logs to return"
            },
            "event_type": {
                "type": str,
                "required": False,
                "description": "Filter by event type"
            },
            "component": {
                "type": str,
                "required": False,
                "description": "Filter by component name"
            },
            "days": {
                "type": int,
                "required": False,
                "description": "Only return logs from last N days"
            }
        }

    def execute(self, **kwargs) -> SkillResult:
        """Execute log query"""
        try:
            limit = kwargs.get('limit', 20)
            event_type = kwargs.get('event_type')
            component = kwargs.get('component')
            days = kwargs.get('days')

            # Calculate date range if days specified
            start_date = None
            if days:
                start_date = datetime.now() - timedelta(days=days)

            # Query logs
            logs = self.reader.read_logs(
                limit=limit,
                event_type=event_type,
                component=component,
                start_date=start_date
            )

            return SkillResult(
                success=True,
                data={
                    "count": len(logs),
                    "logs": logs
                },
                metadata={
                    "limit": limit,
                    "event_type": event_type,
                    "component": component,
                    "days": days
                }
            )

        except Exception as e:
            return SkillResult(
                success=False,
                error=f"Error querying audit logs: {str(e)}"
            )
