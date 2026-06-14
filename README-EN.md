# Fujifilm Converter

This program converts RAW photos from any camera to Fujifilm style by modifying EXIF so Lightroom can use the corresponding camera profiles and film simulations.

## Usage

First, install ExifTool:

```sh
brew install exiftool
```

Second, install this tool:

```sh
pip install -e .
```

Or with pipx:

```sh
pipx install -e .
```

Usage:

Run directly (defaults to Fujifilm preset):

```sh
fuji-convert ./photos/
```

Specify other preset:

```sh
fuji-convert --preset hasselblad ./photos/
fuji-convert --preset leica ./photos/
```

Check environment:

```sh
fuji-convert --check
```

Docker usage:

```sh
docker build -t fujifilm-converter .

docker run --rm -v "$(pwd)":/data -w /data fujifilm-converter ./photos/
```

After processing, the modified .dng files (with updated EXIF) are ready to import into Lightroom. Original RAW files are moved to the originals/ folder in the same directory.

When using an agent, simply pass the link to this repository and it can perform the conversion.

## Effect Comparison

- Sony PT Creative Style

![5](./resources/DSC08427-sony.jpg)

- Fujifilm NC Film Simulation

![6](./resources/DSC08427-fuji.jpg)

- Sony PT Creative Style

![new-sony](./resources/DSC08784-sony.jpg)

- Fujifilm NC Film Simulation

![new-fuji](./resources/DSC08784-fuji.jpg)
