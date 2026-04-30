import sys
import os
from jinja2 import Environment, FileSystemLoader
import numpy as np
from PIL import Image



def ProcessImage(imagePath, byteOffset):
    img = Image.open(imagePath).convert("L")  # Convert to grayscale
    img = img.point(lambda p: 255 if p > 128 else 0)  # Threshold to B/W
    img = img.convert("1")  # Convert to pure black/white
    width, height = img.size
    pixels = np.array(img, dtype=np.uint8)

    metaData = {
        "name": os.path.basename(imagePath).split('.', 1)[0],
        "width": width,
        "height": height,
        "offset": byteOffset
    }

    bitmap = []
    bitOffset = 0
    bitmap.append(0)
    byteOffset += 1

    for x in range(width):
        for y in range(height):
            if pixels[y, x] == 0:  # Black pixel
                bitmap[-1] |= (1 << (7 - bitOffset))
            bitOffset += 1
            if bitOffset == 8:
                bitOffset = 0
                byteOffset += 1
                bitmap.append(0)

    if bitOffset == 0:
        byteOffset -= 1
        bitmap.pop()

    return metaData, byteOffset, bitmap



def GenerateImageFile(templatePath, outputPath, paths):
    offset = 0;
    bitmaps = [];
    images = [];

    for path in paths:
        if os.path.isfile(path):
            image, offset, bitmap = ProcessImage(path, offset)
            images.append(image)
            bitmaps += bitmap
        elif os.path.isdir(path):
            for root, dirs, files in os.walk(path):
                for file in files:
                    fullPath = os.path.join(root, file)
                    image, offset, bitmap = ProcessImage(fullPath, offset)
                    images.append(image)
                    bitmaps += bitmap

    formattedBitmap = [f"0x{b:02X}" for b in bitmaps]

    templateDir = os.path.dirname(templatePath) or "."
    templateFile = os.path.basename(templatePath)

    env = Environment(
        loader=FileSystemLoader(templateDir),
        trim_blocks=True,
        lstrip_blocks=True
    )
    template = env.get_template(templateFile)

    output = template.render(
        bitmap=formattedBitmap,
        images=images
    )

    with open(outputPath, "w") as f:
        f.write(output)



if __name__ == "__main__":
    if len(sys.argv) < 4:
        print(f"Usage: {sys.argv[0]} <template.tmp> <output.h> <image1.png> [directory, image2.png ...]")
        sys.exit(1)
    GenerateImageFile(sys.argv[1], sys.argv[2], sys.argv[3:])
