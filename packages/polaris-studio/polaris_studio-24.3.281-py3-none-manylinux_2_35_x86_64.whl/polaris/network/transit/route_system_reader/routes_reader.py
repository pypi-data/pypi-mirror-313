# Copyright (c) 2024, UChicago Argonne, LLC
# BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
import sqlite3
from os import PathLike

from polaris.network.data.data_table_cache import DataTableCache
from polaris.network.transit.transit_elements.route import Route


def read_routes(conn: sqlite3.Connection, path_to_file: PathLike):
    data = DataTableCache(path_to_file).get_table("transit_routes", conn).reset_index()

    data.drop(columns=["seated_capacity", "design_capacity", "total_capacity", "number_of_cars", "geo"], inplace=True)
    data.rename(
        columns={
            "description": "route_desc",
            "longname": "route_long_name",
            "shortname": "route_short_name",
            "type": "route_type",
        },
        inplace=True,
    )
    routes = []

    for _, dt in data.iterrows():
        rt = Route(-1).from_row(dt)
        routes.append(rt)

    return routes
