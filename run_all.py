"""
Run the full analysis pipeline for all robustness specifications.

Runs data.py three times with price_interval_size = 2, 5, and 10,
saving outputs to tables_Xs/ and figures_Xs/ folders respectively.

Usage:
    python run_all.py
"""

import subprocess
import sys
import os
import shutil

INTERVALS = [5, 2, 10]
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(BASE_DIR, "config.py")

def run_interval(interval):
    """Run data.py with a specific price_interval_size."""
    print(f"\n{'='*60}")
    print(f"  Running analysis with price_interval_size = {interval}")
    print(f"{'='*60}\n")

    # Read config.py and set the interval
    with open(CONFIG_FILE, "r") as f:
        config_text = f.read()

    original_text = config_text
    import re
    config_text = re.sub(
        r"^price_interval_size\s*=\s*\d+",
        f"price_interval_size = {interval}",
        config_text,
        flags=re.MULTILINE,
    )
    with open(CONFIG_FILE, "w") as f:
        f.write(config_text)

    try:
        result = subprocess.run(
            [sys.executable, os.path.join(BASE_DIR, "data.py")],
            cwd=BASE_DIR,
        )
        if result.returncode != 0:
            print(f"\nERROR: data.py failed for interval {interval}")
            return False
    finally:
        # Restore original config
        with open(CONFIG_FILE, "w") as f:
            f.write(original_text)

    # Move outputs to interval-specific folders
    for folder in ["tables", "figures"]:
        src = os.path.join(BASE_DIR, folder)
        dst = os.path.join(BASE_DIR, f"{folder}_{interval}s")
        if os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.copytree(src, dst)

    print(f"\nOutputs saved to tables_{interval}s/ and figures_{interval}s/")
    return True


if __name__ == "__main__":
    success = True
    for interval in INTERVALS:
        if not run_interval(interval):
            success = False
            break

    if success:
        print(f"\n{'='*60}")
        print("  All runs completed successfully.")
        print(f"{'='*60}")
    else:
        print(f"\n{'='*60}")
        print("  Pipeline failed. Check errors above.")
        print(f"{'='*60}")
        sys.exit(1)
