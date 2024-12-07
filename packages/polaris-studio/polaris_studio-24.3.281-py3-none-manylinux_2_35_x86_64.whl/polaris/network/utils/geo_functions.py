# Copyright (c) 2024, UChicago Argonne, LLC
# BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
import numpy as np


# THIS FUNCTIONS APPROPRIATELY FOR PROJECTED COORDINATES ONLY
# FOR NON-PROJECTED COORDINATE SYSTEMS, SEE https://gist.github.com/jeromer/2005586
def compute_line_bearing(point_a: tuple, point_b: tuple) -> float:
    delta_lat = abs(point_a[1] - point_b[1])
    delta_long = abs(point_a[0] - point_b[0])
    return np.arctan2(delta_lat, delta_long) * 180 / np.pi


def intersection_bearing(point_a: tuple, point_b: tuple) -> float:
    degrees = np.arctan2(point_a[1] - point_b[1], point_a[0] - point_b[0]) * 180 / np.pi
    return (degrees + 360) % 360
