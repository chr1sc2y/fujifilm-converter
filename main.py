#!/usr/bin/env python3
"""
Thin compatibility shim for old "python3 main.py" usage.
"""

import sys

from fujifilm_converter.cli import main as cli_main

if __name__ == "__main__":
    raise SystemExit(cli_main())