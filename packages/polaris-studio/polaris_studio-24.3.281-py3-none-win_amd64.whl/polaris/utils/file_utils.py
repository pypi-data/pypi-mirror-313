# Copyright (c) 2024, UChicago Argonne, LLC
# BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
from pathlib import Path

import pandas as pd


def readlines(filename):
    with open(filename, "r") as f:
        return [x.rstrip() for x in f.readlines()]


read_lines = readlines


def read_file(filename):
    with open(filename, "r") as f:
        return f.read()


def replace_in_file(file, pattern, replacement):
    file = Path(file)
    file.write_text(file.read_text().replace(pattern, replacement))


def find_relative(fname, to_dir):
    for f in [Path(fname), Path(to_dir) / fname]:
        if f.exists():
            return f
    raise FileNotFoundError(f"Can't find file {fname} relative to directory {to_dir}")


def df_to_file(df: pd.DataFrame, fname: Path, **kwargs):
    if "index" not in kwargs:
        kwargs["index"] = False
    suffix = fname.suffix.lower()
    if suffix == ".csv":
        df.to_csv(fname, **kwargs)
    elif suffix == ".parquet":
        df.to_parquet(fname, **kwargs)
    elif suffix in [".h5", ".hdf5"]:
        if "key" not in kwargs:
            kwargs["key"] = fname.stem
        if "complevel" not in kwargs:
            kwargs["complevel"] = 5
        df.to_hdf(fname, **kwargs)
    elif suffix == ".zip":
        csv_file = fname.stem + ".csv"
        df.to_csv(fname, compression={"method": "zip", "archive_name": csv_file}, **kwargs)
    else:
        raise RuntimeError(f"Don't know how to save a dataframe to a {suffix} file")


def df_from_file(fname: Path, **kwargs):
    suffix = fname.suffix.lower()
    if suffix == ".csv":
        return pd.read_csv(fname, **kwargs)
    elif suffix == ".parquet":
        if "low_memory" in kwargs:  # read_parquet doesn't support low memory mode
            del kwargs["low_memory"]
        return pd.read_parquet(fname, **kwargs)
    elif suffix in [".h5", ".hdf5"]:
        return pd.read_hdf(fname, **kwargs)
    elif suffix == ".zip":
        return pd.read_csv(fname, **kwargs)
    else:
        raise RuntimeError(f"Don't know how to read a dataframe from a {suffix} file")
