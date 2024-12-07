# Copyright (c) 2024, UChicago Argonne, LLC
# BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
import sqlite3
from os import PathLike

import shapely.wkb
import shapely.wkt
from shapely.ops import transform

from polaris.network.data.data_table_cache import DataTableCache
from polaris.network.transit.transit_elements.pattern import Pattern


def read_patterns(conn: sqlite3.Connection, transformer, path_to_file: PathLike):
    patterns = []
    data = DataTableCache(path_to_file).get_table("transit_patterns", conn).reset_index()
    if data.empty:
        return
    data.geo = data.geo.apply(shapely.wkb.loads)

    data.drop(columns=["matching_quality"], inplace=True)
    data.rename(columns={"pattern": "pattern_hash", "geo": "shape"}, inplace=True)

    for _, dt in data.iterrows():
        pat = Pattern(None, dt.route_id, None).from_row(dt)
        pat.shape_length = pat.best_shape().length

        if transformer:
            pat.shape = transform(transformer.transform, pat.shape)

        patterns.append(pat)
    return patterns
