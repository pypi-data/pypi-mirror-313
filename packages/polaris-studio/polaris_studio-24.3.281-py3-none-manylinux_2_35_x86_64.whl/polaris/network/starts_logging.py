# Copyright (c) 2024, UChicago Argonne, LLC
# BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
import logging


def starts_logging():
    polaris_logger = logging.getLogger("polaris")
    polaris_logger.setLevel(logging.INFO)
    return polaris_logger


logger = starts_logging()
