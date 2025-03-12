/**
 * @file fonts.h
 * @author thisranger
 * @date 11/03/2025
 * @last_update 11/03/2025
 */

#ifndef fonts_H
#define fonts_H

/* ============================================================= */
/*                          INCLUDES                             */
/* ============================================================= */
#include <stdio.h>
#include <stdint.h>

/* ============================================================= */
/*                          DEFINES                              */
/* ============================================================= */

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

/* ============================================================= */
/*                     GLOBAL VARIABLES                          */
/* ============================================================= */

extern const font_t FNT16_data;

extern const font_t* FONT_fonts[];

/* ============================================================= */
/*                     FUNCTION PROTOTYPES                       */
/* ============================================================= */

glyph_t FONT_GetChar(uint8_t fontId, char letter);
void FONT_Draw(uint8_t x0, uint8_t y0, uint8_t fontId, char* text);

#endif /* fonts_H */
