#!/usr/bin/env python3
"""
Email Skills
Skills for email operations (Gmail)
"""

import sys
from pathlib import Path
from typing import Dict, Any, List

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agent_skills.skill_framework import AgentSkill, SkillResult, register_skill
from audit_logger import AuditLogger, EventType


@register_skill
class ReadEmailsSkill(AgentSkill):
    """Read unread important emails from Gmail"""

    def __init__(self):
        super().__init__()
        self.audit_logger = AuditLogger("email_skill")

    def get_description(self) -> str:
        return "Read unread important emails from Gmail inbox"

    def get_parameters(self) -> Dict[str, Dict[str, Any]]:
        return {
            "max_results": {
                "type": int,
                "required": False,
                "default": 10,
                "description": "Maximum number of emails to fetch"
            },
            "mark_as_read": {
                "type": bool,
                "required": False,
                "default": False,
                "description": "Mark emails as read after fetching"
            }
        }

    def execute(self, **kwargs) -> SkillResult:
        """Execute email reading"""
        try:
            max_results = kwargs.get('max_results', 10)

            # Import Gmail watcher functions
            from watcher.gmail_watcher_enhanced import get_gmail_service, get_unread_important_emails

            # Get Gmail service
            service = get_gmail_service()
            if not service:
                return SkillResult(
                    success=False,
                    error="Failed to authenticate with Gmail"
                )

            # Get emails
            emails = get_unread_important_emails(service)
            if emails is None:
                return SkillResult(
                    success=False,
                    error="Failed to fetch emails"
                )

            # Log skill execution
            self.audit_logger.log_event(
                EventType.EMAIL_RECEIVED,
                f"ReadEmailsSkill executed: {len(emails)} emails found",
                details={"count": len(emails)}
            )

            return SkillResult(
                success=True,
                data={
                    "count": len(emails),
                    "emails": [{"id": email['id']} for email in emails[:max_results]]
                },
                metadata={"max_results": max_results}
            )

        except Exception as e:
            self.audit_logger.log_error("skill_execution", str(e), None)
            return SkillResult(
                success=False,
                error=f"Error reading emails: {str(e)}"
            )


@register_skill
class ProcessEmailSkill(AgentSkill):
    """Process an email and create action file"""

    def __init__(self):
        super().__init__()
        self.audit_logger = AuditLogger("email_skill")

    def get_description(self) -> str:
        return "Process a specific email and create action file in Obsidian vault"

    def get_parameters(self) -> Dict[str, Dict[str, Any]]:
        return {
            "email_id": {
                "type": str,
                "required": True,
                "description": "Gmail message ID to process"
            }
        }

    def execute(self, **kwargs) -> SkillResult:
        """Execute email processing"""
        try:
            email_id = kwargs.get('email_id')

            # Import Gmail watcher functions
            from watcher.gmail_watcher_enhanced import (
                get_gmail_service,
                get_email_details,
                create_action_file
            )

            # Get Gmail service
            service = get_gmail_service()
            if not service:
                return SkillResult(
                    success=False,
                    error="Failed to authenticate with Gmail"
                )

            # Get email details
            email = get_email_details(service, email_id)
            if not email:
                return SkillResult(
                    success=False,
                    error=f"Failed to get email details for {email_id}"
                )

            # Create action file
            filepath = create_action_file(email)
            if not filepath:
                return SkillResult(
                    success=False,
                    error=f"Failed to create action file for {email_id}"
                )

            # Log skill execution
            self.audit_logger.log_event(
                EventType.EMAIL_PROCESSED,
                f"ProcessEmailSkill executed: {email_id}",
                details={
                    "email_id": email_id,
                    "file_path": str(filepath)
                }
            )

            return SkillResult(
                success=True,
                data={
                    "email_id": email_id,
                    "file_path": str(filepath),
                    "subject": email['subject'],
                    "from": email['from']
                }
            )

        except Exception as e:
            self.audit_logger.log_error("skill_execution", str(e), None)
            return SkillResult(
                success=False,
                error=f"Error processing email: {str(e)}"
            )


@register_skill
class GetEmailStatisticsSkill(AgentSkill):
    """Get email statistics from vault"""

    def __init__(self):
        super().__init__()
        self.vault_path = Path(__file__).parent.parent / "AI_Employee_Vault"
        self.emails_path = self.vault_path / "Emails"

    def get_description(self) -> str:
        return "Get statistics about emails in the vault"

    def get_parameters(self) -> Dict[str, Dict[str, Any]]:
        return {}

    def execute(self, **kwargs) -> SkillResult:
        """Execute statistics gathering"""
        try:
            if not self.emails_path.exists():
                return SkillResult(
                    success=True,
                    data={"total_emails": 0, "email_files": []}
                )

            # Count email files
            email_files = list(self.emails_path.glob("EMAIL-*.md"))

            return SkillResult(
                success=True,
                data={
                    "total_emails": len(email_files),
                    "email_files": [f.name for f in email_files]
                }
            )

        except Exception as e:
            return SkillResult(
                success=False,
                error=f"Error getting email statistics: {str(e)}"
            )
