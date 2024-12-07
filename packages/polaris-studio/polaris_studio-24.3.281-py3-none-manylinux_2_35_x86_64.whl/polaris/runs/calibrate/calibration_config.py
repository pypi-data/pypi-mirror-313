# Copyright (c) 2024, UChicago Argonne, LLC
# BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
from pathlib import Path

from pydantic import BaseModel

from polaris.utils.config_utils import is_x_iteration


class CalibrationConfig(BaseModel):
    """Configuration class for the POLARIS calibration procedure.

    Calibration in POLARIS occurs by determining a delta from observed counts for key models (activity generation,
    mode choice, destination choice, timing choice) and using this to adjust the Alternative Specific Constants
    (ASC) of that model. This is done by modifying the JSON files in the root of the project at specified
    'calibration' iterations and then allowing the model to stabilise before re-evaluating.
    """

    enabled: bool = False
    """Flag that defines whether the calibation is used or not in a model run"""

    target_csv_dir: Path = "calibration_targets"
    """Directory where the calibration target files are located (mode_choice_targets.csv, 
    destination_choice_targets.csv, timing_choice_targets.csv, activity_generation_targets.csv)
    """

    first_calibration_iteration: int = 1
    """The first iteration at which ASC adjustment should be undertaken (i.e. start)"""

    calibrate_every_x_iter: int = 4
    """The number of iterations between calibration iterations (i.e. step)"""

    last_calibration_iteration: int = 21
    """Last iteration at which ASC adjustment can take place, note that calibration is not 
    guaranteed to happen at this iteration unless it is specified by the start and step parameters."""

    calibrate_activities: bool = True
    """Flag that defines if activity generation ASCs are adjusted at each calibration iteration"""
    calibrate_destinations: bool = True
    """Flag that defines if destination choice ASCs (by activity type) are adjusted at each calibration iteration"""
    calibrate_modes: bool = True
    """Flag that defines if mode shares ASCs (by trip purpose) are adjusted at each calibration iteration"""
    calibrate_timings: bool = True
    """Flag that defines if departure time ASCs (by trip purpose) are adjusted at each calibration iteration"""

    step_size: float = 2.0
    """The rate at which the calibrated ASCs are changed during each calibration iteration (e.g., 2 means calibrated values are increased/decreased by 2x the value they should be based on the gap in model outputs and targets)"""

    # hack this in here until we can figure a way to get warm_start_act to not THROW_EXCEPTION
    warm_calibrating: bool = False
    """Flag to run calibration with only planning outputs meaning demand has not been assigned on network and no feedback of travel times for choices is not accounted"""

    def normalise_paths(self):
        self.target_csv_dir = Path(self.target_csv_dir).resolve()

    def should_calibrate(self, iteration):
        i = iteration.iteration_number
        return (
            self.enabled
            and iteration.is_standard
            and is_x_iteration(
                self.first_calibration_iteration, self.last_calibration_iteration, self.calibrate_every_x_iter, i
            )
        )
