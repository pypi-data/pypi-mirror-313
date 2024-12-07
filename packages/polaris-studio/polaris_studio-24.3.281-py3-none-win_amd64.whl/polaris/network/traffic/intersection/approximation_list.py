# Copyright (c) 2024, UChicago Argonne, LLC
# BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
from typing import List, Tuple

import numpy as np

from polaris.network.traffic.hand_of_driving import DrivingSide
from polaris.network.traffic.intersection.approximation import Approximation


def sort_approx_list(approximations: List[Approximation]) -> Tuple[List[Approximation], List[Approximation]]:
    """
    Sorts the approximations counter-clockwise around the intersection node, starting
    in the direction such that the difference between each angle and the previous angle
    is minimised.

    Returns the incoming and outgoing approximations in that order.

    The sorted order is reversed if using left-hand drive.
    """
    driving_side = approximations[0].driving_side
    data_list, idx, theta = pure_list_sorting(approximations)
    theta = theta[idx] + 180  # Reorder angles in order of data list and translate to 0-360 degrees

    # Get the difference between each angle and the previous angle
    diff = list(theta[1:] - theta[:-1])

    # Add angle from last direction to first
    if driving_side == DrivingSide.RIGHT:
        diff.append(360 + theta[0] - theta[-1])
    else:
        diff = [-360 + theta[0] - theta[-1]] + diff

    # Cyclically shift the list so that the largest difference is between the last and first angle
    if driving_side == DrivingSide.RIGHT:
        position = diff.index(max(diff)) + 1
    else:
        position = diff.index(min(diff))
    data_list = data_list[position:] + data_list[:position]

    # Get the incoming and outgoing approximations
    incoming = [inc for inc in data_list if inc.function == "incoming"][::-1]
    outgoing = [inc for inc in data_list if inc.function == "outgoing"]
    return incoming, outgoing


def pure_list_sorting(approximations: List[Approximation]) -> Tuple[List[Approximation], np.ndarray, np.ndarray]:
    """
    Sorts the approximations in ascending order of the angle they make with the intersection
    node (the origin node). This angle is considered counterclockwise from the -ve x-axis
    (ie, moving counterclockwise from the -ve x-axis starts from -180 degrees and goes to
    180 degrees at the -ve x-axis again).

    If left hand drive, the approximations are sorted in the reverse order.

    Returns the sorted list of approximations, the angle of each approximation in the order
    of the provided list of approximations and a mapping (idx) between the original list
    and sorted list.
    """
    # Determine whether the start/end node of the 1st approximation is the origin (intersection node)
    direc = 1 if approximations[0].function == "outgoing" else -1
    direc *= 1 if approximations[0].direction == 0 else -1
    direc = direc if direc == -1 else 0

    # Get the coordinates of the origin node from the 1st approximation
    node_coords = approximations[0].geo.coords[direc]
    zero = np.array(node_coords)

    def is_outgoing(approx: Approximation) -> bool:
        return approx.geo.coords[0] == node_coords

    # For each approximation, ~ determine the direction in which the lane is pointing relative to the origin node
    direc_vectors_list = []
    for approx in approximations:  # type: Approximation
        # Get the 2nd point in the approximation
        point1 = np.array(approx.geo.coords[1 if is_outgoing(approx) else -2])
        direc_vectors_list.append(point1 - zero)  # Make relative to origin node
    direc_vectors = np.array(direc_vectors_list)

    # Get the direction of each vector in degrees (0 is +ve x-axis)
    y_coords = direc_vectors[:, 1]  # type: np.ndarray
    x_coords = direc_vectors[:, 0]  # type: np.ndarray
    thetas = np.arctan2(y_coords, x_coords) * 180 / np.pi

    # Sort the approximations based on the direction of the vectors (lanes)
    idx = np.argsort(thetas)
    data_list = [approximations[x] for x in idx]

    if approximations[0].driving_side == DrivingSide.RIGHT:
        return (data_list, idx, thetas)
    else:  # Reverse for LH-drive
        return (data_list[::-1], idx[::-1], thetas)
