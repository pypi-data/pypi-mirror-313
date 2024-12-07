# Copyright (c) 2024, UChicago Argonne, LLC
# BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
import json
from pathlib import Path

import yaml


def from_file(model_cls, file):
    file = Path(file)
    if file.suffix.lower() in [".yaml", ".yml"]:
        return from_yaml_file(model_cls, file)
    if file.suffix.lower() in [".json", ".jsn"]:
        return from_json_file(model_cls, file)
    raise NotImplementedError(f"Don't know how to handle file {file}")


def from_json_file(model_cls, file):
    with open(file, "r") as f:
        return model_cls(**json.loads(f.read()))


def from_yaml_file(model_cls, file):
    with open(file, "r") as f:
        return model_cls(**yaml.load(f, Loader=yaml.FullLoader))


def is_x_iteration(first: int, last: int, step: int, i):
    i_ = i - first
    return i >= first and i <= last and i_ % step == 0
