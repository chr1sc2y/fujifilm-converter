"""
fujifilm-converter

Patch EXIF on any camera's RAW/DNG files so Lightroom sees them as coming
from a Fujifilm profile-ready camera identity.

Public API (for scripting):
    from fujifilm_converter.core import process_inputs, process_file
    from fujifilm_converter.cameras import list_presets, get_camera
"""

__version__ = "0.4.0"

from .cameras import list_presets, get_camera
from .core import process_file, process_inputs, print_status
from .cli import main as cli_main

__all__ = [
    "list_presets",
    "get_camera",
    "process_file",
    "process_inputs",
    "print_status",
    "cli_main",
]
