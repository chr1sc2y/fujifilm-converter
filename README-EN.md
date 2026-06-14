# Fujifilm Converter

This program converts RAW photos from any camera to Fujifilm style by modifying the EXIF information, allowing Lightroom to select Fujifilm film simulations.

## Usage

1. Install ExifTool

```sh
brew install exiftool
```

2. Install this tool

```sh
pip install -e .
```

Or

```sh
pipx install -e .
```

3. Run directly

```sh
fuji-convert ~/Downloads/temp/ # the directory including your raw files
```

After processing, the .dng files with updated EXIF will be generated in the same directory. Drag them directly into Lightroom to select Fujifilm film simulation presets. The original RAW files will be moved to the originals/ directory in the same folder.

You can also directly pass the repository link to the agent to have it execute.

### Docker method

```sh
docker build -t fujifilm-converter .
docker run --rm -v "$(pwd)":/data -w /data fujifilm-converter ./photos/
```

## Effect Comparison

- Sony PT Creative Style

![5](./resources/DSC08427-sony.jpg)

- Fujifilm NC Film Simulation

![6](./resources/DSC08427-fuji.jpg)

- Sony PT Creative Style

![new-sony](./resources/DSC08784-sony.jpg)

- Fujifilm NC Film Simulation

![new-fuji](./resources/DSC08784-fuji.jpg)
