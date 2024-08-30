import os
import sys

import cv2
import cv2 as cv

from threadArt import HalfmontyAlgorithm

import logging


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    image_path = "../target/horse.jpg"
    width = 500
    number_of_nails = 288
    max_strings = 4000
    nail_skip = 30
    line_weight = 20

    result_file = "../output/results.txt"
    result_img = "../output/result.png"

    use_visualizer = True

    settings = {
        "Width": width,
        "Number of Nails": number_of_nails,
        "Max Strings": max_strings,
        "Nail Skip": nail_skip,
        "Line Weight": line_weight
    }

    for k, v in settings.items():
        print(f"{k}: {v}")

    im = cv.imread(image_path, cv2.IMREAD_GRAYSCALE)

    seq = HalfmontyAlgorithm(im, pin_count=number_of_nails, min_distance=nail_skip, max_lines=max_strings,
                             line_weight=line_weight, img_size=width, use_visualizer=True).run()

    if not os.path.isdir("../output"):
        os.mkdir("../output/")

    with open(result_file, 'w') as f:
        f.write(','.join(map(str, seq)))

