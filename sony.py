"""
Legacy jpg patcher for Sony creative styles (interactive).

Modern recommendation: use fuji-convert with appropriate preset or custom flags
on DNGs. Kept only for backward compatibility.
"""

from fujifilm_converter.exif import update_exif
from fujifilm_converter.converters import ensure_dir
import os


def main():
    dir_path = input("Please input the dir: ")
    dir_path = os.path.abspath(dir_path)

    # Collect jpgs the old way
    paths = []
    for name in os.listdir(dir_path):
        if name.lower().endswith(".jpg"):
            paths.append(os.path.join(dir_path, name))

    if not paths:
        print(f"No .jpg files found in {dir_path}")
        return 1

    # Use the new generic updater (sony preset)
    update_exif(paths, preset="sony")
    print(f"Patched {len(paths)} file(s) using Sony preset")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
