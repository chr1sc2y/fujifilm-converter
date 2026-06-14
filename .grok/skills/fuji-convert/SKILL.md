---
name: fuji-convert
description: >
  Convert any camera's RAW or DNG photos to Fujifilm, Hasselblad, Leica or other styles 
  by patching EXIF so Lightroom can use the target camera's profiles and film simulations.
  The full pipeline (RAW→DNG conversion if needed + EXIF patch + archiving originals) 
  is done with a single command: fuji-convert <path>. 
  Use when user provides photo folders/files and wants to "make it Fuji", "convert to Hasselblad", 
  "fujifilm style", "hassel", "unlock film simulations", etc. 
  Supports simple preset names like fuji, fujifilm, hasselblad, hassel, hassy, leica.
  Default behavior uses fixed clean configurations for best Lightroom compatibility.
---

# fuji-convert Skill

This skill lets you (the Agent) run the complete Fujifilm Converter workflow for the user with minimal friction.

## Core Principle for Agents
The **entire end-to-end process** for a human or for you is **one single command** after initial setup:

```bash
fuji-convert <path-to-photos-or-folder>
```

Examples the user might say:
- "convert these to Fuji"
- "make it Hasselblad style"
- "run fuji on /Users/me/photos"
- "unlock film simulations for this folder"

## How to Execute (Agent Workflow)

1. **Detect the target preset** from user intent:
   - Default: `fuji` (Fujifilm GFX100II)
   - If user mentions Hasselblad / 哈苏 / hassel / hassy / hass → `--preset hasselblad`
   - If user mentions Leica → `--preset leica`
   - If user mentions Sony creative style → `--preset sony`
   - If user mentions DJI → `--preset dji`
   - Fuzzy names are supported (fujifilm, fuji film, hassel etc.)

2. **Run the one-command full pipeline** (preferred):
   Use the terminal tool to execute:

   ```bash
   fuji-convert --preset <chosen> <user-provided-path>
   ```

   - The command automatically:
     - Converts RAW → DNG (using Adobe DNG Converter or dnglab if present)
     - Patches EXIF to the chosen camera (Make / Model / UniqueCameraModel)
     - Moves original RAW files into an `originals/` folder next to the photos
     - Uses `-overwrite_original` so no extra messy backup directories are created
   - Output: the patched .dng files are left in the original location, ready to drag into Lightroom.

3. **If `fuji-convert` command is not found** (first time in this environment):
   - Recommend the cleanest one-liner for humans (using pipx for temporary execution):
     ```bash
     pipx run --spec "git+https://github.com/zintrulcre/fujifilm-converter.git" fuji-convert --preset <chosen> <path>
     ```
   - Or permanent install (recommended for repeated use):
     ```bash
     pip install -e "git+https://github.com/zintrulcre/fujifilm-converter.git"
     fuji-convert --preset <chosen> <path>
     ```
   - Note to user: they still need the system tools once:
     - macOS: `brew install exiftool dnglab`
     - Linux: exiftool + dnglab binary

4. **Docker alternative** (when user wants zero host dependencies):
   - One-time: `docker build -t fuji-converter .`
   - Every time (the actual one command):
     ```bash
     docker run --rm -v "$(pwd)":/data -w /data fuji-converter --preset <chosen> <path-relative-to-pwd>
     ```

5. **After running**:
   - Show the user the resulting .dng file(s).
   - Tell them the originals were archived to `originals/`.
   - Instruct them to import the new .dng files into Lightroom — they should now see the target camera's film simulations / profiles (Fujifilm NC, Astia, Eterna, Hasselblad profiles, etc.).

## Important Flags Agents Can Use
- `--preset fuji` (or hasselblad, leica, etc.)
- `--list-presets` — useful to show user what is available
- `--skip-convert` — when input is already DNG
- `--no-archive-raw` — leave the original RAW files in place
- `--check` — verify exiftool + RAW converter are present

## Example Agent Responses
When user says "convert /Users/zintrulcre/Downloads/temp to Fuji":

You should run:
```
fuji-convert --preset fuji /Users/zintrulcre/Downloads/temp
```

When user says "make these Hasselblad":

You should run:
```
fuji-convert --preset hasselblad /path/to/folder
```

Always prefer the native `fuji-convert` command when available because it is the true "one command completes the whole flow".

## Notes for Reliability
- The tool is intentionally designed so that after the one-time dependency install, the daily/Agent usage is literally one command.
- It supports both RAW files and already-converted DNGs.
- The EXIF values are deliberately fixed per preset (no user-supplied model/lens details) to guarantee Lightroom recognizes them cleanly.
- Both `fuji-convert` and the fuller `fujifilm-convert` command names work.

Use this skill whenever the user wants to "fujify", "hasselblad-ify", unlock film simulations, or emulate another camera via EXIF on their photo files.
