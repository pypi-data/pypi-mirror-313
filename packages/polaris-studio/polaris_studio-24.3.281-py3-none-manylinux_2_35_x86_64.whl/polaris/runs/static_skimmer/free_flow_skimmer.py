# Copyright (c) 2024, UChicago Argonne, LLC
# BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
import numpy as np
import openmatrix as omx
from aequilibrae.paths.network_skimming import NetworkSkimming
from tables import Filters

from polaris.runs.convergence.convergence_config import ConvergenceConfig
from polaris.runs.polaris_inputs import PolarisInputs
from polaris.runs.static_skimmer.intrazonals import fill_intrazonals
from polaris.runs.static_skimmer.static_graph import build_graph
from polaris.utils.logging_utils import function_logging


@function_logging("  Free flow skimming")
def free_flow_skimming(config: ConvergenceConfig, polaris_inputs: PolarisInputs):
    if polaris_inputs.highway_skim.exists():
        return

    graph = build_graph(polaris_inputs.supply_db)
    ns = NetworkSkimming(graph)
    ns.execute()

    ttime = ns.results.skims.time.astype(np.float32)
    distance = ns.results.skims.distance.astype(np.float32)

    data = {"time": fill_intrazonals(ttime), "distance": fill_intrazonals(distance)}
    data["cost"] = np.zeros_like(data["distance"], dtype=np.float32)
    compression = Filters(complevel=4, complib="zlib")
    with omx.open_file(polaris_inputs.highway_skim, "w", filters=compression) as omx_export:
        omx_export.create_mapping("taz", graph.centroids)
        for interv in config.skim_interval_endpoints:
            for metric, values in data.items():
                slice_name = f"auto_{interv}_{metric}"
                # Add values and all its attributes
                omx_export[slice_name] = values
                omx_export[slice_name].attrs.timeperiod = interv
                omx_export[slice_name].attrs.metric = metric
                omx_export[slice_name].attrs.mode = "auto"
        omx_export.root._v_attrs["interval_count"] = np.array([len(config.skim_interval_endpoints)]).astype("int32")
        omx_export.root._v_attrs["update_intervals"] = np.array(config.skim_interval_endpoints).astype("float32")

    assert not np.any(np.isinf(distance))
    assert not np.any(np.isinf(ttime))
