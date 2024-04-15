import os

camera_info = {
    "fuji": {
        "make": "FUJIFILM",
        "model": "GFX100II",
        "camera": "Fujifilm GFX 100 II",
    },
    "sony": {"make": "SONY", "model": "ILCE-7CM2", "camera": "SONY ILCE-7CM2"},
}


def archive_originals(dir, extension):
    archive_dir = dir + "/archived/"
    if not os.path.exists(archive_dir):
        os.makedirs(archive_dir)
    for filename in os.listdir(dir):
        if filename.endswith(f".{extension}_original"):
            original_path = os.path.join(dir, filename)
            archive_file = filename.replace(f".{extension}_original", f".{extension}")
            archive_path = os.path.join(archive_dir, archive_file)
            os.rename(original_path, archive_path)
            print(f"Renamed: {original_path} -> {archive_path}")


def convert(dir, camera_preset, extension):
    make = camera_info[camera_preset]["make"]
    model = camera_info[camera_preset]["model"]
    camera = camera_info[camera_preset]["camera"]
    command = f'exiftool -make="{make}" -model="{model}" -uniquecameramodel="{camera}" '
    command += dir
    print(command)
    os.system(command)
    archive_originals(dir, extension)
