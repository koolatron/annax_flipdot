#!/usr/bin/python

import time
import os
from PIL import Image, ImageDraw, ImageFont

def main():
    W, H = (240, 16)
    string = u"The quick brown fox jumps Over The lazy dog"

    fontselect = [("../fonts/" + file, size) for file in os.listdir('../fonts/') for size in range(15, 19)]

    for (file, size) in fontselect:
        try:
            font = ImageFont.truetype(file, size)

            img = Image.new("1", (W,H))
            draw = ImageDraw.Draw(img)
            w, h = draw.textsize(string, font=font)
            draw.text((((W-w)/2),(H-h)/2), string, font=font, fill=(1))

            img.save("%s-%d.png" % (os.path.basename(file), size))
        except:
            pass

if __name__ == "__main__":
    main()
