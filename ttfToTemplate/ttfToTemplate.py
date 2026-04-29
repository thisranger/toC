import sys
import os
import freetype
import numpy as np
from PIL import Image
from jinja2 import Environment, FileSystemLoader

FIRST_CHAR = 32
LAST_CHAR = 126

IMAGE_WIDTH = 1024
IMAGE_HEIGHT = 256


def ProcessFont(fontPath, fontSize, startOffset):
    face = freetype.Face(fontPath)

    # 🔑 CRITICAL: use pixel size (NOT char size)
    face.set_pixel_sizes(0, fontSize)

    ascent = face.size.ascender >> 6
    descent = face.size.descender >> 6
    linegap = (face.size.height >> 6) - ascent + descent

    bitmapData = []
    glyphs = []
    byteOffset = startOffset

    image = np.zeros((IMAGE_HEIGHT, IMAGE_WIDTH), dtype=np.uint8)

    cursorX = 5
    cursorY = ascent + 5

    for charCode in range(FIRST_CHAR, LAST_CHAR + 1):
        face.load_char(
            chr(charCode),
            freetype.FT_LOAD_RENDER | freetype.FT_LOAD_TARGET_MONO
        )

        glyph = face.glyph
        bmp = glyph.bitmap

        width = bmp.width
        height = bmp.rows
        advance = glyph.advance.x >> 6

        # Handle empty glyphs
        if width == 0 or height == 0:
            glyphs.append({
                "width": 0,
                "height": 0,
                "padding": advance,
                "x_offset": 0,
                "y_offset": 0,
                "buffer": byteOffset
            })
            continue

        # Wrap to next line if needed
        if cursorX + width >= IMAGE_WIDTH:
            cursorX = 5
            cursorY += fontSize + 4

        glyphs.append({
            "width": width,
            "height": height,
            "padding": advance,
            "x_offset": glyph.bitmap_left,
            "y_offset": glyph.bitmap_top,
            "buffer": byteOffset
        })

        # Align glyph to baseline
        y_base = cursorY - glyph.bitmap_top

        bitOffset = 0
        bitmapData.append(0)
        byteOffset += 1

        for y in range(height):
            for x in range(width):
                # ✅ Correct bit extraction
                byte = bmp.buffer[y * bmp.pitch + (x >> 3)]
                pixel = byte & (0x80 >> (x & 7))

                if pixel:
                    bitmapData[-1] |= (1 << (7 - bitOffset))

                    # Draw preview safely
                    py = y_base + y
                    px = cursorX + x

                    if 0 <= py < IMAGE_HEIGHT and 0 <= px < IMAGE_WIDTH:
                        image[py, px] = 255

                bitOffset += 1

                if bitOffset == 8:
                    bitOffset = 0
                    bitmapData.append(0)
                    byteOffset += 1

        # Remove trailing empty byte
        if bitOffset == 0:
            bitmapData.pop()
            byteOffset -= 1

        # 🔑 Better spacing for pixel fonts
        cursorX += max(width, advance)

    return glyphs, bitmapData, byteOffset, image


def CollectFontPaths(paths):
    fontPaths = []

    for path in paths:
        if os.path.isfile(path):
            fontPaths.append(path)
        elif os.path.isdir(path):
            for root, _, files in os.walk(path):
                for file in files:
                    if file.lower().endswith((".ttf", ".otf")):
                        fontPaths.append(os.path.join(root, file))

    return fontPaths


def GenerateFontFile(templatePath, outputPath, fontPaths, fontSize, generatePreview):
    templateDir = os.path.dirname(templatePath) or "."
    templateFile = os.path.basename(templatePath)

    env = Environment(
        loader=FileSystemLoader(templateDir),
        trim_blocks=True,
        lstrip_blocks=True
    )

    template = env.get_template(templateFile)

    allBitmaps = []
    fonts = []
    offset = 0

    os.makedirs("previews", exist_ok=True)

    for fontPath in fontPaths:
        fontName = os.path.basename(fontPath).split('.', 1)[0]

        glyphs, bitmap, offset, image = ProcessFont(fontPath, fontSize, offset)

        fonts.append({
            "name": fontName,
            "glyphs": glyphs
        })

        allBitmaps += bitmap

        if generatePreview:
            previewPath = os.path.join("previews", f"{fontName}.png")
            Image.fromarray(image, mode='L').save(previewPath)
            print(f"Preview: {previewPath}")

    formattedBitmap = [f"0x{b:02X}" for b in allBitmaps]

    output = template.render(
        bitmap=formattedBitmap,
        fonts=fonts,
        first_char=FIRST_CHAR,
        last_char=LAST_CHAR,
        font_size=fontSize
    )

    with open(outputPath, "w") as f:
        f.write(output)

    print(f"Generated: {outputPath}")


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print(f"Usage: {sys.argv[0]} <template> <output> <size> [--preview] <fonts...>")
        sys.exit(1)

    templatePath = sys.argv[1]
    outputPath = sys.argv[2]
    fontSize = int(sys.argv[3])

    args = sys.argv[4:]

    generatePreview = False
    if "--preview" in args:
        generatePreview = True
        args.remove("--preview")

    fontPaths = CollectFontPaths(args)

    if not fontPaths:
        print("No fonts found.")
        sys.exit(1)

    GenerateFontFile(templatePath, outputPath, fontPaths, fontSize, generatePreview)