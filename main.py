import os

make = "FUJIFILM"
model = "GFX100S"
camera = "Fujifilm GFX 100S"
command = f'exiftool -make="{make}" -model="{model}" -uniquecameramodel="{camera}" '

if __name__ == "__main__":
    file = input("Please input the file: ")
    command += file
    print(command)
    os.system(command)
