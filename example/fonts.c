/**
 * @file fonts.c
 * @author thisranger
 * @date 11/03/2025
 * @last_update 11/03/2025
 */

/* ============================================================= */
/*                         INCLUDES                              */
/* ============================================================= */

#include "fonts.h"

/* ============================================================= */
/*                          DEFINES                              */
/* ============================================================= */

/* ============================================================= */
/*                        GLOBAL VARIABLES                       */
/* ============================================================= */

const font_t* FONT_fonts[] = {
        &FNT16_data,
};

/* ============================================================= */
/*                        LOCAL VARIABLES                        */
/* ============================================================= */

/* ============================================================= */
/*                     FUNCTION PROTOTYPES                       */
/* ============================================================= */

/* ============================================================= */
/*                      GLOBAL FUNCTIONS                         */
/* ============================================================= */

glyph_t FONT_GetChar(uint8_t fontId, char letter)
{
    font_t* font = FONT_fonts[fontId];

    if ( letter >= font->firstChar && letter <= font->lastChar){
        return font->glyphs[letter - font->firstChar];
    } else {
        printf("Char not available\n");
        return font->glyphs[0];
    }
}


void FONT_Draw(uint8_t x0, uint8_t y0, uint8_t fontId, char* text)
{
    y0 += FONT_fonts[fontId]->size;
    uint16_t i = 0;

    while (text[i] != NULL) {
        glyph_t letter = FONT_GetChar(fontId, text.chars[i]);

        uint16_t  bitCounter = 0;
        for (uint16_t x = 0; x < letter.width; x++) {
            for (uint16_t y = 0; y < letter.height; y++) {
                bool bit = letter.buffer[bitCounter/8] & 1 << (7 - bitCounter & 0b111);
                SetPixel(x0 +x+letter.xOffset, y0 + y-letter.yOffset, bit);

                bitCounter++;
            }
        }

        x0 += letter.padding;
        i++;
    }
}

/* ============================================================= */
/*                       LOCAL FUNCTIONS                         */
/* ============================================================= */

void SetPixel(uint8_t x0, uint8_t y0, bool black)
{
    //Draw pixel
}