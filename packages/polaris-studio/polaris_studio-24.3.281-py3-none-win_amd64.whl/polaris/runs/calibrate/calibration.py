# Copyright (c) 2024, UChicago Argonne, LLC
# BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
from pathlib import Path

import pandas as pd
from polaris.runs.calibrate import activity_generation, destination_choice, mode_choice, timing_choice
from polaris.runs.convergence.convergence_config import ConvergenceConfig
from polaris.runs.convergence.convergence_iteration import ConvergenceIteration
from polaris.runs.run_utils import merge_csvs
from polaris.utils.logging_utils import stdout_logging

stdout_logging()


def scenario_mods_for_calibration(config: ConvergenceConfig, current_iteration: ConvergenceIteration, mods, file):
    if not config.calibration.should_calibrate(current_iteration):
        return
    warm_calibrating = False  # do_warm_start and loop >= first_warm_start_loop and loop < init_loop

    if warm_calibrating:
        mods["warm_start_activities"] = True

    return mods, file


def end_of_loop_fn_for_calibration(
    config: ConvergenceConfig, current_iteration: ConvergenceIteration, output_dir: Path
):
    if not config.calibration.should_calibrate(current_iteration):
        return

    RMSE_activity, RMSE_destination, RMSE_mode, RMSE_mode_boardings, RMSE_timing = -2, -2, -1, -2, -2

    if config.calibration.calibrate_activities:
        RMSE_activity = activity_generation.calibrate(config, current_iteration)

    if config.calibration.calibrate_destinations:
        RMSE_destination = destination_choice.calibrate(config, current_iteration)

    if config.calibration.calibrate_modes:
        RMSE_mode, RMSE_mode_boardings = mode_choice.calibrate(config, current_iteration)

    if config.calibration.calibrate_timings:
        RMSE_timing = timing_choice.calibrate(config, current_iteration)

    # We generate a csv into the iteration folder, then immediately merge it with any other csvs in other iterations
    # into a single merged rmse_report.csv in the root folder
    record = {
        "iteration": str(current_iteration),
        "RMSE_activity": RMSE_activity,
        "RMSE_mode": RMSE_mode,
        "RMSE_mode_boardings": RMSE_mode_boardings,
        "RMSE_destination": RMSE_destination,
        "RMSE_timing": RMSE_timing,
    }
    pd.DataFrame([record]).to_csv(output_dir / "rmse_report.csv", index=False)
    merge_csvs(config, "rmse_report.csv")
