# Copyright (c) 2024, UChicago Argonne, LLC
# BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
import os

os.environ["USE_PYGEOS"] = "0"

from warnings import filterwarnings  # noqa: E402

filterwarnings(action="ignore", message="invalid value encountered in line_locate_point")

from polaris.project.polaris import Polaris  # noqa: E402, F401
from .version import __version__ as version  # noqa: E402, F401
