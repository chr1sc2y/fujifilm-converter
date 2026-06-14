"""
RAW / DNG converter discovery and execution.

Handles finding Adobe DNG Converter or dnglab, and performing the
RAW → DNG conversion step. Kept completely separate from EXIF and archiving.
"""

from __future__ import annotations

import json
import os
import platform
import shutil
import subprocess
import urllib.request
import zipfile
from typing import Tuple, Optional

RAW_EXTENSIONS = {
    "arw", "cr2", "cr3", "nef", "nrw", "raf", "orf", "rw2", "pef", "srw",
    "dng", "raw", "rwl", "3fr", "iiq", "mef", "mrw", "erf", "kdc", "dcr", "gpr",
}

ADOBE_DNG_CONVERTER_PATHS = {
    "Darwin": "/Applications/Adobe DNG Converter.app/Contents/MacOS/Adobe DNG Converter",
    "Windows": r"C:\Program Files\Adobe\Adobe DNG Converter\Adobe DNG Converter.exe",
}


def file_extension(path: str) -> str:
    return os.path.splitext(path)[1].lstrip(".").lower()


def is_raw_file(path: str) -> bool:
    return file_extension(path) in RAW_EXTENSIONS


def is_dng_file(path: str) -> bool:
    return file_extension(path) == "dng"


def find_executable(name: str) -> Optional[str]:
    return shutil.which(name)


def find_adobe_dng_converter() -> Optional[str]:
    custom = os.environ.get("ADOBE_DNG_CONVERTER")
    if custom and os.path.isfile(custom):
        return custom

    system = platform.system()
    default_path = ADOBE_DNG_CONVERTER_PATHS.get(system)
    if default_path and os.path.isfile(default_path):
        return default_path
    return None


def find_dng_converter() -> Tuple[Optional[str], Optional[str]]:
    """Return (converter_type, path) or (None, None)."""
    adobe = find_adobe_dng_converter()
    if adobe:
        return ("adobe", adobe)

    dnglab = find_executable("dnglab")
    if dnglab:
        return ("dnglab", dnglab)

    # Auto-download portable dnglab binary if missing (makes install closer to one-click)
    dnglab = _ensure_dnglab()
    if dnglab:
        return ("dnglab", dnglab)

    return (None, None)


def _ensure_dnglab() -> Optional[str]:
    """Download dnglab binary to user cache if not present. Returns path or None."""
    cache_dir = os.path.expanduser("~/.cache/fujifilm-converter")
    os.makedirs(cache_dir, exist_ok=True)
    bin_path = os.path.join(cache_dir, "dnglab")

    if os.path.isfile(bin_path) and os.access(bin_path, os.X_OK):
        return bin_path

    system = platform.system()
    machine = platform.machine().lower()

    if system == "Darwin":
        asset = "dnglab-macos-arm64"
        download_name = "dnglab_download.zip"
        is_zip = True
    elif system == "Linux":
        if "aarch" in machine or "arm" in machine:
            asset = "dnglab_linux_aarch64"
        else:
            asset = "dnglab_linux_x64"
        download_name = "dnglab_download"
        is_zip = False
    else:
        return None

    print("dnglab not found, downloading portable binary...")
    try:
        api_url = "https://api.github.com/repos/dnglab/dnglab/releases/latest"
        with urllib.request.urlopen(api_url, timeout=30) as resp:
            release = json.load(resp)

        download_url = None
        for a in release.get("assets", []):
            if asset in a.get("name", ""):
                download_url = a["browser_download_url"]
                break

        if not download_url:
            print("Could not find matching dnglab asset for this platform.")
            return None

        download_path = os.path.join(cache_dir, download_name)
        urllib.request.urlretrieve(download_url, download_path)

        if is_zip:
            with zipfile.ZipFile(download_path) as zf:
                for member in zf.namelist():
                    if "dnglab" in member.lower() and not member.endswith("/"):
                        zf.extract(member, cache_dir)
                        extracted = os.path.join(cache_dir, member)
                        if os.path.dirname(extracted) != cache_dir:
                            # move to flat
                            final = os.path.join(cache_dir, os.path.basename(member))
                            os.rename(extracted, final)
                            extracted = final
                        os.rename(extracted, bin_path)
                        break
            os.remove(download_path)
        else:
            os.rename(download_path, bin_path)

        os.chmod(bin_path, 0o755)
        print(f"Downloaded dnglab to {bin_path}")
        return bin_path
    except Exception as e:
        print(f"Failed to auto-download dnglab: {e}")
        return None


def ensure_dir(path: str) -> None:
    if not os.path.exists(path):
        os.makedirs(path)


def run_command(command: list[str], label: str) -> subprocess.CompletedProcess:
    """Run a command, print what we are doing, raise on failure."""
    print(f"[{label}] {' '.join(command)}")
    result = subprocess.run(command, check=False)
    if result.returncode != 0:
        raise RuntimeError(f"{label} failed with exit code {result.returncode}")
    return result


def expected_dng_path(raw_path: str) -> str:
    return os.path.splitext(raw_path)[0] + ".dng"


def find_converted_dng(raw_path: str) -> Optional[str]:
    base = os.path.splitext(raw_path)[0]
    for ext in (".dng", ".DNG"):
        candidate = base + ext
        if os.path.isfile(candidate):
            return candidate
    return None


def convert_raw_to_dng(raw_path: str, converter_type: str, converter_path: str) -> str:
    output_dir = os.path.dirname(os.path.abspath(raw_path))
    expected = expected_dng_path(raw_path)

    if converter_type == "adobe":
        run_command(
            [converter_path, "-fl", "-mp", "-d", output_dir, raw_path],
            "RAW to DNG (Adobe DNG Converter)",
        )
    elif converter_type == "dnglab":
        run_command(
            [converter_path, "convert", "-f", raw_path, expected],
            "RAW to DNG (dnglab)",
        )
    else:
        raise RuntimeError("No RAW to DNG converter found")

    dng_path = find_converted_dng(raw_path)
    if not dng_path:
        raise RuntimeError(f"DNG output not found for {raw_path}")
    return dng_path


def print_converter_status() -> None:
    converter_type, converter_path = find_dng_converter()
    exiftool = find_executable("exiftool")
    print(f"exiftool: {'found' if exiftool else 'missing (install from https://exiftool.org/ or brew/apt)'}")
    if converter_path:
        print(f"RAW converter: {converter_type} ({converter_path})")
    else:
        print("RAW converter: missing (will try to auto-download dnglab; or install Adobe DNG Converter)")
