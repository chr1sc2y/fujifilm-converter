import os
from common import convert

camera_name = "A7C2"
extension = "jpg"

if __name__ == "__main__":
    dir = input("Please input the dir: ")
    convert(dir, camera_name, extension)
