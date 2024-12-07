# Copyright (c) 2024, UChicago Argonne, LLC
# BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
import sqlite3
from os import PathLike

import pandas as pd

from polaris.network.data.data_table_cache import DataTableCache
from polaris.network.transit.transit_elements.trip import Trip


def read_trips(conn: sqlite3.Connection, path_to_file: PathLike):
    data = DataTableCache(path_to_file).get_table("transit_trips", conn).reset_index()
    data.drop(columns=["seated_capacity", "design_capacity", "total_capacity", "is_artic"], inplace=True)
    data.drop(columns=["number_of_cars"], inplace=True)

    pats = pd.read_sql("Select pattern_id, route_id from Transit_Patterns", conn)
    data = data.merge(pats, on="pattern_id")
    data.trip = data.trip.astype(str)
    data.rename(
        columns={
            "trip": "trip_headsign",
            "dir": "direction_id",
            "pattern_id": "shape_id",
        },
        inplace=True,
    )
    data = data.assign(service_id=data.shape_id)
    return [Trip().from_row(dt) for _, dt in data.iterrows()]
