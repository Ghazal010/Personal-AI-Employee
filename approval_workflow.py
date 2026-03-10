#!/usr/bin/env python3
"""
Human-in-the-Loop Approval Workflow
Manages approval for sensitive actions
"""

import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional, List
from enum import Enum

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from audit_logger import AuditLogger

# Setup audit logger
audit_logger = AuditLogger("approval_workflow")


class ActionSensitivity(Enum):
    """Action sensitivity levels"""
    LOW = "low"           # Auto-approve
    MEDIUM = "medium"     # Prompt for approval
    HIGH = "high"         # Always require approval
    CRITICAL = "critical" # Require approval + confirmation


class ApprovalStatus(Enum):
    """Approval status"""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    AUTO_APPROVED = "auto_approved"


class ApprovalWorkflow:
    """
    Human-in-the-Loop Approval System

    Features:
    - Sensitivity-based approval requirements
    - Auto-approval for low-risk actions
    - Approval history and audit trail
    - Configurable approval rules
    """

    def __init__(self):
        self.vault_path = Path(__file__).parent / "AI_Employee_Vault"
        self.approvals_dir = self.vault_path / "Approvals"
        self.approvals_dir.mkdir(exist_ok=True)

        self.config_file = Path(__file__).parent / "approval_config.json"
        self.load_config()

    def load_config(self):
        """Load approval configuration"""
        default_config = {
            "auto_approve_low": True,
            "require_confirmation_critical": True,
            "approval_timeout_seconds": 300,
            "sensitive_actions": {
                # Social Media
                "PostTweetSkill": "MEDIUM",
                "PostToFacebookSkill": "MEDIUM",
                "PostToInstagramSkill": "MEDIUM",

                # Email
                "SendEmailSkill": "HIGH",
                "DeleteEmailSkill": "CRITICAL",

                # Business Operations
                "CreateOdooInvoiceSkill": "HIGH",
                "DeleteOdooInvoiceSkill": "CRITICAL",
                "CreateOdooCustomerSkill": "MEDIUM",

                # File Operations
                "DeleteFileSkill": "CRITICAL",
                "MoveTaskSkill": "LOW",

                # System Operations
                "ExecuteCommandSkill": "CRITICAL",
                "ModifySystemConfigSkill": "CRITICAL"
            }
        }

        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    self.config = json.load(f)
            except Exception as e:
                print(f"⚠ Failed to load config, using defaults: {e}")
                self.config = default_config
        else:
            self.config = default_config
            self.save_config()

    def save_config(self):
        """Save approval configuration"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, indent=2, fp=f)
        except Exception as e:
            print(f"⚠ Failed to save config: {e}")

    def get_action_sensitivity(self, action_name: str) -> ActionSensitivity:
        """Get sensitivity level for an action"""
        sensitivity_str = self.config['sensitive_actions'].get(
            action_name,
            "MEDIUM"
        )
        return ActionSensitivity[sensitivity_str]

    def request_approval(
        self,
        action_name: str,
        action_params: Dict[str, Any],
        description: str = ""
    ) -> bool:
        """
        Request approval for an action

        Args:
            action_name: Name of the action/skill
            action_params: Parameters for the action
            description: Human-readable description

        Returns:
            True if approved, False if rejected
        """
        sensitivity = self.get_action_sensitivity(action_name)

        # Auto-approve low sensitivity actions
        if sensitivity == ActionSensitivity.LOW and self.config['auto_approve_low']:
            self._log_approval(action_name, action_params, ApprovalStatus.AUTO_APPROVED)
            return True

        # Create approval request
        approval_id = datetime.now().strftime('%Y%m%d%H%M%S')
        approval_data = {
            'id': approval_id,
            'timestamp': datetime.now().isoformat(),
            'action_name': action_name,
            'action_params': action_params,
            'description': description,
            'sensitivity': sensitivity.value,
            'status': ApprovalStatus.PENDING.value
        }

        # Display approval request
        print("\n" + "=" * 60)
        print("🔔 APPROVAL REQUIRED")
        print("=" * 60)
        print(f"\n📋 Action: {action_name}")
        print(f"🎯 Sensitivity: {sensitivity.value.upper()}")
        if description:
            print(f"📝 Description: {description}")
        print(f"\n⚙️  Parameters:")
        for key, value in action_params.items():
            print(f"   • {key}: {value}")
        print()

        # Get user input
        if sensitivity == ActionSensitivity.CRITICAL:
            print("⚠️  CRITICAL ACTION - Requires confirmation")
            response = input("Type 'APPROVE' to proceed, anything else to reject: ").strip()
            approved = response == "APPROVE"
        else:
            response = input("Approve this action? (y/n): ").strip().lower()
            approved = response in ['y', 'yes']

        # Update status
        status = ApprovalStatus.APPROVED if approved else ApprovalStatus.REJECTED
        approval_data['status'] = status.value
        approval_data['response_time'] = datetime.now().isoformat()

        # Save approval record
        self._save_approval_record(approval_id, approval_data)

        # Log to audit
        self._log_approval(action_name, action_params, status)

        # Display result
        if approved:
            print("✅ Action APPROVED")
        else:
            print("❌ Action REJECTED")
        print("=" * 60)
        print()

        return approved

    def _save_approval_record(self, approval_id: str, data: Dict[str, Any]):
        """Save approval record to file"""
        try:
            approval_file = self.approvals_dir / f"APPROVAL-{approval_id}.json"
            with open(approval_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"⚠ Failed to save approval record: {e}")

    def _log_approval(self, action_name: str, params: Dict[str, Any], status: ApprovalStatus):
        """Log approval to audit system"""
        audit_logger.log_event(
            "approval_decision",
            f"Action {action_name}: {status.value}",
            details={
                'action': action_name,
                'params': params,
                'status': status.value
            }
        )

    def get_approval_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent approval history"""
        approvals = []

        try:
            approval_files = sorted(
                self.approvals_dir.glob("APPROVAL-*.json"),
                reverse=True
            )[:limit]

            for file in approval_files:
                with open(file, 'r') as f:
                    approvals.append(json.load(f))

        except Exception as e:
            print(f"⚠ Failed to load approval history: {e}")

        return approvals

    def generate_approval_report(self) -> str:
        """Generate approval history report"""
        history = self.get_approval_history(limit=50)

        if not history:
            return "No approval history found."

        # Count by status
        approved = sum(1 for a in history if a['status'] == 'approved')
        rejected = sum(1 for a in history if a['status'] == 'rejected')
        auto_approved = sum(1 for a in history if a['status'] == 'auto_approved')

        report = f"""# Approval History Report

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Total Requests:** {len(history)}

## Summary

- ✅ Approved: {approved}
- ❌ Rejected: {rejected}
- 🤖 Auto-Approved: {auto_approved}

## Recent Approvals

"""

        for approval in history[:20]:
            status_emoji = {
                'approved': '✅',
                'rejected': '❌',
                'auto_approved': '🤖',
                'pending': '⏳'
            }.get(approval['status'], '❓')

            report += f"""### {status_emoji} {approval['action_name']}
**Time:** {approval['timestamp']}
**Status:** {approval['status'].upper()}
**Sensitivity:** {approval['sensitivity'].upper()}

"""

        return report


