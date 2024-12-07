# Copyright (c) 2024, UChicago Argonne, LLC
# BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
import datetime
import inspect
import logging
import sys
from functools import wraps
from os.path import dirname
from pathlib import Path
from typing import List, Optional

from polaris.utils.dir_utils import mkdir_p

FORMATTER = logging.Formatter("%(asctime)s;%(levelname)s ; %(message)s", datefmt="%H:%M:%S:")


def function_logging(msg):
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            # format all arguments into a dictionary by argument name, including default arguments
            args_dict = inspect.getcallargs(function, *args, **kwargs)
            formatted_msg = msg.format(**args_dict)
            start_time = datetime.datetime.now()
            logging.info(formatted_msg)
            rv = function(*args, **kwargs)
            logging.info(f"{formatted_msg}: Done in {datetime.datetime.now() - start_time} seconds")
            return rv

        return wrapper

    return decorator


def add_file_handler(logger, logging_level, log_path: Path):
    remove_file_handler(logger, "LOGFILE")
    log_path = log_path / "polaris.log"

    mkdir_p(dirname(log_path))
    ch = logging.FileHandler(log_path)
    ch.setFormatter(FORMATTER)
    ch.set_name("LOGFILE")
    ch.setLevel(logging_level)
    logger.addHandler(ch)


def remove_file_handler(logger, handler_name):
    for h in [h for h in logger.handlers if h.name and handler_name == h.name]:
        h.close()
        logger.removeHandler(h)


def has_named_handler(logger: logging.Logger, handler_name: str):
    return len([h for h in logger.handlers if h.name and handler_name == h.name]) > 0


def ensure_stdout_handler(logger, logging_level):
    if has_named_handler(logger, "stdout"):
        return
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging_level)
    stdout_handler.setFormatter(FORMATTER)
    stdout_handler.set_name("stdout")
    logger.addHandler(stdout_handler)


def stdout_logging(also_to_file: Optional[Path] = None):
    handlers: List[logging.Handler] = [logging.StreamHandler(sys.stdout)]
    if also_to_file:
        handlers.append(logging.FileHandler(also_to_file))
    logging.basicConfig(
        handlers=handlers,
        format="%(asctime)s %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S%z",
        level=logging.INFO,
        force=True,
    )
