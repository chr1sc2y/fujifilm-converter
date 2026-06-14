"""
Legacy jpg patcher for DJI (interactive).

Modern recommendation: use fuji-convert. Kept for backward compatibility only.
"""

import os
from fujifilm_converter.exif import update_exif


def main():
    dir_path = input("Please input the dir: ")
    dir_path = os.path.abspath(dir_path)

    paths = []
    for name in os.listdir(dir_path):
        if name.lower().endswith(".jpg"):
            paths.append(os.path.join(dir_path, name))

    if not paths:
        print(f"No .jpg files found in {dir_path}")
        return 1

    update_exif(paths, preset="dji")
    print(f"Patched {len(paths)} file(s) using DJI preset")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
