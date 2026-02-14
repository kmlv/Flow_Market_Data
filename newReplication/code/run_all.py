"""
Run the full analysis pipeline, including robustness checks.

1. Runs data.py with default 5-second intervals (generates Tables 1-6, S1, S8, all figures)
2. Runs data.py --interval 10 (generates Tables S2-S4: 10-second robustness)
3. Runs data.py --interval 2  (generates Tables S5-S7: 2-second robustness)

Usage:
    python run_all.py
"""

import subprocess
import sys
import os

CODE_DIR = os.path.dirname(os.path.abspath(__file__))


def run_interval(interval=None):
    """Run data.py, optionally with a specific interval size."""
    cmd = [sys.executable, os.path.join(CODE_DIR, 'data.py')]
    label = '5s (default)'
    if interval is not None:
        cmd += ['--interval', str(interval)]
        label = f'{interval}s'

    print(f"\n{'=' * 60}")
    print(f"  Running analysis: price_interval_size = {label}")
    print(f"{'=' * 60}\n")

    result = subprocess.run(cmd, cwd=CODE_DIR)
    if result.returncode != 0:
        print(f"\nERROR: data.py failed for {label}")
        return False
    return True


if __name__ == "__main__":
    success = True
    for interval in [None, 10, 2]:
        if not run_interval(interval):
            success = False
            break

    if success:
        print(f"\n{'=' * 60}")
        print("  All runs completed successfully.")
        print(f"{'=' * 60}")
    else:
        print(f"\n{'=' * 60}")
        print("  Pipeline failed. Check errors above.")
        print(f"{'=' * 60}")
        sys.exit(1)
