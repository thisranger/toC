# ttfToC

## Convert TTF to C Source Code
This project provides a Python script to convert TrueType Fonts (TTF) into C source files using Jinja2 templates. The generated C file typically includes glyph metadata, a bitmap array, and a global font structure for easy integration.

### Features
Converts TTF to a packed bitmap format (1 bit per pixel).  
Uses Jinja2 templates for flexible output formatting.
Generates C files with font data and glyph metadata.  
Produces PNG previews of the rendered fonts.  
Supports adjustable font sizes.  

## Usage
### Command:
```sh
python ttfToTemplate.py <template_file> <output_file> <font_size> [--preview] <font_files_or_directories...>
```

### Parameters:
- `<template_file>`: Path to the Jinja2 template file (e.g., `example/fonts.c.j2`).
- `<output_file>`: Path where the generated code will be saved (e.g., `example/fonts.c`).
- `<font_size>`: Pixel size of the font.
- `--preview`: (Optional) Generate a PNG preview for each font in the `previews/` directory.
- `<font_files_or_directories...>`: One or more paths to TTF/OTF files or directories containing them.

### Example:
```sh
python ttfToTemplate.py example/fonts.c.j2 example/fonts.c 16 --preview fonts/
```

See [example/](./example/) for a complete setup with templates.

## Template Variables
The following variables are available in the Jinja2 template:
- `bitmap`: A list of hex strings (e.g., `["0x00", "0xFF", ...]`) representing the packed 1-bit bitmap data.
- `fonts`: A list of font objects, each containing:
    - `name`: The base name of the font file.
    - `glyphs`: A list of glyph objects:
        - `width`, `height`, `padding`, `x_offset`, `y_offset`, `buffer` (byte offset in the bitmap).
- `first_char`: The ASCII value of the first character (usually 32).
- `last_char`: The ASCII value of the last character (usually 126).
- `font_size`: The requested font size.

## C Structures
The templates define the following structures:
```c
typedef struct {
    uint8_t width, height, padding;
    int8_t xOffset, yOffset;
    const uint8_t* buffer;
} glyph_t;

typedef struct {
    uint8_t size;
    uint8_t firstChar, lastChar;
    glyph_t* glyphs;
} font_t;
```

## Example Usage
See [example/README.md](./example/README.md) for detailed usage and helper functions for rendering.

## Requirements
- Python 3
- [requirements.txt](./requirements.txt)

Install requirements:
```sh
pip install -r requirements.txt
```

## Contributing
Feel free to submit issues or contribute improvements!
