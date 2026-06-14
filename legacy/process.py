#!/usr/bin/env python3
"""
Backward-compatible shim.

People (and old docs) can still run:
    python3 process.py ./photos/

It now delegates to the clean packaged implementation.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Allow running directly from root: python legacy/process.py
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from fujifilm_converter.cli import main as cli_main


def main(argv: list[str] | None = None) -> int:
    # The real CLI lives in fujifilm_converter.cli
    # We just forward everything (including --check, --list-presets, custom camera, etc.)
    return cli_main(argv)


if __name__ == "__main__":
    raise SystemExit(main())