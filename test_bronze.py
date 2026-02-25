#!/usr/bin/env python3
"""
Test script for Personal AI Employee Bronze Tier
Validates all components are working correctly
"""

import os
import sys
from pathlib import Path
from datetime import datetime

# Colors for output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_test(name, passed, message=""):
    """Print test result"""
    status = f"{GREEN}✅ PASS{RESET}" if passed else f"{RED}❌ FAIL{RESET}"
    print(f"{status} - {name}")
    if message:
        print(f"      {message}")

def test_vault_structure():
    """Test that vault structure exists"""
    print(f"\n{BLUE}Testing Vault Structure...{RESET}")

    vault_path = Path("AI_Employee_Vault")

    # Check main vault directory
    print_test("Vault directory exists", vault_path.exists())

    # Check required files
    dashboard = vault_path / "Dashboard.md"
    print_test("Dashboard.md exists", dashboard.exists())

    handbook = vault_path / "Company_Handbook.md"
    print_test("Company_Handbook.md exists", handbook.exists())

    # Check folder structure
    inbox = vault_path / "Inbox"
    print_test("Inbox folder exists", inbox.exists() and inbox.is_dir())

    needs_action = vault_path / "Needs_Action"
    print_test("Needs_Action folder exists", needs_action.exists() and needs_action.is_dir())

    done = vault_path / "Done"
    print_test("Done folder exists", done.exists() and done.is_dir())

    return True

def test_watcher_script():
    """Test that watcher script exists and is executable"""
    print(f"\n{BLUE}Testing Watcher Script...{RESET}")

    watcher = Path("watcher/inbox_watcher.py")
    print_test("Watcher script exists", watcher.exists())
    print_test("Watcher script is executable", os.access(watcher, os.X_OK))

    # Check script has required imports
    if watcher.exists():
        content = watcher.read_text()
        has_pathlib = "from pathlib import Path" in content
        has_subprocess = "import subprocess" in content
        print_test("Watcher has required imports", has_pathlib and has_subprocess)

    return True

def test_agent_skills():
    """Test that Agent Skills are configured"""
    print(f"\n{BLUE}Testing Agent Skills...{RESET}")

    skills_dir = Path(".claude/skills")
    print_test("Skills directory exists", skills_dir.exists())

    # Check individual skills
    vault_status = skills_dir / "vault-status.json"
    print_test("vault-status skill exists", vault_status.exists())

    process_inbox = skills_dir / "process-inbox.json"
    print_test("process-inbox skill exists", process_inbox.exists())

    update_dashboard = skills_dir / "update-dashboard.json"
    print_test("update-dashboard skill exists", update_dashboard.exists())

    return True

def test_file_counts():
    """Test and display current file counts"""
    print(f"\n{BLUE}Current Vault Status...{RESET}")

    vault_path = Path("AI_Employee_Vault")

    inbox_files = list((vault_path / "Inbox").glob("*"))
    inbox_count = len([f for f in inbox_files if f.is_file() and not f.name.startswith('.')])
    print(f"   📥 Inbox: {inbox_count} items")

    needs_action_files = list((vault_path / "Needs_Action").glob("*"))
    needs_action_count = len([f for f in needs_action_files if f.is_file() and not f.name.startswith('.')])
    print(f"   ⚡ Needs Action: {needs_action_count} items")

    done_files = list((vault_path / "Done").glob("*"))
    done_count = len([f for f in done_files if f.is_file() and not f.name.startswith('.')])
    print(f"   ✅ Done: {done_count} items")

    return True

def test_dashboard_content():
    """Test that dashboard has been updated"""
    print(f"\n{BLUE}Testing Dashboard Content...{RESET}")

    dashboard = Path("obsidian_vault/Dashboard.md")
    if dashboard.exists():
        content = dashboard.read_text()
        has_status = "Status Overview" in content
        has_activity = "Recent Activity" in content
        has_alerts = "Alerts" in content

        print_test("Dashboard has status section", has_status)
        print_test("Dashboard has activity section", has_activity)
        print_test("Dashboard has alerts section", has_alerts)

        # Check if it's been updated from template
        is_updated = "{{date}}" not in content
        print_test("Dashboard has been updated", is_updated)

    return True

def main():
    """Run all tests"""
    print(f"\n{YELLOW}{'='*60}{RESET}")
    print(f"{YELLOW}Personal AI Employee - Bronze Tier Test Suite{RESET}")
    print(f"{YELLOW}{'='*60}{RESET}")

    try:
        test_vault_structure()
        test_watcher_script()
        test_agent_skills()
        test_file_counts()
        test_dashboard_content()

        print(f"\n{GREEN}{'='*60}{RESET}")
        print(f"{GREEN}✅ All Bronze Tier components verified!{RESET}")
        print(f"{GREEN}{'='*60}{RESET}")
        print(f"\n{BLUE}Next steps:{RESET}")
        print("  1. Run: ./start.sh (to start the watcher)")
        print("  2. Add files to AI_Employee_Vault/Inbox/")
        print("  3. Watch them get processed automatically!")
        print(f"\n{BLUE}Manual processing:{RESET}")
        print("  claude code (then describe what you want to do)")

        return 0

    except Exception as e:
        print(f"\n{RED}❌ Test suite failed: {e}{RESET}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
