# tinyfy-skill

A Claude Code skill that wraps the [TinyPNG API](https://tinypng.com/developers) to compress and resize images from the command line.

## What it does

The `tinyfy` skill lets Claude compress or resize images on your behalf. When you ask Claude to compress, optimize, or resize an image, it uses this skill to invoke the TinyPNG API automatically.

## Project structure

```
skills/
└── tinyfy/
    ├── SKILL.md          # Skill definition (triggers + instructions for Claude)
    ├── cli.py            # Python CLI wrapping the TinyPNG API
    ├── requirements.txt  # Python dependencies
    ├── .env.example      # API key template
    └── .env              # Your API key (git-ignored)
```

## Setup

**1. Install dependencies:**

```bash
pip install -r skills/tinyfy/requirements.txt
```

**2. Set your TinyPNG API key:**

```bash
cp skills/tinyfy/.env.example skills/tinyfy/.env
# Edit .env and fill in your TINIFY_API_KEY
```

Get a free API key at [tinypng.com/developers](https://tinypng.com/developers) (500 compressions/month free).

## Usage

Once installed in a Claude Code project, just ask Claude naturally:

- "Compress `photo.png`"
- "Resize `banner.jpg` to 800px wide"
- "Resize the long side of `image.png` to 1200px"

Claude will invoke the CLI and report before/after file sizes with the percentage saved.

### Direct CLI usage

You can also call the CLI directly:

**Compress:**
```bash
python skills/tinyfy/cli.py compress <input> [-o <output>]
```

**Resize by width or height (preserves aspect ratio):**
```bash
python skills/tinyfy/cli.py resize <input> --width <px> [-o <output>]
python skills/tinyfy/cli.py resize <input> --height <px> [-o <output>]
```

**Pass API key inline:**
```bash
python skills/tinyfy/cli.py --api-key <KEY> compress photo.png
```

### Output defaults

| Command    | Default output filename      |
|------------|------------------------------|
| `compress` | `<name>_optimized.<ext>`     |
| `resize`   | `<name>_resized.<ext>`       |

## Dependencies

| Package        | Purpose                                      |
|----------------|----------------------------------------------|
| `tinify`       | TinyPNG API client                           |
| `python-dotenv`| Loads `TINIFY_API_KEY` from `.env`           |
| `Pillow`       | Reads image dimensions for long-side resize  |
| `pytest`       | Test runner                                  |

## License

Apache 2.0 — see [LICENSE](LICENSE).
