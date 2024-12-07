# Copyright (c) 2024, UChicago Argonne, LLC
# BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
from os import PathLike
from os.path import join

import pandas as pd

from polaris.network.data.data_table_cache import DataTableCache


def export_locations_to_gmns(gmns_folder: str, transformer, conn, path_to_file: PathLike):
    locs = DataTableCache(path_to_file).get_table("Location", conn=conn).reset_index()
    lons, lats = transformer.transform(locs[:]["x"], locs[:]["y"])

    locs.loc[:, "x"] = lons[:]
    locs.loc[:, "y"] = lats[:]

    locs.rename(
        columns={
            "location": "loc_id",
            "x": "x_coord",
            "y": "y_coord",
            "link": "link_id",
            "offset": "lr",
            "land_use": "loc_type",
            "zone": "zone_id",
        },
        inplace=True,
    )

    links = pd.read_sql("Select link link_id, node_a ref_node_id from Link", conn)

    locs = locs.merge(links, on="link_id", how="left")

    cols = ["loc_id", "link_id", "ref_node_id", "lr", "x_coord", "y_coord", "loc_type", "zone_id"]

    locs.loc[:, "link_id"] = 2 * locs.link_id + locs["dir"]
    locs[cols].to_csv(join(gmns_folder, "location.csv"), index=False)
