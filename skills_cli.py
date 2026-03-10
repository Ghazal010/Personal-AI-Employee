#!/usr/bin/env python3
"""
Agent Skills CLI
Command-line interface for executing agent skills
"""

import sys
import json
import argparse
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from agent_skills import list_skills, execute_skill


def print_skills():
    """Print all available skills"""
    skills = list_skills()

    print("\n" + "=" * 60)
    print("AVAILABLE AGENT SKILLS")
    print("=" * 60 + "\n")

    for skill in skills:
        print(f"📦 {skill['name']}")
        print(f"   {skill['description']}")
        print(f"   Version: {skill['version']}")

        if skill['parameters']:
            print(f"   Parameters:")
            for param_name, param_def in skill['parameters'].items():
                required = "required" if param_def.get('required', False) else "optional"
                param_type = param_def.get('type', type).__name__
                default = param_def.get('default', 'N/A')
                desc = param_def.get('description', 'No description')
                print(f"      - {param_name} ({param_type}, {required}): {desc}")
                if not param_def.get('required', False):
                    print(f"        Default: {default}")
        else:
            print(f"   Parameters: None")

        print()


def execute_skill_cli(skill_name: str, params: dict):
    """Execute a skill and print results"""
    print(f"\n🚀 Executing skill: {skill_name}")
    print(f"📋 Parameters: {json.dumps(params, indent=2)}\n")

    result = execute_skill(skill_name, **params)

    print("=" * 60)
    print("RESULT")
    print("=" * 60)

    if result.success:
        print("✅ Status: SUCCESS\n")
        print("📊 Data:")
        print(json.dumps(result.data, indent=2))

        if result.metadata:
            print("\n📝 Metadata:")
            print(json.dumps(result.metadata, indent=2))
    else:
        print("❌ Status: FAILURE\n")
        print(f"⚠️ Error: {result.error}")

    print(f"\n⏰ Timestamp: {result.timestamp}")
    print()


def main():
    """Main CLI function"""
    parser = argparse.ArgumentParser(
        description="Agent Skills CLI - Execute modular AI agent capabilities",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # List all available skills
  python3 skills_cli.py --list

  # Get email statistics
  python3 skills_cli.py --skill GetEmailStatisticsSkill

  # Get audit statistics for last 30 days
  python3 skills_cli.py --skill GetAuditStatisticsSkill --params '{"days": 30}'

  # Generate CEO briefing
  python3 skills_cli.py --skill GenerateCEOBriefingSkill

  # List tasks in needs_action stage
  python3 skills_cli.py --skill ListTasksSkill --params '{"stage": "needs_action"}'

  # Create a new task
  python3 skills_cli.py --skill CreateTaskSkill --params '{"title": "Review code", "description": "Review PR #123", "priority": "high"}'
        """
    )

    parser.add_argument(
        '--list',
        action='store_true',
        help='List all available skills'
    )

    parser.add_argument(
        '--skill',
        type=str,
        help='Name of the skill to execute'
    )

    parser.add_argument(
        '--params',
        type=str,
        default='{}',
        help='JSON string of parameters for the skill'
    )

    args = parser.parse_args()

    # List skills
    if args.list:
        print_skills()
        return

    # Execute skill
    if args.skill:
        try:
            params = json.loads(args.params)
        except json.JSONDecodeError as e:
            print(f"❌ Error: Invalid JSON in --params: {e}")
            sys.exit(1)

        execute_skill_cli(args.skill, params)
        return

    # No action specified
    parser.print_help()


if __name__ == "__main__":
    main()
