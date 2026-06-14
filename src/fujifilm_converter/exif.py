"""
EXIF patching using exiftool.

The key function update_exif() is now generic — it accepts either a preset
name or explicit make/model/uniquecameramodel. It also defaults to
-overwrite_original so we don't leave a second "archived/" directory full
of near-duplicate DNGs.
"""

from __future__ import annotations

import os
from typing import Iterable, Optional

from .converters import find_executable, run_command
from .archiving import archive_exif_backup
from .cameras import get_camera, format_camera_info


def update_exif(
    paths: list[str],
    preset: Optional[str] = None,
    make: Optional[str] = None,
    model: Optional[str] = None,
    uniquecameramodel: Optional[str] = None,
    keep_exif_backup: bool = False,
) -> None:
    """
    Patch Make / Model / UniqueCameraModel on the given files.

    If keep_exif_backup=True, the old exiftool *_original files will be
    moved into an archive directory (see archiving.py). By default we pass
    -overwrite_original and never create those files → only one archive dir.
    """
    cam = get_camera(preset=preset, make=make, model=model, uniquecameramodel=uniquecameramodel)

    exiftool = find_executable("exiftool")
    if not exiftool:
        raise RuntimeError("exiftool not found. Install it from https://exiftool.org/")

    print(f"[EXIF] Using camera: {format_camera_info(cam)}")

    command: list[str] = [
        exiftool,
        "-m",
        f'-make={cam["make"]}',
        f'-model={cam["model"]}',
        f'-uniquecameramodel={cam["camera"]}',
    ]

    if not keep_exif_backup:
        command.append("-overwrite_original")

    command.extend(paths)

    run_command(command, "EXIF conversion")

    if keep_exif_backup:
        # Old behavior for people who really want the pre-patch DNGs saved
        dirs = {os.path.dirname(os.path.abspath(p)) for p in paths}
        for d in dirs:
            archive_exif_backup(d, "dng", archive_dir_name="originals")
