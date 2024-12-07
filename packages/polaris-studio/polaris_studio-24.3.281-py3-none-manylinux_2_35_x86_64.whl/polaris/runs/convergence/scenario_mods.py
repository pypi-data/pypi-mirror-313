# Copyright (c) 2024, UChicago Argonne, LLC
# BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
from polaris.runs.calibrate.calibration import scenario_mods_for_calibration
from polaris.runs.convergence.convergence_config import ConvergenceConfig
from polaris.runs.convergence.convergence_iteration import ConvergenceIteration


def get_scenario_for_iteration(config: ConvergenceConfig, current_iteration: ConvergenceIteration):
    # These are the standard set of mods that are always applied in a model run
    mods, scenario_file = base_scenario_mods(config, current_iteration)

    # This is some additional setup that may or may not be standard things we want to do
    if config.fixed_connectivity_penetration_rates_for_cv is not None:
        mods["use_fixed_connectivity_penetration_rates_for_cv"] = True
        mods["fixed_connectivity_penetration_rate_for_cv"] = config.fixed_connectivity_penetration_rates_for_cv

    if config.rsu_enabled_switching:
        mods["rsu_enabled_switching"] = True

    scenario_mods_for_calibration(config, current_iteration, mods, scenario_file)

    return mods, scenario_file


def base_scenario_mods(config: ConvergenceConfig, current_iteration: ConvergenceIteration):
    if current_iteration.is_skim:
        scenario_file, mods = setup_scenario_for_skimming(config)
    elif current_iteration.is_pop_synth:
        scenario_file, mods = setup_scenario_for_pop_synth(config)
    elif current_iteration.is_cristal:
        scenario_file, mods = setup_scenario_for_cristal(config)
    elif current_iteration.is_abm_init:
        scenario_file, mods = setup_scenario_for_abm_init(config)
    elif current_iteration.is_dta:
        scenario_file, mods = setup_scenario_for_dta_iteration(config, current_iteration)
    else:
        scenario_file, mods = setup_scenario_for_normal_iteration(config, current_iteration)

    # We always set the traffic scale factor to account for our reduced population sample
    mods["traffic_scale_factor"] = config.population_scale_factor

    # To ensure that we are doing ABM-DTA loops
    if config.num_outer_loops > 1 and (config.num_dta_runs) > 0:
        replan_workplaces = current_iteration.iteration_number % (config.num_abm_runs + config.num_dta_runs) == 1
        mods["Population synthesizer controls.replan.workplaces"] = replan_workplaces

    # Set the output directory
    mods["Output controls.output_directory"] = f"{config.db_name}_{current_iteration}"

    # Set dbname appropriately
    mods["database_name"] = config.db_name
    mods["input_result_database_name"] = config.db_name

    # The following is a code smell - I think we should get rid of any param from Config that is directly passed to json
    def pass_through_param(key):
        if getattr(config, key) is not None:
            mods[key] = getattr(config, key)

    pass_through_param("capacity_expressway")
    pass_through_param("capacity_arterial")
    pass_through_param("capacity_local")

    pass_through_param("realtime_informed_vehicle_market_share")
    pass_through_param("skim_averaging_factor")

    return mods, scenario_file


def setup_scenario_for_skimming(config: ConvergenceConfig):
    mods = {
        "Routing and skimming controls.time_dependent_routing": False,
        "Routing and skimming controls.time_dependent_routing_weight_factor": 1.0,
        "percent_to_synthesize": 0.0,
        "ABM Controls.read_trip_factors": {"External": 0.0},
        "read_population_from_database": False,
        "Population synthesizer controls.replan": {},  # no replanning as there is no population
        "vehicle_trajectory_sample_rate": 0.0,
        "skim_nodes_per_zone": 4,
        "read_skim_tables": False,
        "write_skim_tables": True,
        "generate_transit_skims": True,
        "skim_interval_endpoint_minutes": config.skim_interval_endpoints,
        "EV_charging": False,  # this slows down skimming and is not necessary
        "use_tnc_system": True,  # this slows down skimming but is necessary for TNC_AND_RIDE skims
        "tnc_feedback": False,
        "time_dependent_routing_weight_factor": 1.0,
    }
    return config.scenario_main, mods


