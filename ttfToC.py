import freetype
import numpy as np
from PIL import Image

FIRST_CHAR = 32
LAST_CHAR = 126
IMAGE_WIDTH = 1024
IMAGE_HEIGHT = 256

class Glyph:
    def __init__(self, width, height, padding, x_offset, y_offset, buffer):
        self.width = width
        self.height = height
        self.padding = padding
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.buffer = buffer


def generate_font_header(font_path, output_header, output_image, global_name, font_size):
    face = freetype.Face(font_path)
    face.set_pixel_sizes(0, font_size)

    bitmap_data = bytearray()
    glyphs = []
    byte_pos = 0

    image = np.zeros((IMAGE_HEIGHT, IMAGE_WIDTH), dtype=np.uint8)
    cursor_x, cursor_y = 5, font_size + 5

    for index, char_code in enumerate(range(FIRST_CHAR, LAST_CHAR + 1)):
        face.load_char(chr(char_code), freetype.FT_LOAD_RENDER)
        bmp = face.glyph.bitmap
        advance_width = face.glyph.advance.x >> 6  # Convert 26.6 fixed point to integer

        if bmp.width == 0 or bmp.rows == 0:
            glyphs.append(Glyph(0, 0, advance_width, 0, 0, byte_pos))
            continue

        glyph = Glyph(bmp.width, bmp.rows, advance_width, face.glyph.bitmap_left, face.glyph.bitmap_top, byte_pos)
        glyphs.append(glyph)

        if cursor_x + bmp.width >= IMAGE_WIDTH:
            cursor_x = 5
            cursor_y += font_size + 5

        bitmap_data.append(0)
        bit_pos = 0
        byte_pos += 1

        for x in range(bmp.width):
            for y in range(bmp.rows):
                pixel_value = bmp.buffer[y * bmp.pitch + x]  # Get grayscale pixel value
                if pixel_value > 128:
                    bitmap_data[-1] |= (1 << (7-bit_pos))
                    image[cursor_y - glyph.y_offset + y, cursor_x + x] = 255

                bit_pos += 1
                if bit_pos == 8:
                    bit_pos = 0
                    byte_pos += 1
                    bitmap_data.append(0)
        cursor_x += advance_width

        if bit_pos == 0:
            byte_pos -= 1
            bitmap_data.pop()

    with open(output_header, "w") as f:
        f.write(f"#include <stdint.h>\n#include \"..\\fonts.h\"\n\n")

        f.write(f"static const uint8_t fontBitmap[] = {{\n")
        for i in range(0, len(bitmap_data), 16):
            f.write("\t" + ", ".join(f"0x{b:02X}" for b in bitmap_data[i:i + 16]) + ",\n")
        f.write("};\n\n")

        f.write(f"static const glyph_t fontGlyphs[{LAST_CHAR - FIRST_CHAR + 1}] = {{\n")
        for g in glyphs:
            f.write(f"\t{{{g.width}, {g.height}, {g.padding}, {g.x_offset}, {g.y_offset}, &fontBitmap[{g.buffer}]}},\n")
        f.write("};\n\n")

        f.write(
            f"const font_t {global_name}_data = {{{font_size}, {FIRST_CHAR}, {LAST_CHAR}, (glyph_t *) &fontGlyphs}};\n")

    img = Image.fromarray(image, mode='L')
    img.save(output_image)
    print(f"Font header generated: {output_header}")
    print(f"Font preview image generated: {output_image}")



if __name__ == "__main__":
    import sys

    if len(sys.argv) < 4:
        print(f"Usage: {sys.argv[0]} <font.ttf> <output.c> <preview.png> <global variable name> <size>")
        sys.exit(1)
    generate_font_header(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], int(sys.argv[5]))