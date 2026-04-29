# ttfToC

## Convert TTF to C Source Code
This project provides a Python script to convert TrueType Fonts (TTF) into C source files using Jinja2 templates. The generated file typically includes glyph metadata, a bitmap array, and a global font structure for easy integration.

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

## Example Usage
The following code demonstrates how to use the generated data to draw an image.

```c
glyph_t GetChar(font_t* font, char letter)
{
    if ( letter >= font->firstChar && letter <= font->lastChar){
        return font->glyphs[letter - font->firstChar];
    } else {
        printf("Char not available\n");
        return font->glyphs[0];
    }
}

textDimensions_t SizeString(font_t* font, char* text)
{
    textDimensions_t dimensions = {0, font->size};

    for (int32_t i = 0; text[i]; i++) {
        dimensions.width += GetChar(font, text[i]).padding;
    }
    return dimensions;
}

void DrawText(uint8_t xt, uint8_t yt, font_t* font, const char* text)
{
    yt += font->size;

    for (int32_t i = 0; text[i]; i++) {
        glyph_t letter = GetChar(font, text[i]);

        uint16_t  bitCounter = 0;
        for (uint16_t x = 0; x < letter.width; x++) {
            for (uint16_t y = 0; y < letter.height; y++) {
                bool bit = letter.buffer[bitCounter/8] & 1 << (7 - (bitCounter & 0b111));
                SetPixel(xt +x+letter.xOffset, yt + y-letter.yOffset, !bit);

                bitCounter++;
            }
        }

        xt += letter.padding;
    }
}
```

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

## Requirements
- Python 3
- [requirements.txt](./requirements.txt)

Install requirements:
```sh
pip install -r requirements.txt
```

## Contributing
Feel free to submit issues or contribute improvements!
