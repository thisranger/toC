#ifndef fonts_H
#define fonts_H

#include <stdio.h>
#include <stdint.h>

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

typedef struct {
    uint8_t width, height;
} textDimensions_t;



extern font_t FONT_zpix_12;
extern font_t FONT_CozetteVector_12;

#endif /* fonts_H */