# Copyright (c) 2024, UChicago Argonne, LLC
# BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
from os import PathLike
from os.path import join

from polaris.network.data.data_table_cache import DataTableCache


def export_nodes_to_gmns(gmns_folder: str, transformer, conn, path_to_file: PathLike):
    nodes = DataTableCache(path_to_file).get_table("Node", conn=conn).reset_index()
    lons, lats = transformer.transform(nodes[:]["x"], nodes[:]["y"])

    nodes.loc[:, "x"] = lons[:]
    nodes.loc[:, "y"] = lats[:]

    nodes.rename(columns={"node": "node_id", "x": "x_coord", "y": "y_coord", "zone": "zone_id"}, inplace=True)
    nodes.rename(columns={"control_type": "ctrl_type"}, inplace=True)
    nodes.loc[nodes.ctrl_type == "stop_sign", "ctrl_type"] = "stop"
    nodes.loc[nodes.ctrl_type == "all_stop", "ctrl_type"] = "4_stop"
    nodes.drop(columns=["geo"], inplace=True)
    nodes.to_csv(join(gmns_folder, "node.csv"), index=False)
