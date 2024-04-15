import os


def convert(dir):
    make = "FUJIFILM"
    model = "GFX100II"
    camera = "Fujifilm GFX 100 II"
    command = f'exiftool -make="{make}" -model="{model}" -uniquecameramodel="{camera}" '
    command += dir
    print(command)
    os.system(command)


def archive_originals(dir):
    archive_dir = dir + "/archived/"
    if not os.path.exists(archive_dir):
        os.makedirs(archive_dir)
    for filename in os.listdir(dir):
        if filename.endswith(".dng_original"):
            original_path = os.path.join(dir, filename)
            archive_file = filename.replace(".dng_original", ".dng")
            archive_path = os.path.join(archive_dir, archive_file)
            os.rename(original_path, archive_path)
            print(f"Renamed: {original_path} -> {archive_path}")


if __name__ == "__main__":
    dir = input("Please input the dir: ")
    convert(dir)
    archive_originals(dir)
