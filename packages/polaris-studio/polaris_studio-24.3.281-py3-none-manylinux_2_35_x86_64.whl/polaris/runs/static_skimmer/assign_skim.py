# Copyright (c) 2024, UChicago Argonne, LLC
# BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
import logging
from pathlib import Path
from typing import Dict

import numpy as np
import openmatrix as omx
from aequilibrae.matrix.aequilibrae_matrix import AequilibraeMatrix
from scipy.sparse._coo import coo_matrix as coo_type
from tables import Filters

from polaris.analyze.activity_metrics import ActivityMetrics
from polaris.analyze.result_kpis import ResultKPIs
from polaris.runs.convergence.convergence_callback_functions import copy_back_files
from polaris.runs.convergence.convergence_config import ConvergenceConfig
from polaris.runs.convergence.convergence_iteration import ConvergenceIteration
from polaris.runs.polaris_inputs import PolarisInputs
from polaris.runs.static_skimmer.intrazonals import fill_intrazonals
from polaris.runs.static_skimmer.static_assign import assign_with_skim
from polaris.runs.static_skimmer.static_graph import build_graph
from polaris.runs.static_skimmer.static_skimmer_inputs import STAInputs
from polaris.utils.logging_utils import function_logging


@function_logging("  Assignment skimming")
def assignment_skimming(
    external_trips: Dict[int, coo_type],
    assig_pars: STAInputs,
    config: ConvergenceConfig,
    current_iteration: ConvergenceIteration,
    output_dir: Path,
    polaris_inputs: PolarisInputs,
):
    act_metr = ActivityMetrics(polaris_inputs.supply_db, output_dir / polaris_inputs.demand_db.name)
    graph = build_graph(polaris_inputs.supply_db)
    compression = Filters(complevel=0, complib="zlib")
    omx_export = omx.open_file(output_dir / polaris_inputs.highway_skim.name, "w", filters=compression)
    omx_export.create_mapping("taz", graph.centroids)
    omx_export.root._v_attrs["interval_count"] = np.array([len(config.skim_interval_endpoints)]).astype("int32")
    omx_export.root._v_attrs["update_intervals"] = np.array(config.skim_interval_endpoints).astype("float32")

    aeq_data = output_dir / "aequilibrae_data"
    aeq_data.mkdir(exist_ok=True)
    graph.network.to_parquet(aeq_data / "graph_network.parquet")

    ch = logging.FileHandler(output_dir / "log" / "polaris_progress.log")
    ch.setFormatter(logging.Formatter("%(asctime)s;%(message)s"))
    ch.name = "POLARIS LOG"
    ch.setLevel(logging.INFO)
    logger = logging.getLogger("aequilibrae")
    logger.addHandler(ch)

    pre = 0
    logging.basicConfig(level=logging.ERROR)

    for interv in config.skim_interval_endpoints:
        logger.info(f"      Skimming period: {interv}")
        matrix = act_metr.vehicle_trip_matrix(from_start_time=pre * 60, to_start_time=interv * 60)

        # We only have car trips among our activities, so no PCE conversion needed

        # We collapse all matrices onto the first matrix slice
        if len(matrix.names) == 0:
            matrix = AequilibraeMatrix()
            zones = graph.centroids.shape[0]
            matrix.create_empty(zones=zones, matrix_names=["SOV"], index_names=["taz"], memory_only=True)
            matrix.index[:] = graph.centroids[:]
            matrix.computational_view()

        elif len(matrix.names) > 1:
            matrix.matrices[:, :, 0] = matrix.matrices.sum(axis=2)[:, :]
            matrix.matrices[:, :, 1:] = 0
        matrix.matrix[matrix.names[0]] += np.nan_to_num(external_trips[interv].todense())
        # Convert to an average 1h demand
        matrix.matrices /= (interv - pre) / 60

        matrix.computational_view(matrix.names[0])
        matrix.export(str(aeq_data / f"demand_matrix_{interv}.omx"), cores=[matrix.names[0]])
        skims = assign_with_skim(graph, matrix, assig_pars)

        for metric, value in skims.items():
            slice_name = f"auto_{interv}_{metric}"
            omx_export[slice_name] = fill_intrazonals(value)
            omx_export[slice_name].attrs.timeperiod = interv
            omx_export[slice_name].attrs.metric = metric
            omx_export[slice_name].attrs.mode = "auto"
        del skims
        pre = interv
    del matrix
    del graph

    for handler in logger.handlers:
        if handler.get_name() == "POLARIS LOG":
            logger.removeHandler(handler)
            break

    omx_export.close()
    copy_back_files(config, current_iteration)
    dt = [
        "skim_stats",
        "activity_duration_distribution",
        "distance_by_act_type",
        "planned_modes",
        "activity_start_distribution",
    ]
    ResultKPIs.from_iteration(current_iteration).cache_all_available_metrics(metrics_to_cache=dt)
