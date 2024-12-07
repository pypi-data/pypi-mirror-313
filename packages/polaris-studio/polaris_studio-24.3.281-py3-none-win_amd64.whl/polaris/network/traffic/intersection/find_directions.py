# Copyright (c) 2024, UChicago Argonne, LLC
# BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
def find_directions(angle: float) -> str:
    if angle < 45 or angle > 315:
        return "NB"
    if 45 <= angle < 135:
        return "EB"
    if 135 <= angle < 225:
        return "SB"
    return "WB"
