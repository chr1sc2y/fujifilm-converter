"""
Modern CLI entry point.

fuji-convert is now fully generic: it can output any camera EXIF you want
(Fujifilm for film sims, Hasselblad, Leica, Sony, or completely custom).
"""

from __future__ import annotations

import argparse
import importlib.metadata
import sys
from typing import Optional

from .cameras import list_presets, format_camera_info, get_camera
from .core import process_inputs, print_status


def build_parser() -> argparse.ArgumentParser:
    presets = list_presets()

    parser = argparse.ArgumentParser(
        description=(
            "Patch EXIF on RAW/DNG files so Lightroom thinks the photos were taken "
            "with a different camera. This lets you use that camera's profiles and "
            "film simulations (Fujifilm, Hasselblad, etc.) in Lightroom.\n\n"
            "You almost never need to know exact model numbers. "
            "Just say the brand you want."
        ),
        epilog=(
            "Simple usage (recommended):\n"
            "  fuji-convert ./photos/                    # default = Fujifilm\n"
            "  fuji-convert --preset fuji ./photos/\n"
            "  fuji-convert --preset fujifilm ./photos/  # many aliases work\n"
            "  fuji-convert --preset hasselblad ./photos/\n"
            "  fuji-convert --preset hassel ./photos/    # hassel, hassy, hasselblad all work\n"
            "  fuji-convert --list-presets\n\n"
            "Advanced (only if you really need something special):\n"
            "  fuji-convert --make HASSELBLAD --model X2D --uniquecameramodel \"Hasselblad X2D 100C\" ./photos/"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    try:
        version = importlib.metadata.version("fujifilm-converter")
    except importlib.metadata.PackageNotFoundError:
        version = "dev"
    parser.add_argument("--version", action="version", version=f"%(prog)s {version}")

    parser.add_argument(
        "inputs",
        nargs="*",
        help="RAW/DNG file(s) or directory containing them",
    )

    # Preset or fully custom
    parser.add_argument(
        "--preset",
        default="fuji",
        help="What camera to emulate. "
             "You can use simple names: fuji, fujifilm, hasselblad, hassel, hassy, leica, sony, dji. "
             "Many natural aliases are accepted (default: fuji).",
    )
    parser.add_argument(
        "--make",
        help="ADVANCED: directly set EXIF Make (must be used together with --model and --uniquecameramodel). "
             "For normal use just use --preset hasselblad or --preset fuji etc.",
    )
    parser.add_argument(
        "--model",
        help="ADVANCED: directly set EXIF Model",
    )
    parser.add_argument(
        "--uniquecameramodel",
        "--camera",
        dest="uniquecameramodel",
        help="ADVANCED: directly set the Unique Camera Model tag",
    )

    parser.add_argument(
        "--no-archive-raw",
        action="store_true",
        help="Do not move original RAW files into the archive directory",
    )
    parser.add_argument(
        "--archive-dir",
        default="originals",
        help="Directory name for archived original files (default: originals). "
             "Only the true source RAWs go here by default.",
    )
    parser.add_argument(
        "--keep-exif-backup",
        action="store_true",
        help="Keep exiftool's pre-patch *_original files (creates a second directory). "
             "Rarely needed — default behavior is clean single-dir archiving.",
    )
    parser.add_argument(
        "--skip-convert",
        action="store_true",
        help="Skip RAW→DNG conversion (input must already be DNG)",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check required external tools (exiftool, dng converter) and exit",
    )
    parser.add_argument(
        "--list-presets",
        action="store_true",
        help="List all built-in camera presets and exit",
    )

    return parser


def main(argv: Optional[list[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.list_presets:
        print("Available simple presets (just type what feels natural):")
        for p in list_presets():
            cam = get_camera(preset=p)
            print(f"  {p:12s} → {format_camera_info(cam)}")
        print("\nAliases that also work:")
        print("  fuji / fujifilm / fuji film / gfx     → Fujifilm")
        print("  hasselblad / hassel / hassy / hass    → Hasselblad (哈苏)")
        print("  (The resolver is very forgiving on purpose.)")
        return 0

    if args.check:
        print_status()
        return 0

    if not args.inputs:
        parser.error("inputs are required unless --check or --list-presets is used")

    # Resolve camera: custom flags win over preset
    preset = args.preset or "fuji"
    try:
        # Just validate early (core will also resolve)
        get_camera(
            preset=None if (args.make or args.model or args.uniquecameramodel) else preset,
            make=args.make,
            model=args.model,
            uniquecameramodel=args.uniquecameramodel,
        )
    except ValueError as e:
        parser.error(str(e))

    try:
        results = process_inputs(
            args.inputs,
            preset=preset,
            archive_raw=not args.no_archive_raw,
            skip_raw_conversion=args.skip_convert,
            archive_dir=args.archive_dir,
            keep_exif_backup=args.keep_exif_backup,
            make=args.make,
            model=args.model,
            uniquecameramodel=args.uniquecameramodel,
        )
    except (RuntimeError, ValueError, FileNotFoundError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(f"Processed {len(results)} file(s)")
    for path in results:
        print(f"  {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
