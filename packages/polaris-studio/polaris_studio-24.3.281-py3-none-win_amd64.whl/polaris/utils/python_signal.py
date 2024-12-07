# Copyright (c) 2024, UChicago Argonne, LLC
# BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
import importlib.util as iutil
from random import choice

from polaris.utils.env_utils import is_on_ci

missing_tqdm = iutil.find_spec("tqdm") is None

if not missing_tqdm:
    notebook = iutil.find_spec("ipywidgets") is not None
    if notebook:
        from tqdm.notebook import tqdm  # type: ignore
    else:
        from tqdm import tqdm  # type: ignore


class PythonSignal:  # type: ignore
    """
    This class only manages where the updating information will flow to, either emitting signals
    to the QGIS interface to update is progress bars or to update the terminal progress bars
    powered by tqdm

    Structure of data is the following:

    ['action', 'bar hierarchy', 'value', 'text', 'master']

    'action': 'start', 'update', or 'finished_*_processing' (the last one applies in QGIS)
    'bar hierarchy': 'master' or 'secondary'
    'value': Numerical value for the action (total or current)
    'text': Whatever label to be updated
    'master': The corresponding master bar for this task
    """

    deactivate = is_on_ci() or missing_tqdm  # by default don't use progress bars in tests

    def __init__(self, object):
        self.color = choice(["green", "magenta", "cyan", "blue", "red", "yellow"])
        self.masterbar = None  # type: tqdm
        self.secondarybar = None  # type: tqdm

        self.current_master_data = {}

    def emit(self, val):
        if self.deactivate:
            return
        if len(val) == 1:
            if "finished_" not in val[0] or "_procedure" not in val[0]:
                raise Exception("Wrong signal")
            for bar in [self.masterbar, self.secondarybar]:
                if bar is not None:
                    bar.close()
            return

        action, bar, qty, txt = val[:4]

        if action == "start":
            if bar == "master":
                self.masterbar = tqdm(total=qty, colour=self.color, leave=False, desc=txt)
            else:
                self.secondarybar = tqdm(total=qty, colour=self.color, leave=False, desc=txt)

        elif action == "update":
            do_bar = self.masterbar if bar == "master" else self.secondarybar
            if do_bar is None:
                return
            if bar == "secondary":
                if do_bar.n + 1 == do_bar.total and self.masterbar is not None:
                    self.masterbar.update(1)

            do_bar.update(1)
            if do_bar.n == do_bar.total:
                do_bar.close()
