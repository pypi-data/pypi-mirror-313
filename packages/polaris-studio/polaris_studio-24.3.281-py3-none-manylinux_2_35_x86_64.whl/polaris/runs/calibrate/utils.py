# Copyright (c) 2024, UChicago Argonne, LLC
# BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
import logging
import math

import pandas as pd


def log_data(data, columns, index=None):
    index = index or columns[0:2]
    logging.info("\n\t" + pd.DataFrame(data, columns=columns).set_index(index).to_string().replace("\n", "\n\t") + "\n")


def calculate_rmse(simulated, target):
    if target is None:
        return -2
    sample_size, total_error_sq = 0, 0.0
    for key in set.intersection(set(target.keys()), set(simulated.keys())):
        if simulated[key] > 0 and target[key] > 0:
            sample_size += 1
            total_error_sq += math.pow((target[key] - simulated[key]), 2)
    return math.sqrt(total_error_sq / sample_size) if sample_size > 0 else -1
