import os
from common import convert

camera_preset = "fuji"
extension = "dng"

if __name__ == "__main__":
    dir = input("Please input the dir: ")
    convert(dir, camera_preset, extension)
