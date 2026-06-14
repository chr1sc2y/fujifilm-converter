# Fujifilm Converter

This program patches EXIF metadata on RAW/DNG files so that Lightroom (and other software) believes they were shot on a different camera.

Classic use: unlock Fujifilm film simulations with any sensor.
It also works for Hasselblad (哈苏), Leica, or completely custom makes/models.

## Comparision

### Example 1

- Sony PT Creative Style

![5](./resources/DSC08427-sony.jpg)

- Fujifilm NC Film Simulation

![6](./resources/DSC08427-fuji.jpg)

### Example 2

- Sony style (before)

![new-sony](./resources/DSC08784-sony.jpg)

- Fujifilm style (after)

![new-fuji](./resources/DSC08784-fuji.jpg)

## One Command to Run the Full Pipeline (for Humans)

After the **one-time** setup of system dependencies (`exiftool` + a RAW→DNG tool) and installing this package, the **entire workflow** — RAW to DNG conversion (if needed), EXIF patching for the target camera, and safe archiving of your originals — is accomplished with **a single command**:

```sh
fuji-convert ./your-photos-folder/
fuji-convert --preset hasselblad /path/to/some/raws
fuji-convert --preset fujifilm ./photos/
```

This is the recommended daily method for humans.

**True zero-permanent-install one-liner** (perfect for occasional use):

```sh
pipx run --spec "git+https://github.com/zintrulcre/fujifilm-converter.git" fuji-convert --preset fuji ./photos/
```

(You will still need `exiftool` and either `dnglab` or Adobe DNG Converter installed on the host machine once.)

After running, the patched `.dng` files stay in place (ready for Lightroom), and your original files are moved into a single clean `originals/` folder.

## Using as a Grok Skill (for Agents / AI)

This tool is also packaged as an official Grok skill so that Agents can directly understand the intent and execute the full conversion workflow.

**Skill location (project-scoped):**  
`.grok/skills/fuji-convert/SKILL.md`

The skill definition is written in **English by default** (this is the reference version). It contains precise, actionable instructions that tell an Agent:

- When to trigger (user says "make it Fuji", "convert to Hasselblad", "fujify these", "unlock film simulations for this folder", etc.).
- How to pick the right `--preset` (with rich alias support: `fuji`, `fujifilm`, `hasselblad`, `hassel`, `hassy`, `hass`, `哈苏`, etc.).
- How to run the **one-command full pipeline** using the native `fuji-convert` binary (or fall back to the Docker path).
- How to handle first-time setup for the user.
- What to report back (location of new DNGs + archived originals).

**For Agents**: When a user provides photo paths and wants camera emulation / film simulation profiles, prefer loading and following the `fuji-convert` skill. The skill tells you the exact terminal commands to invoke and the expected behavior.

This way both humans (simple CLI) and Agents (structured skill with direct execution guidance) are fully supported.

## Quick Start (Truly Hands-Free) — Docker Path

**Docker (strongly recommended when you want zero host dependencies)**

```sh
# Command 1: Build the image once (exiftool + dnglab + converter all bundled)
docker build -t fujifilm-converter .

# Command 2: Process your photos (this is all you need every day)
docker run --rm -v "$(pwd)":/data -w /data fujifilm-converter ./photos/
```

Output `.dng` files appear in your local folder, ready for Lightroom.

**Archiving (greatly improved — only one directory by default)**:
- Source camera RAW files are moved into `originals/` (configurable via `--archive-dir`).
- exiftool is invoked with `-overwrite_original` by default, so no extra "archived/" directory full of near-duplicate files is created. This fixes the previous confusing "two Archive directories" situation.

More examples:
```sh
docker run --rm -v "$(pwd)":/data -w /data fujifilm-converter DSC08427.ARW

# Hasselblad or other presets
docker run --rm -v "$(pwd)":/data -w /data fujifilm-converter --preset hasselblad ./photos/
docker run --rm -v "$(pwd)":/data -w /data fujifilm-converter --preset sony ./photos/

# Fully custom for any manufacturer
docker run --rm -v "$(pwd)":/data -w /data fujifilm-converter \
  --make HASSELBLAD \
  --model "X2D 100C" \
  --uniquecameramodel "Hasselblad X2D 100C" \
  ./photos/

docker run --rm -v "$(pwd)":/data -w /data fujifilm-converter --list-presets
docker run --rm -v "$(pwd)":/data -w /data fujifilm-converter --check
```

**Native install (macOS/Linux — one-time setup, then single command forever)**

1. Install the required system tools with your package manager:
   - macOS:
     ```sh
     brew install exiftool dnglab
     ```
   - Ubuntu/Debian:
     ```sh
     sudo apt update && sudo apt install -y exiftool
     curl -fsSL -o /tmp/dnglab https://github.com/dnglab/dnglab/releases/latest/download/dnglab_linux_x64 && \
       sudo install -m 755 /tmp/dnglab /usr/local/bin/dnglab
     ```

2. Install the tool (gives you the `fuji-convert` and `fujifilm-convert` commands).

**Recommended: Use pipx (cleanest, no venv activation needed)**

```sh
pipx install -e .
```

**Alternative: Use a virtual environment (strongly recommended on macOS)**

```sh
cd /Users/zintrulcre/repo/fujifilm-converter

# Create and activate a venv
python3 -m venv .venv
source .venv/bin/activate

# Upgrade pip first (your system pip is likely too old for modern pyproject.toml editable installs)
python -m pip install --upgrade pip

# Now install in editable mode
pip install -e .
```

**Quick one-liner for old pip on macOS (if you see "editable mode currently requires a setuptools-based build")**

```sh
cd /Users/zintrulcre/repo/fujifilm-converter

# Create a tiny setup.py for legacy pip compatibility
cat > setup.py << 'EOF'
from setuptools import setup
if __name__ == "__main__":
    setup()
EOF

python3 -m pip install --upgrade pip
python3 -m pip install -e . --user
```

After any of the above, you should be able to run:

```sh
fuji-convert --help
fuji-convert --list-presets
```

3. Then just run:

```sh
fuji-convert /path/to/DSC08427.ARW
fuji-convert ./photos/
fuji-convert --preset hasselblad ./photos/
fuji-convert --list-presets
fuji-convert --check

# Fully custom (any brand)
fuji-convert --make HASSELBLAD --model "X2D 100C" --uniquecameramodel "Hasselblad X2D 100C" ./photos/
```

You can still run directly from source without installing:
```sh
python3 process.py ./photos/
```

### One-command automation (local)

(Once system dependencies are installed) The full pipeline is literally one command:

```sh
fuji-convert DSC08427.ARW DSC08428.ARW
fuji-convert ./photos/
fuji-convert --preset hasselblad ./photos/
fuji-convert --skip-convert ./photos/
```

After processing:
- Modified `.dng` files remain in the same directory
- Original RAW files (if any) are moved to `originals/` (single clean archive directory by default)

### Manual workflow (legacy, deprecated)

Early versions required manual steps: use Adobe DNG Converter to turn RAW into DNG, run `python3 main.py` (or fuji.py) to patch EXIF via exiftool, then import to Lightroom.

Full numbered steps + screenshots have been removed for conciseness (see git history or old resources/ images if needed). Use the one-command `fuji-convert` instead.
