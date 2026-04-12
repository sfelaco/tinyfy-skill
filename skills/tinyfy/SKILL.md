---
name: tinyfy
description: Use this skill to compress or resize images using the tinyfy CLI tool. Trigger whenever the user asks to compress, optimize, reduce, or resize an image file. Also trigger when the user mentions reducing file size, resizing to a specific width or height, fitting an image within a dimension, or resizing "the long side" of an image. Always use this skill for any image compression or resizing task in this project, even if the user doesn't explicitly mention tinyfy.
---

# tinyfy — Image Compression & Resize CLI

tinyfy wraps the TinyPNG API to compress and resize images from the command line.  
The CLI code lives inside this skill folder.

***IMPORTANT***
Follow the installation step before using the skill.

---

## Installation

Create a dedicated virtual environment and install all dependencies into it:

```bash
python -m venv skills/tinyfy/.venv
skills/tinyfy/.venv/Scripts/pip install -r skills/tinyfy/requirements.txt   # Windows
# skills/tinyfy/.venv/bin/pip install -r skills/tinyfy/requirements.txt    # Unix/macOS
```

`requirements.txt` includes:
- `tinify` — TinyPNG API client
- `python-dotenv` — loads `.env` automatically
- `Pillow` — reads image dimensions (needed for long-side resize)
- `pytest` — test runner

The API key is read from `skills/tinyfy/.env`:

```
TINIFY_API_KEY=<your_key>
```

Alternatively, pass `--api-key <KEY>` to any command.

**Define the venv Python path once** before running any command below:

```bash
TINYFY_PY=skills/tinyfy/.venv/Scripts/python   # Windows
# TINYFY_PY=skills/tinyfy/.venv/bin/python     # Unix/macOS
```

---

## Compress

Compress an image without changing its dimensions:

```bash
$TINYFY_PY skills/tinyfy/cli.py compress <input> [-o <output>]
```

- If `-o` is omitted, the output is saved as `<name>_optimized.<ext>` next to the input file.

**Example:**
```bash
$TINYFY_PY skills/tinyfy/cli.py compress photo.png -o photo_small.png
```

---

## Resize (explicit width or height)

Resize while preserving aspect ratio, then compress. Specify **either** `--width` or `--height`, never both:

```bash
$TINYFY_PY skills/tinyfy/cli.py resize <input> --width <px> [-o <output>]
$TINYFY_PY skills/tinyfy/cli.py resize <input> --height <px> [-o <output>]
```

- If `-o` is omitted, the output is saved as `<name>_resized.<ext>`.

**Examples:**
```bash
$TINYFY_PY skills/tinyfy/cli.py resize photo.png --width 800
$TINYFY_PY skills/tinyfy/cli.py resize photo.png --height 600 -o thumb.png
```

---

## Resize by long side

When the user asks to resize "the long side" to a target size (e.g. "resize the long side to 1200px"), determine which dimension is larger, then pass the right flag to the CLI.

**Step 1 — detect dimensions:**

```bash
$TINYFY_PY -c "
from PIL import Image
img = Image.open('PATH_TO_IMAGE')
w, h = img.size
print(f'width={w} height={h}')
"
```

**Step 2 — pick the flag:**

| Condition | Flag to use |
|---|---|
| `width > height` (landscape) | `--width <target>` |
| `height >= width` (portrait or square) | `--height <target>` |

**Step 3 — call the CLI:**

```bash
# landscape example (width is the long side)
$TINYFY_PY skills/tinyfy/cli.py resize photo.png --width 1200

# portrait example (height is the long side)
$TINYFY_PY skills/tinyfy/cli.py resize photo.png --height 1200
```

---

## Output defaults summary

| Command | Default output name |
|---|---|
| `compress` | `<name>_optimized.<ext>` |
| `resize` | `<name>_resized.<ext>` |

Both commands print before/after file sizes and the percentage saved.
