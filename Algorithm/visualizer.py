import dataclasses
import random

import cv2 as cv
import numpy as np

from polar_system import polar_to_cartesian, cartesian_to_polar, deg_to_rad, rad_to_deg


@dataclasses.dataclass
class Nail:
    def __init__(self, x, y, idx):
        self.x = x
        self.y = y
        self.idx = idx


class String:
    def __init__(self, start_nail: Nail, end_nail: Nail, idx: int, color: tuple[int, int, int] = (0, 0, 0),
                 thickness=2):
        self.start_nail = start_nail
        self.end_nail = end_nail
        self.idx = idx
        self.color = color
        self.thickness = thickness

    def draw(self, im: np.array):
        pt1 = self.start_nail.x, self.start_nail.y
        pt2 = self.end_nail.x, self.end_nail.y
        cv.line(im, pt1=pt1, pt2=pt2, color=self.color)


class StringVisualizer:
    def __init__(self, nail_count: int = 300, diameter: int = 900,
                 background_color: tuple[int, int, int] = (255, 255, 255),
                 circle_color: tuple[int, int, int] = (0, 0, 0),
                 nail_color: tuple[int, int, int] = (127, 127, 127),
                 line_color: tuple[int, int, int] = (0, 0, 0),
                 line_thickness=1,
                 padding: int = 20,
                 win_name: str = "Strings"):
        self.nail_count = nail_count
        self.win_name = win_name
        self.diameter = diameter

        self.circle_color = circle_color
        self.nail_color = nail_color
        self.line_color = line_color

        self.line_thickness = line_thickness

        self.im = np.zeros((diameter + 2*padding, diameter + 2*padding, 3), dtype=np.uint8)
        self.im[::] = background_color
        self._cx, self._cy = self.im.shape[0] // 2, self.im.shape[1] // 2
        self.center = (self._cx, self._cy)
        cv.circle(img=self.im, center=self.center, radius=diameter//2, color=circle_color, thickness=1)

        self.nails: list[Nail] = []
        self.strings: list[String] = []

    @property
    def current_nail(self) -> Nail | None:
        if len(self.strings) != 0:
            return self.strings[-1].end_nail
        return self.nails[0]

    def add_nail(self, idx, cx, cy):
        self.nails.insert(idx, Nail(cx, cy, idx))
        cv.circle(img=self.im, center=(cx, cy), color=self.nail_color, radius=2, thickness=-2)

    def add_line(self, nail_1: int | Nail, nail_2: int | Nail):
        if isinstance(nail_1, int):
            nail_1 = self.nails[nail_1]
        if isinstance(nail_2, int):
            nail_2 = self.nails[nail_2]

        line = String(start_nail=nail_1, end_nail=nail_2, idx=len(self.strings), color=self.line_color,
                      thickness=self.line_thickness)
        self.strings.append(line)
        line.draw(self.im)

    def next_line(self, to_nail: int | Nail):
        if isinstance(to_nail, int):
            to_nail = self.nails[to_nail]

        from_nail = self.current_nail
        self.add_line(nail_1=from_nail, nail_2=to_nail)

    def generate_nails(self, live_delay: int | None = None):
        nail_spacing_deg = 360/self.nail_count

        theta = 0
        for i in range(0, self.nail_count):
            if theta >= 360:
                break
            x1, y1 = polar_to_cartesian(self.diameter//2, deg_to_rad(theta))
            x, y = map(int, (self._cx + x1, self._cy + y1))
            self.add_nail(i, x, y)
            theta += nail_spacing_deg

            self.update(live_delay)

    def from_lines(self, file_path: str, live_update: int | None = 1):
        with open(file_path, 'r') as f:
            indices = f.read().split(",")[1:]

        for idx in map(int, indices):
            visualizer.next_line(idx)
            self.update(live_update)

    def update(self, delay: int | None = 1, width: int = 1024):
        im_new = cv.resize(self.im, (width, width), interpolation=cv.INTER_CUBIC)
        cv.imshow(self.win_name, im_new)
        if delay is not None:
            cv.waitKey(delay)


if __name__ == '__main__':
    visualizer = StringVisualizer(diameter=2500)
    visualizer.generate_nails(1)

    # Generated from https://halfmonty.github.io/StringArtGenerator/
    visualizer.from_lines("test.lines", 1)
    cv.imwrite("output.png", visualizer.im)
