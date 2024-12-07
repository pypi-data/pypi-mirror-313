# Copyright (c) 2024, UChicago Argonne, LLC
# BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
import logging
import math
from pathlib import Path

import pandas as pd
from polaris.runs.calibrate.utils import calculate_rmse, log_data
from polaris.runs.convergence.convergence_config import ConvergenceConfig
from polaris.runs.convergence.convergence_iteration import ConvergenceIteration
from polaris.runs.scenario_file import load_json, write_json
from polaris.runs.wtf_runner import render_wtf_file, sql_dir
from polaris.utils.database.db_utils import commit_and_close, has_table, run_sql
from polaris.utils.logging_utils import function_logging


@function_logging("Calibrating destinations")
def calibrate(config: ConvergenceConfig, current_iteration: ConvergenceIteration):
    cconfig = config.calibration
    if cconfig.warm_calibrating:
        return -1

    target = load_target(cconfig.target_csv_dir / "destination_choice_targets.csv")
    simulated = load_simulated(current_iteration.files.demand_db)

    top_level_key = "ADAPTS_Destination_Choice_Model"
    model_file = Path(load_json(current_iteration.scenario_file)["ABM Controls"]["destination_choice_model_file"]).name
    output_dict = load_json(current_iteration.output_dir / "model_files" / model_file)[top_level_key]

    data, not_found_vars = [], []
    for var in map_vars:
        var_name = f"C_DISTANCE_{map_vars[var]}"
        if var_name in output_dict:
            v = float(output_dict[var_name])
        else:
            v = 1.0
            not_found_vars.append(var_name)

        if var in simulated and var in target and simulated[var] > 0 and target[var] > 0:
            new_v = v + cconfig.step_size * math.log(simulated[var] / target[var])
        else:
            new_v = v
        data.append([var, map_vars[var], target.get(var, 0), simulated.get(var, 0), v, new_v])

        output_dict[var_name] = new_v

    if not_found_vars:
        logging.warning(f"Variables not found in the original Destination Choice File: {not_found_vars}")

    log_data(data, ["variable", "asc", "target", "modelled", "old_v", "new_v"])

    write_json(config.data_dir / model_file, {top_level_key: output_dict})
    return calculate_rmse(simulated, target)


def load_target(target_file):
    return pd.read_csv(target_file).set_index("ACTIVITY_TYPE")["distance"].to_dict()


def load_simulated(demand_database):
    with commit_and_close(demand_database) as conn:
        if not has_table(conn, "ttime_By_ACT_Average"):
            run_sql(render_wtf_file(sql_dir / "travel_time.template.sql", 1.0), conn)
            conn.commit()

        sql = "SELECT acttype, ttime_avg, dist_avg from TTIME_by_ACT_Average"
        simulated = {act: avg_dist for act, tt, avg_dist in conn.execute(sql).fetchall()}

        # TODO: document why are we doing this?
        simulated["OTHER"] = simulated.get("PERSONAL", 0)

        return simulated


map_vars = {
    "EAT OUT": "EAT_OUT",
    "OTHER": "OTHER",
    "PICKUP-DROPOFF": "PICK",
    "RELIGIOUS-CIVIC": "CIVIC",
    "SERVICE": "SERVICE",
    "SHOP-MAJOR": "MAJ_SHOP",
    "SHOP-OTHER": "MIN_SHOP",
    "SOCIAL": "SOCIAL",
    "WORK": "WORK",
    "LEISURE": "LEISURE",
    "ERRANDS": "ERRANDS",
}
