# toTemplate

A collection of tools to convert various assets (fonts, images) into C source code using Jinja2 templates. This is particularly useful for embedded systems where you want to embed assets directly into your firmware.

## Sub-projects

### 1. [ttfToTemplate](ttfToTemplate/)
Convert TrueType Fonts (TTF) or OpenType Fonts (OTF) into C bitmap fonts.
- Supports any font size.
- Flexible output via Jinja2 templates.
- Generates 1-bit packed bitmaps.
- Optional PNG preview generation.

### 2. [pngToTemplate](./pngToTemplate/)
Convert PNG images into C bitmap arrays.
- Generates 1-bit packed bitmaps from grayscale/thresholded images.
- Flexible output via Jinja2 templates.
- Supports individual files or entire directories.

## Requirements
Most tools require:
- Python 3
- `jinja2`
- `numpy`
- `pillow`
- `freetype-py` (for fonts)

Install requirements for all tools:
```sh
pip install -r ttfToTemplate/requirements.txt -r pngToTemplate/requirements.txt
```

## Usage
Each sub-project has its own `README.md` with specific usage instructions.
