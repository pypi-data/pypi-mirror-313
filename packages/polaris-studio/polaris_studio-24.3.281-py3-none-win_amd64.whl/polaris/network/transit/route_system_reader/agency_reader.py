# Copyright (c) 2024, UChicago Argonne, LLC
# BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
import sqlite3
from os import PathLike

from polaris.network.data.data_table_cache import DataTableCache
from polaris.network.transit.transit_elements.agency import Agency


def read_agencies(conn: sqlite3.Connection, network_file: PathLike):
    data = DataTableCache(network_file).get_table("transit_agencies", conn).reset_index()
    return [Agency(network_file).from_row(dt) for _, dt in data.iterrows() if dt.agency_id > 1]
