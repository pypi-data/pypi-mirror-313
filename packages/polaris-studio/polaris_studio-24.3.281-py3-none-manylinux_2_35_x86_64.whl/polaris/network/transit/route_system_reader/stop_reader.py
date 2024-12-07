# Copyright (c) 2024, UChicago Argonne, LLC
# BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
import sqlite3
from os import PathLike
from typing import List

import shapely.wkb

from polaris.network.data.data_table_cache import DataTableCache
from polaris.network.transit.transit_elements.stop import Stop


def read_stops(conn: sqlite3.Connection, transformer, path_to_file: PathLike) -> List[Stop]:
    data = DataTableCache(path_to_file).get_table("transit_stops", conn).reset_index()
    data = data[data.agency_id > 1]
    data.geo = data.geo.apply(shapely.wkb.loads)
    if transformer:
        lons, lats = transformer.transform(data.X.values, data.Y.values)
        data.loc[:, "X"] = lons[:]
        data.loc[:, "Y"] = lats[:]

    data.drop(columns=["moved_by_matching", "Z"], inplace=True)
    data.rename(
        columns={
            "description": "stop_desc",
            "name": "stop_name",
            "street": "stop_street",
            "transit_zone_id": "zone_id",
            "Y": "stop_lat",
            "X": "stop_lon",
        },
        inplace=True,
    )

    return [Stop(-1).from_row(dt) for _, dt in data.iterrows()]
