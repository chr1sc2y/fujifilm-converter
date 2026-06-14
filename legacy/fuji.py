#!/usr/bin/env python3
"""
Legacy interactive wrapper (kept for people who liked the old "python3 fuji.py" prompt).

Modern usage is `fuji-convert` (or python3 process.py).
"""

import sys
from pathlib import Path

# Allow running directly from root
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from fujifilm_converter.core import process_inputs
from fujifilm_converter.cameras import get_camera


def legacy_dir_mode():
    dir_path = input("Please input the dir: ")
    # Old behavior was hardcoded fuji + dng extension scanning
    # We now route through the modern path (it will only pick .dng and .raw files)
    try:
        process_inputs([dir_path], preset="fuji")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    return 0


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    if not argv:
        return legacy_dir_mode()

    try:
        process_inputs(argv, preset="fuji")
    except (RuntimeError, ValueError, FileNotFoundError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())