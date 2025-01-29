from common import convert


camera_preset = "dji"
extension = "jpg"

if __name__ == "__main__":
    dir = input("Please input the dir: ")
    convert(dir, camera_preset, extension)
