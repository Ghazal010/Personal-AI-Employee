#!/usr/bin/env python3
"""
Plan.md Generator - Claude Reasoning Loop
Analyzes current state and generates actionable plans
"""

import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from agent_skills import execute_skill
from audit_logger import AuditLogger

# Setup audit logger
audit_logger = AuditLogger("plan_generator")


class PlanGenerator:
    """
    Claude Reasoning Loop for Plan Generation

    Analyzes:
    - Current tasks and priorities
    - Email backlog
    - WhatsApp conversations
    - Social media mentions
    - Business operations (Odoo)

    Generates:
    - Actionable plans with priorities
    - Time estimates
    - Dependencies
    - Success criteria
    """

    def __init__(self):
        self.vault_path = Path(__file__).parent / "AI_Employee_Vault"
        self.plan_file = self.vault_path / "Plan.md"

    def analyze_current_state(self) -> Dict[str, Any]:
        """Analyze current system state"""
        print("🔍 Analyzing current state...")

        state = {
            'timestamp': datetime.now().isoformat(),
            'tasks': {},
            'emails': {},
            'whatsapp': {},
            'social_media': {},
            'business': {},
            'priorities': []
        }

        # Get task statistics
        try:
            task_result = execute_skill('GetTaskStatisticsSkill')
            if task_result.success:
                state['tasks'] = task_result.data
                print(f"  ✓ Tasks analyzed: {task_result.data.get('total_tasks', 0)} total")
        except Exception as e:
            print(f"  ⚠ Task analysis failed: {e}")

        # Get email statistics
        try:
            email_result = execute_skill('GetEmailStatisticsSkill')
            if email_result.success:
                state['emails'] = email_result.data
                print(f"  ✓ Emails analyzed: {email_result.data.get('total_emails', 0)} total")
        except Exception as e:
            print(f"  ⚠ Email analysis failed: {e}")

        # Get WhatsApp statistics
        try:
            whatsapp_result = execute_skill('GetWhatsAppStatisticsSkill')
            if whatsapp_result.success:
                state['whatsapp'] = whatsapp_result.data
                print(f"  ✓ WhatsApp analyzed: {whatsapp_result.data.get('total_chats', 0)} chats")
        except Exception as e:
            print(f"  ⚠ WhatsApp analysis failed: {e}")

        # Get social media statistics
        try:
            social_result = execute_skill('GetSocialMediaStatisticsSkill')
            if social_result.success:
                state['social_media'] = social_result.data
                print(f"  ✓ Social media analyzed")
        except Exception as e:
            print(f"  ⚠ Social media analysis failed: {e}")

        # Get Odoo statistics (if available)
        try:
            customers_result = execute_skill('GetOdooCustomersSkill', limit=5)
            if customers_result.success:
                state['business']['customers'] = customers_result.data.get('count', 0)
                print(f"  ✓ Business data analyzed: {state['business']['customers']} customers")
        except Exception as e:
            print(f"  ⚠ Business analysis skipped: {e}")

        return state

    def generate_priorities(self, state: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate prioritized action items"""
        print("\n🎯 Generating priorities...")

        priorities = []

        # Priority 1: Pending tasks in Needs_Action
        needs_action = state['tasks'].get('needs_action', 0)
        if needs_action > 0:
            priorities.append({
                'priority': 'HIGH',
                'category': 'Tasks',
                'action': f'Process {needs_action} pending tasks',
                'location': 'AI_Employee_Vault/Needs_Action/',
                'estimated_time': f'{needs_action * 10} minutes',
                'success_criteria': 'All tasks moved to Done or have clear next steps'
            })

        # Priority 2: Unprocessed emails
        total_emails = state['emails'].get('total_emails', 0)
        if total_emails > 5:
            priorities.append({
                'priority': 'HIGH',
                'category': 'Email',
                'action': f'Review and respond to {total_emails} emails',
                'location': 'AI_Employee_Vault/Emails/',
                'estimated_time': f'{total_emails * 5} minutes',
                'success_criteria': 'All emails categorized and responded to'
            })

        # Priority 3: WhatsApp conversations
        total_chats = state['whatsapp'].get('total_chats', 0)
        if total_chats > 0:
            priorities.append({
                'priority': 'MEDIUM',
                'category': 'WhatsApp',
                'action': f'Review {total_chats} WhatsApp conversations',
                'location': 'AI_Employee_Vault/WhatsApp_Chats/',
                'estimated_time': f'{total_chats * 3} minutes',
                'success_criteria': 'All conversations reviewed and responded to'
            })

        # Priority 4: Social media engagement
        twitter_mentions = state['social_media'].get('twitter', {}).get('mentions', 0)
        if twitter_mentions > 0:
            priorities.append({
                'priority': 'MEDIUM',
                'category': 'Social Media',
                'action': f'Respond to {twitter_mentions} Twitter mentions',
                'location': 'Twitter',
                'estimated_time': f'{twitter_mentions * 2} minutes',
                'success_criteria': 'All mentions acknowledged or responded to'
            })

        # Priority 5: Business operations
        customers = state['business'].get('customers', 0)
        if customers > 0:
            priorities.append({
                'priority': 'LOW',
                'category': 'Business',
                'action': 'Review customer pipeline and follow-ups',
                'location': 'Odoo ERP',
                'estimated_time': '15 minutes',
                'success_criteria': 'All customers have recent activity or scheduled follow-up'
            })

        # Priority 6: System maintenance
        priorities.append({
            'priority': 'LOW',
            'category': 'System',
            'action': 'Review audit logs and system health',
            'location': 'AI_Employee_Vault/Audit_Logs.md',
            'estimated_time': '10 minutes',
            'success_criteria': 'No errors or warnings in logs'
        })

        print(f"  ✓ Generated {len(priorities)} priority items")
        return priorities

    def generate_plan_markdown(self, state: Dict[str, Any], priorities: List[Dict[str, Any]]) -> str:
        """Generate Plan.md content"""
        print("\n📝 Generating Plan.md...")

        content = f"""# Action Plan

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Status:** Active

---

## 📊 Current State Summary

### Tasks
- **Total Tasks:** {state['tasks'].get('total_tasks', 0)}
- **Inbox:** {state['tasks'].get('inbox', 0)}
- **Needs Action:** {state['tasks'].get('needs_action', 0)}
- **Done:** {state['tasks'].get('done', 0)}

### Communications
- **Emails:** {state['emails'].get('total_emails', 0)} total
- **WhatsApp Chats:** {state['whatsapp'].get('total_chats', 0)} conversations
- **Twitter Mentions:** {state['social_media'].get('twitter', {}).get('mentions', 0)} mentions

### Business
- **Customers:** {state['business'].get('customers', 'N/A')}
- **Invoices:** Pending review
- **Expenses:** Pending review

---

## 🎯 Priority Actions

"""

        # Add priorities
        for i, priority in enumerate(priorities, 1):
            content += f"""### {i}. {priority['action']} [{priority['priority']}]

**Category:** {priority['category']}
**Location:** {priority['location']}
**Estimated Time:** {priority['estimated_time']}
**Success Criteria:** {priority['success_criteria']}

**Next Steps:**
- [ ] Review items in {priority['location']}
- [ ] Take appropriate action
- [ ] Update status
- [ ] Mark as complete

---

"""

        # Add recommendations
        content += """## 💡 Recommendations

### Immediate Actions (Today)
- Process all HIGH priority items
- Respond to urgent communications
- Update task statuses

### Short-term Actions (This Week)
- Complete all MEDIUM priority items
- Review business pipeline
- Generate weekly CEO briefing

### Long-term Actions (This Month)
- Optimize automation workflows
- Review and update system documentation
- Plan new integrations

---

## 📈 Success Metrics

- [ ] All HIGH priority items completed
- [ ] Inbox at zero or near-zero
- [ ] All communications responded to within 24 hours
- [ ] Business operations up to date
- [ ] System health at 100%

---

## 🔄 Next Plan Generation

This plan will be regenerated:
- Automatically every 24 hours
- When significant state changes occur
- On manual request

**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

*Generated by Claude Reasoning Loop*
"""

        return content

    def save_plan(self, content: str):
        """Save Plan.md to vault"""
        print("\n💾 Saving Plan.md...")

        try:
            self.plan_file.write_text(content, encoding='utf-8')
            print(f"  ✓ Plan saved to: {self.plan_file}")

            # Log to audit
            audit_logger.log_event(
                "plan_generated",
                "Plan.md generated successfully",
                details={'file': str(self.plan_file)}
            )

        except Exception as e:
            print(f"  ✗ Failed to save plan: {e}")
            audit_logger.log_error("plan_save_failed", str(e), None)

    def generate(self):
        """Main generation workflow"""
        print("=" * 60)
        print("Plan.md Generator - Claude Reasoning Loop")
        print("=" * 60)
        print()

        # Step 1: Analyze current state
        state = self.analyze_current_state()

        # Step 2: Generate priorities
        priorities = self.generate_priorities(state)

        # Step 3: Generate plan markdown
        content = self.generate_plan_markdown(state, priorities)

        # Step 4: Save plan
        self.save_plan(content)

        print()
        print("✅ Plan generation complete!")
        print(f"📄 View plan: {self.plan_file}")
        print()


def main():
    """Generate Plan.md"""
    generator = PlanGenerator()
    generator.generate()


if __name__ == "__main__":
    main()
