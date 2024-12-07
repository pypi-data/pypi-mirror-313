# Copyright (c) 2024, UChicago Argonne, LLC
# BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
from functools import partial
from pathlib import Path

from polaris.runs.convergence.convergence_callback_functions import do_nothing
from polaris.runs.convergence.convergence_config import ConvergenceConfig
from polaris.runs.convergence.convergence_iteration import ConvergenceIteration
from polaris.runs.convergence.convergence_runner import run_polaris_convergence
from polaris.runs.convergence.scenario_mods import base_scenario_mods
from polaris.runs.polaris_inputs import PolarisInputs
from polaris.runs.static_skimmer.assign_skim import assignment_skimming
from polaris.runs.static_skimmer.external_matrices import build_external_trip_matrices
from polaris.runs.static_skimmer.free_flow_skimmer import free_flow_skimming
from polaris.runs.static_skimmer.static_skimmer_inputs import STAInputs
from polaris.utils.cmd_runner import run_cmd
from polaris.utils.logging_utils import function_logging


@function_logging("  Static skimming")
def static_skimming(model_path: Path, iterations=10, sta_param=None):
    assig_pars = sta_param or STAInputs()
    config = ConvergenceConfig.from_file(model_path / "convergence_control.yaml")
    config.num_abm_runs = iterations
    config.do_skim = False
    config.do_abm_init = True
    inputs = PolarisInputs.from_dir(model_path)

    external_trips = build_external_trip_matrices(inputs.supply_db, inputs.demand_db, config.skim_interval_endpoints)

    if not inputs.transit_skim.exists():
        raise FileNotFoundError("Transit skim file not found. File is a strict requirement for this procedure")

    free_flow_skimming(config, inputs)

    run_polaris_convergence(
        config,
        scenario_file_fn=scenario_mods_for_skimming,
        end_of_loop_fn=partial(assignment_skimming, external_trips, assig_pars),
        async_end_of_loop_fn=do_nothing,
        cmd_runner=run_cmd_ignore_errors,
    )


def run_cmd_ignore_errors(cmd, working_dir, printer=print, ignore_errors=False, stderr_buf=None, **kwargs):
    run_cmd(cmd, working_dir, printer, ignore_errors=True, stderr_buf=stderr_buf)


def scenario_mods_for_skimming(config: ConvergenceConfig, current_iteration: ConvergenceIteration):
    mods, scenario_file = base_scenario_mods(config, current_iteration)
    mods["General simulation controls.early_exit"] = "after_activity_gen"
    mods["ABM Controls.tnc_feedback"] = False
    mods["Routing and skimming controls.time_dependent_routing"] = True
    return mods, scenario_file
