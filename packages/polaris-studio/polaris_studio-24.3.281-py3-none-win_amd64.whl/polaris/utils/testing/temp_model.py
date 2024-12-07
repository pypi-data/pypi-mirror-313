# Copyright (c) 2024, UChicago Argonne, LLC
# BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
import shutil
import tempfile
from pathlib import Path

from polaris import Polaris
from polaris.utils.env_utils import is_windows


def TempModel(model_name):
    fldr = f"C:/temp_container/{model_name}" if is_windows() else f"/tmp/{model_name}"
    new_fldr = tempfile.mkdtemp()
    shutil.copytree(fldr, new_fldr, dirs_exist_ok=True)

    Polaris.from_dir(Path(new_fldr)).upgrade()
    return Path(new_fldr)