def setup_scenario_for_pop_synth(config: ConvergenceConfig):
    mods = {
        "Routing and skimming controls.time_dependent_routing": False,
        "Population synthesizer controls.read_population_from_database": False,
        "Population synthesizer controls.percent_to_synthesize": config.population_scale_factor,
        "ABM Controls.read_trip_factors": {"External": 0.0},
        "time_dependent_routing_weight_factor": 1.0,
        "early_exit": "after_loc_choice",
        # question for brainstrust - does pop synth require skims to be read? Cant we just use whatever was in the json?
        "read_skim_tables": True,
    }
    return config.scenario_main, mods


def setup_scenario_for_abm_init(config: ConvergenceConfig):
    mods = {
        "Routing and skimming controls.time_dependent_routing": False,
        "Population synthesizer controls.read_population_from_database": False,
        "Population synthesizer controls.percent_to_synthesize": config.population_scale_factor,
        "ABM Controls.read_trip_factors": {"External": config.population_scale_factor},
        "time_dependent_routing": False,
        "time_dependent_routing_weight_factor": 1.0,
        "tnc_feedback": False,
        "vehicle_trajectory_sample_rate": config.trajectory_sampling / config.population_scale_factor,
    }
    return config.scenario_main, mods


def setup_scenario_for_cristal(config: ConvergenceConfig):
    mods = {
        "ABM Controls.read_trip_factors": {"External": 1.0},
        "Population synthesizer controls.read_population_from_database": True,
        "Population synthesizer controls.percent_to_synthesize": 1.0,
        "Routing and skimming controls.EV_charging": False,
        "use_tnc_system": False,
        "tnc_feedback": False,
        "multimodal_routing": False,
        "CRISTAL Controls.model_freight": True,
        "CRISTAL Controls.use_b2c_routing": True,
    }
    return config.scenario_main, mods


def setup_scenario_for_normal_iteration(config: ConvergenceConfig, current_iteration: ConvergenceIteration):
    replan_workplaces = config.workplace_stabilization.should_choose_workplaces(current_iteration)
    mods = {
        "Routing and skimming controls.time_dependent_routing_weight_factor": 1.0,
        "percent_to_synthesize": 1.0,
        "ABM Controls.read_trip_factors": {"External": 1.0, "ABM": 0.0},
        "read_population_from_database": True,
        "Population synthesizer controls.replan.workplaces": replan_workplaces,
        "vehicle_trajectory_sample_rate": config.trajectory_sampling / config.population_scale_factor,
    }

    mods["time_dependent_routing"] = True

    time_dependent_weight = 1.0
    # If routing MSA is enabled, only do it on iterations which are not (a) the first (b) workplace replanning iters
    if config.do_routing_MSA and config.workplace_stabilization.should_choose_workplaces(current_iteration):
        n = config.workplace_stabilization.number_of_prior_workplaces_iteration(current_iteration.iteration_number)
        time_dependent_weight = 1 / (current_iteration.iteration_number - n)
    mods["time_dependent_routing_weight_factor"] = time_dependent_weight

    if current_iteration.is_last:
        mods["Output controls.write_lc_traffic_trajectory"] = True

    return config.scenario_main, mods


def setup_scenario_for_dta_iteration(config, current_iteration):
    mods = {
        "Routing and skimming controls.time_dependent_routing_weight_factor": 1.0 / current_iteration.iteration_number,
        "Routing and skimming controls.time_dependent_routing_weight_factor_affects_choice": True,
        "Routing and skimming controls.time_dependent_routing_weight_factor_affects_calculation": False,
        "Routing and skimming controls.time_dependent_routing_gap_calculation_strategy": "use_average",
        "percent_to_synthesize": 1.0,
        "ABM Controls.read_trip_factors": {"External": 1.0, "ABM": 1.0, "TNC": 1.0},
        "read_population_from_database": True,
        "Population synthesizer controls.replan": {},  # No replanning of any type during DTA
        "read_trajectories": True,
        "convergence_mode": True,
        "vehicle_trajectory_sample_rate": 1.00,
        "time_dependent_routing": True,
    }

    return config.scenario_main, mods
