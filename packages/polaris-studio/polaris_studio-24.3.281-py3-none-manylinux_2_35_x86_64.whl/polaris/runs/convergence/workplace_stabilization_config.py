# Copyright (c) 2024, UChicago Argonne, LLC
# BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
from pydantic import BaseModel

from polaris.utils.config_utils import is_x_iteration


class WorkplaceStabilizationConfig(BaseModel):
    """Configuration class for the POLARIS workplace stabilization process.

    Workplace stabilization in POLARIS is the process by which long-term decisions regarding work location
    are introduced to an overall iterative process. Work places are allowed to be updated based on current
    congestion conditions on specified iterations, a number of iterations are then run using those updated
    choices to allow the congestion to stabilize before repeating the process.
    """

    enabled: bool = False
    """Flag which controls if any workpalce stabilization will be undertaken during the model run"""

    first_workplace_choice_iteration: int = 1
    """The first iteration at which workplace choice should be allowed (i.e. start)"""

    choose_workplaces_every_x_iter: int = 5
    """The number of iterations between workplace choice iterations (i.e. step)"""

    last_workplace_choice_iteration: int = 31
    """Last iteration at which it is possible to choose work places, note that workplace choice is
    not guaranteed to happen at this iteration unless it is specified by the start and step parameters."""

    def should_choose_workplaces(self, iteration):
        return iteration.is_standard and self._should_choose_workplaces(iteration.iteration_number)

    def number_of_prior_workplaces_iteration(self, i: int) -> float:
        return float(sum([self._should_choose_workplaces(e) for e in range(1, i)]))

    def _should_choose_workplaces(self, i):
        return self.enabled and is_x_iteration(
            self.first_workplace_choice_iteration,
            self.last_workplace_choice_iteration,
            self.choose_workplaces_every_x_iter,
            i,
        )
