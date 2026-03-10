#!/usr/bin/env python3
"""
Ralph Wiggum Loop - Autonomous Task Execution Agent
Simple, persistent, autonomous agent that executes tasks continuously
"""

import sys
import time
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from agent_skills import execute_skill, list_skills
from audit_logger import AuditLogger, EventType


class RalphWiggumLoop:
    """
    Autonomous agent that continuously monitors and executes tasks

    Named after Ralph Wiggum from The Simpsons - simple, persistent, and always working
    """

    def __init__(self, check_interval: int = 300):
        """
        Initialize the autonomous agent

        Args:
            check_interval: Seconds between task checks (default: 5 minutes)
        """
        self.check_interval = check_interval
        self.audit_logger = AuditLogger("ralph_wiggum_loop")
        self.vault_path = Path(__file__).parent / "AI_Employee_Vault"
        self.running = False
        self.task_count = 0
        self.cycle_count = 0

    def log(self, message: str, level: str = "INFO"):
        """Log message with timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] [{level}] {message}")

    def get_pending_tasks(self) -> List[Dict[str, Any]]:
        """Get list of pending tasks from Needs_Action folder"""
        needs_action_path = self.vault_path / "Needs_Action"

        if not needs_action_path.exists():
            return []

        tasks = []
        for task_file in needs_action_path.glob("*.md"):
            tasks.append({
                "name": task_file.stem,
                "file_name": task_file.name,
                "file_path": str(task_file),
                "modified": datetime.fromtimestamp(task_file.stat().st_mtime)
            })

        # Sort by modified time (oldest first)
        tasks.sort(key=lambda x: x['modified'])

        return tasks

    def analyze_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze a task to determine what actions to take

        Returns:
            Dictionary with task analysis and recommended actions
        """
        task_name = task['name']

        # Determine task type from filename prefix
        task_type = "unknown"
        if task_name.startswith("EMAIL-"):
            task_type = "email"
        elif task_name.startswith("WHATSAPP-"):
            task_type = "whatsapp"
        elif task_name.startswith("TASK-"):
            task_type = "task"
        elif task_name.startswith("CRITICAL-"):
            task_type = "critical"

        # Read task content to understand priority
        try:
            with open(task['file_path'], 'r', encoding='utf-8') as f:
                content = f.read()

            # Determine priority from content
            priority = "normal"
            if "🔴" in content or "CRITICAL" in content.upper():
                priority = "critical"
            elif "🟠" in content or "IMPORTANT" in content.upper():
                priority = "high"
            elif "🟡" in content or "URGENT" in content.upper():
                priority = "high"

        except Exception as e:
            self.log(f"Error reading task content: {e}", "WARNING")
            content = ""
            priority = "normal"

        return {
            "task": task,
            "task_type": task_type,
            "priority": priority,
            "content_preview": content[:200] if content else "",
            "recommended_actions": self.get_recommended_actions(task_type, priority)
        }

    def get_recommended_actions(self, task_type: str, priority: str) -> List[str]:
        """Get recommended actions based on task type and priority"""
        actions = []

        if task_type == "email":
            actions.append("Review email content")
            actions.append("Draft response if needed")
            actions.append("Move to In_Progress or Done")

        elif task_type == "whatsapp":
            actions.append("Review WhatsApp conversation")
            actions.append("Identify action items")
            actions.append("Move to In_Progress or Done")

        elif task_type == "task":
            actions.append("Review task requirements")
            actions.append("Execute task steps")
            actions.append("Move to In_Progress when started")
            actions.append("Move to Done when completed")

        elif task_type == "critical":
            actions.append("⚠️ URGENT: Address immediately")
            actions.append("Escalate if needed")
            actions.append("Move to In_Progress")

        else:
            actions.append("Review and categorize")
            actions.append("Determine next steps")

        return actions

    def execute_autonomous_cycle(self) -> Dict[str, Any]:
        """
        Execute one autonomous cycle

        Returns:
            Dictionary with cycle results
        """
        self.cycle_count += 1
        cycle_start = datetime.now()

        self.log(f"🔄 Starting autonomous cycle #{self.cycle_count}")

        results = {
            "cycle": self.cycle_count,
            "start_time": cycle_start.isoformat(),
            "tasks_found": 0,
            "tasks_analyzed": 0,
            "actions_taken": [],
            "errors": []
        }

        try:
            # 1. Check system health
            self.log("🏥 Checking system health...")
            health_result = execute_skill("GetAuditStatisticsSkill", days=1)

            if health_result.success:
                stats = health_result.data
                success_rate = (stats['success_count'] / stats['total_events'] * 100) if stats['total_events'] > 0 else 100
                self.log(f"   System health: {success_rate:.1f}% success rate, {stats['total_events']} events")
            else:
                self.log(f"   ⚠️ Could not check system health: {health_result.error}", "WARNING")

            # 2. Get pending tasks
            self.log("📋 Checking for pending tasks...")
            pending_tasks = self.get_pending_tasks()
            results['tasks_found'] = len(pending_tasks)

            if not pending_tasks:
                self.log("   ✅ No pending tasks found")
                return results

            self.log(f"   Found {len(pending_tasks)} pending task(s)")

            # 3. Analyze tasks
            self.log("🔍 Analyzing tasks...")
            analyzed_tasks = []

            for task in pending_tasks[:5]:  # Analyze top 5 tasks
                analysis = self.analyze_task(task)
                analyzed_tasks.append(analysis)
                results['tasks_analyzed'] += 1

                self.log(f"   📄 {task['name']}")
                self.log(f"      Type: {analysis['task_type']}, Priority: {analysis['priority']}")

            # 4. Execute automated actions
            self.log("⚡ Executing automated actions...")

            # Generate reports
            self.log("   📊 Generating CEO briefing...")
            briefing_result = execute_skill("GenerateCEOBriefingSkill")
            if briefing_result.success:
                self.log("      ✅ CEO briefing generated")
                results['actions_taken'].append("Generated CEO briefing")
            else:
                self.log(f"      ❌ Failed: {briefing_result.error}", "ERROR")
                results['errors'].append(f"CEO briefing: {briefing_result.error}")

            self.log("   📊 Generating audit summary...")
            audit_result = execute_skill("GenerateAuditSummarySkill")
            if audit_result.success:
                self.log("      ✅ Audit summary generated")
                results['actions_taken'].append("Generated audit summary")
            else:
                self.log(f"      ❌ Failed: {audit_result.error}", "ERROR")
                results['errors'].append(f"Audit summary: {audit_result.error}")

            # 5. Log cycle completion
            cycle_end = datetime.now()
            duration = (cycle_end - cycle_start).total_seconds()
            results['end_time'] = cycle_end.isoformat()
            results['duration_seconds'] = duration

            self.log(f"✅ Cycle #{self.cycle_count} completed in {duration:.1f}s")

            # Audit log
            self.audit_logger.log_event(
                EventType.SYSTEM_HEALTH_CHECK,
                f"Ralph Wiggum Loop cycle #{self.cycle_count} completed",
                details=results
            )

            return results

        except Exception as e:
            self.log(f"❌ Error in autonomous cycle: {e}", "ERROR")
            results['errors'].append(str(e))
            self.audit_logger.log_error("autonomous_cycle", str(e), None)
            return results

    def run(self):
        """Run the autonomous loop continuously"""
        self.running = True

        self.log("=" * 60)
        self.log("🤖 Ralph Wiggum Loop - Autonomous Agent Starting")
        self.log("=" * 60)
        self.log(f"📁 Vault path: {self.vault_path}")
        self.log(f"⏱️ Check interval: {self.check_interval} seconds")
        self.log("")

        # Log system start
        self.audit_logger.log_system_start()

        try:
            while self.running:
                # Execute autonomous cycle
                results = self.execute_autonomous_cycle()

                # Wait before next cycle
                self.log(f"⏳ Waiting {self.check_interval} seconds until next cycle...")
                self.log("")

                time.sleep(self.check_interval)

        except KeyboardInterrupt:
            self.log("\n👋 Ralph Wiggum Loop stopped by user")
            self.audit_logger.log_system_stop("user_interrupt")

        except Exception as e:
            self.log(f"💥 Fatal error: {e}", "ERROR")
            self.audit_logger.log_error("fatal_error", str(e), None)
            self.audit_logger.log_system_stop("fatal_error")
            raise

    def stop(self):
        """Stop the autonomous loop"""
        self.running = False
        self.log("🛑 Stopping Ralph Wiggum Loop...")


def main():
    """Main function"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Ralph Wiggum Loop - Autonomous Task Execution Agent",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run with default 5-minute interval
  python3 ralph_wiggum_loop.py

  # Run with 10-minute interval
  python3 ralph_wiggum_loop.py --interval 600

  # Run in background
  nohup python3 ralph_wiggum_loop.py > logs/ralph-wiggum.log 2>&1 &
        """
    )

    parser.add_argument(
        '--interval',
        type=int,
        default=300,
        help='Check interval in seconds (default: 300 = 5 minutes)'
    )

    args = parser.parse_args()

    # Create and run agent
    agent = RalphWiggumLoop(check_interval=args.interval)

    try:
        agent.run()
    except KeyboardInterrupt:
        agent.stop()


if __name__ == "__main__":
    main()
