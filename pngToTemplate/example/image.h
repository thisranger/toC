#ifndef image_H
#define image_H

#include <stdio.h>
#include <stdint.h>



typedef struct {
    uint8_t* data;
    struct {
        uint8_t width, height;
    } size;
} image_t;



extern image_t IMAGE_dir;
extern image_t IMAGE_file;

#endif /* image_H */