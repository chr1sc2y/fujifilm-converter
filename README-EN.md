# Fujifilm Converter

[简体中文](./README.md)

Patch RAW/DNG photos so Lightroom recognizes them as a Fujifilm camera and exposes Fujifilm film simulations.

The tool converts RAW files to DNG, then writes the camera identity into the DNG metadata. It does not recreate an in-camera Fujifilm JPEG; it only unlocks the matching Lightroom profile choices when those profiles are available.

## Three Ways To Use It

### 1. Local CLI

Use this if you already have Python installed and want to run the tool locally.

```sh
brew install exiftool
python3 -m pip install -e .
fuji-convert ./photos/  # ./photos/ is the directory containing RAW photos
```

After processing, the updated `.dng` files are created next to the source photos. Import those DNG files into Lightroom and choose a Fujifilm film simulation. Original RAW files are moved into `originals/` by default.

To keep original RAW files in place:

```sh
fuji-convert --no-archive-raw ./photos/  # ./photos/ is the directory containing RAW photos
```

### 2. Docker

Use this if you do not want to install Python dependencies on the host. The image includes ExifTool and dnglab.

```sh
docker build -t fujifilm-converter .
docker run --rm -v "$PWD":/data -w /data fujifilm-converter ./photos/  # ./photos/ is the directory containing RAW photos
```

### 3. Agent Skill

If you only need Fujifilm film simulations and want a workflow that never moves, overwrites, or edits source files, use the dedicated Skill repository:

[fujifilm-film-sim-skill](https://github.com/chr1sc2y/fujifilm-film-sim-skill)

```sh
npx skills@latest add chr1sc2y/fujifilm-film-sim-skill
```

Then ask your agent:

```text
Use $unlock-fujifilm-film-simulations on /Users/me/Pictures/trip.
```

The Skill writes results to `fujifilm-ready/` and creates `report.json` plus `REPORT.md`. The difference is simple: the Skill is copy-first and leaves originals untouched; this CLI moves original RAW files into `originals/` by default.

## Common Commands

```sh
fuji-convert --check
fuji-convert --list-presets
fuji-convert ./photos/  # ./photos/ is the directory containing RAW photos
```

The main workflow is Fujifilm film simulations. Do not assume EXIF changes can unlock every other brand's profiles; some brands have extra Lightroom-side checks.

## Comparison

| Original rendering | Fujifilm NC film simulation |
| --- | --- |
| ![Sony PT Creative Style](./resources/DSC08427-sony.jpg) | ![Fujifilm NC Film Simulation](./resources/DSC08427-fuji.jpg) |
| ![Sony PT Creative Style](./resources/DSC08784-sony.jpg) | ![Fujifilm NC Film Simulation](./resources/DSC08784-fuji.jpg) |

## Requirements

- Python 3.8+
- [ExifTool](https://exiftool.org/)
- Adobe DNG Converter or [dnglab](https://github.com/dnglab/dnglab) for RAW-to-DNG conversion
- Lightroom / Camera Raw with the relevant Fujifilm Camera Matching profiles installed

## Notes

This is an independent project and is not affiliated with Fujifilm, Adobe, or Lightroom. Available profiles depend on your Lightroom / Camera Raw version.
