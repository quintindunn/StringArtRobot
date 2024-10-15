import os
import sys

import cv2 as cv

from threadArt import KasperMeertsAlgorithm

import logging


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    image_path = "../target/horse.jpg"
    width = 500
    number_of_nails = 288
    max_strings = 4000
    nail_skip = 30
    line_weight = 20
    min_distance = 20
    min_loop = 20

    result_file = "../output/results.txt"
    result_img = "../output/result.png"

    use_visualizer = True

    settings = {
        "Width": width,
        "Number of Nails": number_of_nails,
        "Max Strings": max_strings,
        "Nail Skip": nail_skip,
        "Line Weight": line_weight,
        "Min Distance": min_distance,
        "Min Loop": min_loop,
        "User Visualizer": use_visualizer
    }

    for k, v in settings.items():
        print(f"{k}: {v}")

    im = cv.imread(image_path)

    art = KasperMeertsAlgorithm(
            im=im,
            n_pins=number_of_nails,
            max_lines=max_strings,
            line_weight=line_weight,
            min_distance=min_distance,
            min_loop=min_loop,
            use_visualizer=True
    )
    art.run()
    seq = art.sequence

    if not os.path.isdir("../output"):
        os.mkdir("../output/")

    with open(result_file, 'w') as f:
        f.write(','.join(map(str, seq)))

