# Copyright (c) 2024, UChicago Argonne, LLC
# BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
from pathlib import Path
from typing import List, Dict

import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse._coo import coo_matrix as coo_type

from polaris.analyze.trip_metrics import TripMetrics

pces = {"SOV_0": 1.0, "TAXI_9": 1.0, "MD_TRUCK_17": 2.5, "HD_TRUCK_18": 4.0, "BPLATE_19": 2.0, "LD_TRUCK_20": 1.8}


def build_external_trip_matrices(supply_path: Path, demand_path: Path, intervals: List[int]) -> Dict[int, coo_type]:
    trip_metr = TripMetrics(supply_path, demand_path)

    pre = 0
    external_matrices = {}
    for interv in intervals:
        matrix = trip_metr.vehicle_trip_matrix(from_start_time=pre * 60, to_start_time=interv * 60)
        for i, mat in enumerate(matrix.names):
            matrix.matrix[mat][:, :] *= pces[mat]
        external_matrices[interv] = coo_matrix(matrix.matrices.sum(axis=2))
        pre = interv
    return external_matrices
