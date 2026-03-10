#!/usr/bin/env python3
"""
WhatsApp Skills
Skills for WhatsApp chat operations
"""

import sys
from pathlib import Path
from typing import Dict, Any, List

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agent_skills.skill_framework import AgentSkill, SkillResult, register_skill
from audit_logger import AuditLogger, EventType


@register_skill
class ProcessWhatsAppChatSkill(AgentSkill):
    """Process a WhatsApp chat export file"""

    def __init__(self):
        super().__init__()
        self.audit_logger = AuditLogger("whatsapp_skill")
        self.inbox_path = Path(__file__).parent.parent / "whatsapp_integration" / "whatsapp_inbox"

    def get_description(self) -> str:
        return "Process a WhatsApp chat export file and create action file"

    def get_parameters(self) -> Dict[str, Dict[str, Any]]:
        return {
            "file_path": {
                "type": str,
                "required": True,
                "description": "Path to WhatsApp chat export .txt file"
            }
        }

    def execute(self, **kwargs) -> SkillResult:
        """Execute WhatsApp chat processing"""
        try:
            file_path = Path(kwargs.get('file_path'))

            if not file_path.exists():
                return SkillResult(
                    success=False,
                    error=f"File not found: {file_path}"
                )

            # Import WhatsApp monitor functions
            from whatsapp_integration.whatsapp_monitor_enhanced import (
                parse_whatsapp_export,
                create_action_file
            )

            # Parse chat
            chat_data = parse_whatsapp_export(file_path)
            if not chat_data:
                return SkillResult(
                    success=False,
                    error=f"Failed to parse chat: {file_path}"
                )

            # Create action file
            success = create_action_file(chat_data)
            if not success:
                return SkillResult(
                    success=False,
                    error=f"Failed to create action file for: {file_path}"
                )

            # Log skill execution
            self.audit_logger.log_event(
                EventType.WHATSAPP_PROCESSED,
                f"ProcessWhatsAppChatSkill executed: {file_path.name}",
                details={
                    "file_name": file_path.name,
                    "chat_name": chat_data['chat_name'],
                    "message_count": chat_data['total_messages']
                }
            )

            return SkillResult(
                success=True,
                data={
                    "file_name": file_path.name,
                    "chat_name": chat_data['chat_name'],
                    "total_messages": chat_data['total_messages']
                }
            )

        except Exception as e:
            self.audit_logger.log_error("skill_execution", str(e), None)
            return SkillResult(
                success=False,
                error=f"Error processing WhatsApp chat: {str(e)}"
            )


@register_skill
class GetWhatsAppStatisticsSkill(AgentSkill):
    """Get WhatsApp chat statistics from vault"""

    def __init__(self):
        super().__init__()
        self.vault_path = Path(__file__).parent.parent / "AI_Employee_Vault"
        self.whatsapp_path = self.vault_path / "WhatsApp_Chats"

    def get_description(self) -> str:
        return "Get statistics about WhatsApp chats in the vault"

    def get_parameters(self) -> Dict[str, Dict[str, Any]]:
        return {}

    def execute(self, **kwargs) -> SkillResult:
        """Execute statistics gathering"""
        try:
            if not self.whatsapp_path.exists():
                return SkillResult(
                    success=True,
                    data={"total_chats": 0, "chat_files": []}
                )

            # Count chat files
            chat_files = list(self.whatsapp_path.glob("WHATSAPP-*.md"))

            return SkillResult(
                success=True,
                data={
                    "total_chats": len(chat_files),
                    "chat_files": [f.name for f in chat_files]
                }
            )

        except Exception as e:
            return SkillResult(
                success=False,
                error=f"Error getting WhatsApp statistics: {str(e)}"
            )


@register_skill
class ListPendingWhatsAppChatsSkill(AgentSkill):
    """List pending WhatsApp chat exports in inbox"""

    def __init__(self):
        super().__init__()
        self.inbox_path = Path(__file__).parent.parent / "whatsapp_integration" / "whatsapp_inbox"

    def get_description(self) -> str:
        return "List pending WhatsApp chat exports waiting to be processed"

    def get_parameters(self) -> Dict[str, Dict[str, Any]]:
        return {}

    def execute(self, **kwargs) -> SkillResult:
        """Execute listing"""
        try:
            if not self.inbox_path.exists():
                return SkillResult(
                    success=True,
                    data={"pending_chats": 0, "files": []}
                )

            # List .txt files
            txt_files = list(self.inbox_path.glob("*.txt"))

            return SkillResult(
                success=True,
                data={
                    "pending_chats": len(txt_files),
                    "files": [f.name for f in txt_files]
                }
            )

        except Exception as e:
            return SkillResult(
                success=False,
                error=f"Error listing pending chats: {str(e)}"
            )