# Global approval workflow instance
approval_workflow = ApprovalWorkflow()


def require_approval(action_name: str, action_params: Dict[str, Any], description: str = "") -> bool:
    """
    Decorator/function to require approval for an action

    Usage:
        if require_approval('PostTweetSkill', {'text': 'Hello'}, 'Posting tweet'):
            # Execute action
            post_tweet(text)
        else:
            # Action rejected
            print("Action cancelled by user")
    """
    return approval_workflow.request_approval(action_name, action_params, description)


def main():
    """Test approval workflow"""
    print("=" * 60)
    print("Approval Workflow - Test")
    print("=" * 60)
    print()

    # Test 1: Low sensitivity (auto-approve)
    print("Test 1: Low sensitivity action")
    approved = require_approval(
        'MoveTaskSkill',
        {'task': 'test.md', 'destination': 'Done'},
        'Moving task to Done folder'
    )
    print(f"Result: {'Approved' if approved else 'Rejected'}\n")

    # Test 2: Medium sensitivity
    print("Test 2: Medium sensitivity action")
    approved = require_approval(
        'PostTweetSkill',
        {'text': 'Hello from AI Employee!'},
        'Posting tweet to Twitter'
    )
    print(f"Result: {'Approved' if approved else 'Rejected'}\n")

    # Test 3: High sensitivity
    print("Test 3: High sensitivity action")
    approved = require_approval(
        'CreateOdooInvoiceSkill',
        {'partner_id': 7, 'amount': 1000.0},
        'Creating invoice for $1000'
    )
    print(f"Result: {'Approved' if approved else 'Rejected'}\n")

    # Test 4: Critical sensitivity
    print("Test 4: Critical sensitivity action")
    approved = require_approval(
        'DeleteEmailSkill',
        {'email_id': '12345'},
        'Permanently deleting email'
    )
    print(f"Result: {'Approved' if approved else 'Rejected'}\n")

    # Generate report
    print("\n" + "=" * 60)
    print("Generating approval report...")
    print("=" * 60)
    report = approval_workflow.generate_approval_report()
    print(report)


if __name__ == "__main__":
    main()
