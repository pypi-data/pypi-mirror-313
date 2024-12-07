# Copyright (c) 2024, UChicago Argonne, LLC
# BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
from os import PathLike

from polaris.network.data.data_table_cache import DataTableCache


def add_land_uses(locations, conn, path_to_file: PathLike):
    # Thorough documentation of the assumptions used in this code is provided
    # with the package documentation
    clu = DataTableCache(path_to_file).get_table("Land_Use", conn=conn).reset_index()

    land_uses = locations["land_use"].unique()
    adds = [luse for luse in land_uses if luse not in clu.land_use.values]
    if not adds:
        return

    data = [[luse, 1, 1, 1, 1, "From GMNS"] for luse in adds]
    sql = """INSERT INTO Land_Use(land_use, is_home, is_work, is_school, is_discretionary, notes)
                         VALUES(?, ?, ?, ?, ?, ?)"""
    conn.executemany(sql, data)
    conn.commit()
