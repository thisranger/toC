# pngToTemplate

## Convert PNG to C Source Code
This project provides a Python script to convert PNG images into C source files using Jinja2 templates. It generates packed 1-bit bitmaps, which are ideal for monochrome displays in embedded systems.

### Features
Converts PNG to a packed bitmap format (1 bit per pixel).  
Thresholds grayscale images to black and white.
Uses Jinja2 templates for flexible output formatting.
Supports individual files or entire directories.

## Usage
### Command:
```sh
python pngToTemplate.py <template_file> <output_file> <image_files_or_directories...>
```

### Parameters:
- `<template_file>`: Path to the Jinja2 template file (e.g., `example/image.c.j2`).
- `<output_file>`: Path where the generated code will be saved (e.g., `example/image.c`).
- `<image_files_or_directories...>`: One or more paths to PNG files or directories containing them.

### Example:
```sh
python pngToTemplate.py example/image.c.j2 example/image.c example/file.png
```

See [example/](./example/) for a complete setup with templates.

## Example Usage
The following code demonstrates how to use the generated data to draw an icon.

```c
#include "image.h"

// Define these in your display driver
void SetPixel(uint8_t x, uint8_t y, bool color);
#define ON true
#define OFF false

void example() {
    // Draw an icon
    FONT_DrawIcon(0, 0, &IMAGE_file, false);
}
```

## Template Variables
The following variables are available in the Jinja2 template:
- `bitmap`: A list of integers (0-255) representing the packed 1-bit bitmap data.
- `images`: A list of image objects, each containing:
    - `name`: The base name of the image file.
    - `width`: Image width in pixels.
    - `height`: Image height in pixels.
    - `offset`: Byte offset in the `bitmap` array where this image's data starts.

## C Structure
The templates define an `icon_t` structure:
```c
typedef struct {
    const uint8_t* data;
    struct {
        uint8_t width, height;
    } size;
} icon_t;
```

## Requirements
- Python 3
- [requirements.txt](./requirements.txt)

Install requirements:
```sh
pip install -r requirements.txt
```
