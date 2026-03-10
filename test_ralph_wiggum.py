#!/usr/bin/env python3
"""
Test Ralph Wiggum Loop - Single Cycle
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from ralph_wiggum_loop import RalphWiggumLoop

def test_single_cycle():
    """Test a single autonomous cycle"""
    print("Testing Ralph Wiggum Loop - Single Cycle\n")

    # Create agent
    agent = RalphWiggumLoop(check_interval=5)

    # Run one cycle
    results = agent.execute_autonomous_cycle()

    print("\n" + "=" * 60)
    print("CYCLE RESULTS")
    print("=" * 60)
    print(f"Cycle: {results['cycle']}")
    print(f"Tasks found: {results['tasks_found']}")
    print(f"Tasks analyzed: {results['tasks_analyzed']}")
    print(f"Actions taken: {len(results['actions_taken'])}")

    if results['actions_taken']:
        print("\nActions:")
        for action in results['actions_taken']:
            print(f"  ✅ {action}")

    if results['errors']:
        print("\nErrors:")
        for error in results['errors']:
            print(f"  ❌ {error}")

    print(f"\nDuration: {results.get('duration_seconds', 0):.1f}s")
    print("\n✅ Test completed successfully!")

if __name__ == "__main__":
    test_single_cycle()
