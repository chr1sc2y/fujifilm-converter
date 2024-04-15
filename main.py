import os


def convert(dir):
    make = "FUJIFILM"
    model = "GFX100S"
    camera = "Fujifilm GFX 100S"
    command = f'exiftool -make="{make}" -model="{model}" -uniquecameramodel="{camera}" '
    command += dir
    print(command)
    os.system(command)


def rename_all_files(dir):
    output_dir = dir + "/exported_dng/"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    for filename in os.listdir(dir):
        if filename.endswith(".dng_original"):
            original_path = os.path.join(dir, filename)
            output_filename = filename.replace(".dng_original", ".dng")
            output_path = os.path.join(output_dir, output_filename)
            os.rename(original_path, output_path)
            print(f"Renamed: {original_path} -> {output_path}")

if __name__ == "__main__":
    dir = input("Please input the dir: ")
    convert(dir)
    rename_all_files(dir)
