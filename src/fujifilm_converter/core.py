"""
High-level processing orchestration.

process_file / process_inputs are the main public API used by the CLI
and by thin legacy wrappers.
"""

from __future__ import annotations

import os
from typing import Optional

from .converters import (
    is_dng_file,
    is_raw_file,
    find_dng_converter,
    convert_raw_to_dng,
    print_converter_status,
)
from .archiving import archive_raw_file
from .exif import update_exif
from .cameras import list_presets


def collect_input_paths(inputs: list[str]) -> list[str]:
    paths: list[str] = []
    for item in inputs:
        item = os.path.abspath(item)
        if os.path.isdir(item):
            for filename in sorted(os.listdir(item)):
                full_path = os.path.join(item, filename)
                if os.path.isfile(full_path) and is_raw_file(full_path):
                    paths.append(full_path)
        elif os.path.isfile(item):
            paths.append(item)
        else:
            raise FileNotFoundError(f"Input not found: {item}")
    return paths


def process_file(
    input_path: str,
    preset: str = "fuji",
    archive_raw: bool = True,
    skip_raw_conversion: bool = False,
    archive_dir: str = "originals",
    keep_exif_backup: bool = False,
    make: Optional[str] = None,
    model: Optional[str] = None,
    uniquecameramodel: Optional[str] = None,
) -> str:
    input_path = os.path.abspath(input_path)
    if not os.path.isfile(input_path):
        raise FileNotFoundError(f"File not found: {input_path}")

    raw_path = None
    dng_path = None

    if is_dng_file(input_path):
        dng_path = input_path
    elif is_raw_file(input_path):
        raw_path = input_path
        if skip_raw_conversion:
            raise ValueError(
                f"{input_path} is a RAW file. Remove --skip-convert or install a DNG converter."
            )
        converter_type, converter_path = find_dng_converter()
        if not converter_path:
            raise RuntimeError(
                "No RAW to DNG converter found. Install Adobe DNG Converter or dnglab."
            )
        dng_path = convert_raw_to_dng(raw_path, converter_type, converter_path)
        if archive_raw:
            archive_raw_file(raw_path, archive_dir_name=archive_dir)
    else:
        raise ValueError(f"Unsupported file type: {input_path}")

    # EXIF update using a preset or explicit advanced camera identity.
    update_exif(
        [dng_path],
        preset=preset,
        make=make,
        model=model,
        uniquecameramodel=uniquecameramodel,
        keep_exif_backup=keep_exif_backup,
    )
    print(f"Done: {dng_path}")
    return dng_path


def process_inputs(
    inputs: list[str],
    preset: str = "fuji",
    archive_raw: bool = True,
    skip_raw_conversion: bool = False,
    archive_dir: str = "originals",
    keep_exif_backup: bool = False,
    make: Optional[str] = None,
    model: Optional[str] = None,
    uniquecameramodel: Optional[str] = None,
) -> list[str]:
    paths = collect_input_paths(inputs)
    if not paths:
        raise RuntimeError("No supported RAW or DNG files found")

    results: list[str] = []
    for path in paths:
        results.append(
            process_file(
                path,
                preset=preset,
                archive_raw=archive_raw,
                skip_raw_conversion=skip_raw_conversion,
                archive_dir=archive_dir,
                keep_exif_backup=keep_exif_backup,
                make=make,
                model=model,
                uniquecameramodel=uniquecameramodel,
            )
        )
    return results


def print_status() -> None:
    """Wrapper so CLI can call without importing converters directly."""
    print_converter_status()
