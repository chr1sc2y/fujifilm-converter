"""
Archiving logic.

Goal (after user feedback): by default produce only **one** clean directory
for original files instead of the confusing "archive/" + "archived/" pair.

Default behavior:
- Source camera RAW files are moved into "originals/" (configurable).
- When patching EXIF we use exiftool's "-overwrite_original" flag so that
  no *_original backup file is ever created on disk. This eliminates the
  second directory completely in the common case.

Advanced / legacy:
- You can still ask for the old behavior via keep_exif_backup=True (will
  create a second dir for the pre-patch DNGs).
"""

from __future__ import annotations

import os
import shutil

from .converters import ensure_dir


def archive_raw_file(
    raw_path: str,
    archive_dir_name: str = "originals",
) -> str:
    """Move the original camera RAW file into the archive dir (flat)."""
    archive_dir = os.path.join(
        os.path.dirname(os.path.abspath(raw_path)), archive_dir_name
    )
    ensure_dir(archive_dir)
    archive_path = os.path.join(archive_dir, os.path.basename(raw_path))

    if os.path.exists(archive_path):
        raise RuntimeError(f"Archive file already exists: {archive_path}")

    shutil.move(raw_path, archive_path)
    print(f"Archived RAW: {raw_path} -> {archive_path}")
    return archive_path


def archive_exif_backup(
    dir_path: str,
    extension: str,
    archive_dir_name: str = "originals",
) -> None:
    """
    Legacy path: move exiftool's *.ext_original files into an archive dir.

    We keep the function for people who pass keep_exif_backup=True, but the
    recommended default path (see exif.py) uses -overwrite_original and never
    calls this.
    """
    archive_dir = os.path.join(dir_path, archive_dir_name)
    ensure_dir(archive_dir)

    for filename in os.listdir(dir_path):
        if filename.endswith(f".{extension}_original"):
            original_path = os.path.join(dir_path, filename)
            archive_file = filename.replace(f".{extension}_original", f".{extension}")
            archive_path = os.path.join(archive_dir, archive_file)
            shutil.move(original_path, archive_path)
            print(f"Archived EXIF backup: {original_path} -> {archive_path}")
