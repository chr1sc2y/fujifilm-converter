"""
Camera presets for EXIF spoofing.

This module contains a small number of **fixed configurations** for metadata
patching. The Fujifilm preset is the recommended profile-unlock path.

Users should **not** need to know exact model numbers or lenses.
They just type a simple name like:
    --preset fuji
    --preset fujifilm

The resolver below accepts natural aliases for the supported presets.

Only presets that should be shown as first-class CLI choices live here.
Adding a new one means verifying that Lightroom actually exposes the
intended profile set, not just that EXIF values can be written.
"""

from __future__ import annotations

# Fixed configurations. Keep first-class presets conservative: a preset should
# not be advertised unless the intended Lightroom behavior has been verified.
CAMERAS: dict[str, dict[str, str]] = {
    "fuji": {
        "make": "FUJIFILM",
        "model": "GFX100II",
        "camera": "Fujifilm GFX 100 II",
    },
    "sony": {
        "make": "SONY",
        "model": "ILCE-7CM2",
        "camera": "SONY ILCE-7CM2",
    },
    "dji": {
        "make": "DJI",
        "model": "Mini 4 Pro",
        "camera": "DJI FC8482",
    },
}

# Very forgiving aliases so users can type natural things.
# Key = what user might type (lowercased), Value = canonical key in CAMERAS
ALIAS_TO_PRESET: dict[str, str] = {
    # Fuji / Fujifilm
    "fuji": "fuji",
    "fujifilm": "fuji",
    "fuji film": "fuji",
    "fujifilm film": "fuji",
    "fuj": "fuji",
    "gf": "fuji",
    "gfx": "fuji",
    "fujifilm converter": "fuji",

    # Others
    "sony": "sony",
    "dji": "dji",
}


def list_presets() -> list[str]:
    """Return the canonical preset names users can rely on."""
    return sorted(CAMERAS.keys())


def _normalize_preset(name: str) -> str:
    """Turn 'Fujifilm', 'fuji film', etc. into a canonical key."""
    if not name:
        return "fuji"

    key = name.lower().strip()

    # exact canonical name
    if key in CAMERAS:
        return key

    # known alias
    if key in ALIAS_TO_PRESET:
        return ALIAS_TO_PRESET[key]

    # last resort: try substring match for convenience
    for alias, canon in ALIAS_TO_PRESET.items():
        if alias in key or key in alias:
            return canon

    return key  # will fail later with a nice error


def get_camera(
    preset: str | None = None,
    make: str | None = None,
    model: str | None = None,
    uniquecameramodel: str | None = None,
) -> dict[str, str]:
    """
    Resolve to one of the fixed configurations.

    Normal usage (recommended):
        get_camera("fuji") or get_camera("fujifilm")

    Advanced (power users who really know what they are doing):
        You can still pass explicit make/model/uniquecameramodel.
        But for normal Lightroom profile selection you almost never need this.
    """
    if make or model or uniquecameramodel:
        if not (make and model and uniquecameramodel):
            raise ValueError(
                "For custom values you must provide all three of "
                "--make, --model and --uniquecameramodel together."
            )
        return {
            "make": make,
            "model": model,
            "camera": uniquecameramodel,
        }

    if not preset:
        preset = "fuji"

    canon = _normalize_preset(preset)

    if canon not in CAMERAS:
        available = ", ".join(list_presets())
        raise ValueError(
            f"Unknown preset '{preset}'. "
            f"Try one of: {available} (or aliases like fuji, fujifilm, gfx, etc.)"
        )

    return CAMERAS[canon].copy()


def format_camera_info(cam: dict[str, str]) -> str:
    return f"{cam['make']} / {cam['model']} / {cam['camera']}"
