# Copyright (c) 2024, UChicago Argonne, LLC
# BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
from .approximation import Approximation


def should_allow(intersection, inc: Approximation, out: Approximation) -> bool:
    """

    :rtype: object
    """
    for from_link, to_link, override in intersection.overrides:
        if from_link == inc.link and to_link == out.link:
            if override >= 0:
                out.penalty = override
                return True
            elif override == -1:
                return False
            else:
                raise ValueError(f"Penalty value for Turn_Override from {from_link} to {to_link} is invalid")

    if inc.link != out.link:
        return True

    if len(intersection.incoming) == len(intersection.outgoing) == 1:
        return True

    return intersection.u_turn
