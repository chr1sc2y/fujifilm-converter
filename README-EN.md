# Fujifilm Converter

This program can convert RAW photos from any camera into Fujifilm style by modifying the EXIF information, allowing Lightroom to select Fujifilm film simulations.

## Usage

### One-key automation (recommended)

1. Install dependencies
  - [ExifTool](https://exiftool.org/) (required)
  - One of the following (required when processing RAW files):
    - [Adobe DNG Converter](https://helpx.adobe.com/camera-raw/using/adobe-dng-converter.html)
    - [dnglab](https://github.com/dnglab/dnglab) (open source command line tool)

2. Install this tool
```sh
pipx install -e .
```
or
```sh
pip install -e .
```

3. Pass RAW or DNG files directly, one command completes the full process (RAW → DNG → modify EXIF → archive original files)

```sh
# Single ARW
fuji-convert /path/to/DSC08784.ARW

# Multiple or entire directory
fuji-convert DSC08784.ARW DSC08785.ARW
fuji-convert ./photos/

# Check if dependencies are ready
fuji-convert --check
```

After processing:
- Modified `.dng` files in the same directory (can be directly imported into Lightroom)
- Original RAW files moved to the `originals/` folder in the same directory

If the input is already DNG, you can skip the RAW conversion step:
```sh
fuji-convert --skip-convert ./photos/
```

### Manual step-by-step (legacy)

1. Download and install the following tools
  - [Adobe DNG Converter](https://helpx.adobe.com/camera-raw/using/adobe-dng-converter.html): used to convert raw files taken by the camera to dng files
  - [ExifTool by Phil Harvey](https://exiftool.org/): used to convert dng files to files containing Fujifilm camera exif information

2. Open Adobe DNG Converter, select the directory where your raw files are located, click convert to start conversion

![1](./resources/1.png)

After completion you will see the following interface

![2](./resources/2.png)

3. Run `python3 fuji.py` in the terminal, then enter the directory of the converted dng files, the output is as follows

```sh
➜  python3 fuji.py
Please input the dir: ./test
exiftool -make="FUJIFILM" -model="GFX100II" -uniquecameramodel="Fujifilm GFX 100 II" ./test
    1 directories scanned
   32 image files updated
```

In the directory you will get some new dng files, the original files are placed in the originals directory

![3](./resources/3.png)

4. Drag these new files into lightroom, you can select all 20 Fujifilm film simulations

![4](./resources/4.png)

## Quick Start

**Docker (zero dependencies)**

```sh
# Build once
docker build -t fujifilm-converter .

# Run
docker run --rm -v "$(pwd)":/data -w /data fujifilm-converter ./photos/
```

**Local**

After installation, run directly
```sh
fuji-convert ./photos/
```

Supports presets (default fuji):
```sh
fuji-convert --preset hasselblad ./photos/
fuji-convert --preset leica ./photos/
```

When using an agent, simply pass the link to this repository to the agent and it can perform the conversion.

## Effect Comparison

- Sony PT Creative Style

![5](./resources/DSC08427-sony.jpg)

- Fujifilm NC Film Simulation

![6](./resources/DSC08427-fuji.jpg)
