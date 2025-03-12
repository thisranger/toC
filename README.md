# toC

## Convert TTF to C Source Code
This project provides a Python script to convert a TrueType Font (TTF) into a C source file containing bitmap font data. The generated C file includes glyph metadata, a bitmap array, and a global font structure for easy integration.
\
\
See example folder for an implementation and the output.

### Features
✅ Converts TTF to a packed bitmap format (1 bit per pixel).  
✅ Generates a `.c` file with font data and glyph metadata.  
✅ Produces a PNG preview of the rendered font.  
✅ Supports adjustable font sizes.  

## Usage
### Command:
```sh
python ttfToC.py <font.ttf> <output.c> <preview.png> <global_variable_name> <size>
```

### Example:
```sh
python ttfToC.py Minecraft.ttf output.c preview.png FNT16 16
```

### Output:
- `output.c`: Contains the font bitmap array and glyph metadata.
- `preview.png`: A visual preview of the font.
- `FNT16_data`: The global font structure for accessing font information.

## C Structure Overview
The generated C file contains:
```c
static const uint8_t fontBitmap[] = { /* Packed 1-bit bitmap data */ };

static const glyph_t fontGlyphs[] = {
    {width, height, padding, x_offset, y_offset, &fontBitmap[offset]},
    // More glyphs...
};

const font_t FNT16_data = {size, first_char, last_char, fontGlyphs};
```

## Requirements
- Python 3
- `freetype-py` (`pip install freetype-py`)
- `pillow` (`pip install pillow`)
- `numpy` (`pip install numpy`)

## Contributing
Feel free to submit issues or contribute improvements!
