# Copyright (c) 2024, UChicago Argonne, LLC
# BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
import sqlite3
from math import log10, floor
from os import PathLike

import pandas as pd

from polaris.network.data.data_table_cache import DataTableCache
from polaris.network.starts_logging import logger
from polaris.network.traffic.intersec import Intersection


def fix_connections_table(
    conn_tbl: pd.DataFrame, map_matching: pd.DataFrame, conn: sqlite3.Connection, path_to_file: PathLike
):
    data_tables = DataTableCache(path_to_file)
    max_link = conn.execute("select max(link) from link").fetchone()[0]

    def build_key(df, max_link):
        multiplier = floor(log10(max_link)) + 3
        multiplier = pow(10, multiplier)
        key = df.link * multiplier + df.dir * (multiplier / 10) + df.to_link * 10 + df.to_dir
        return key

    conn_tbl = conn_tbl.assign(datakey=build_key(conn_tbl, max_link))

    map_matching.sort_values(by=["pattern_id", "index"], inplace=True)
    map_matching = map_matching.assign(
        to_link=map_matching.link.shift(-1),
        to_dir=map_matching.dir.shift(-1),
        to_pattern_id=map_matching.pattern_id.shift(-1),
    )
    map_matching = map_matching[map_matching.pattern_id == map_matching.to_pattern_id]
    map_matching.to_link = map_matching.to_link.astype(int)
    map_matching.to_dir = map_matching.to_dir.astype(int)
    map_matching = map_matching[(map_matching.link != map_matching.to_link) | (map_matching.dir != map_matching.to_dir)]
    map_matching = map_matching.assign(datakey=build_key(map_matching, max_link))

    missing_db = map_matching.loc[~map_matching.datakey.isin(conn_tbl.datakey)]
    if missing_db.empty:
        return
    conn_tbl = conn_tbl.assign(nodekey=10 * conn_tbl.link + conn_tbl.dir)
    missing_db = missing_db.assign(nodekey=10 * missing_db.link + missing_db.dir)
    missing_db = missing_db.merge(conn_tbl[["nodekey", "node"]], on="nodekey")
    missing_db = missing_db.drop_duplicates(subset=["link", "dir", "to_link", "to_dir"], ignore_index=True)
    if missing_db.empty:
        return
    logger.info(f"Adding {missing_db.shape[0]:,} new connections")
    for node in missing_db.node.unique():  # type: int
        df = missing_db[missing_db.node == node]
        intersec = Intersection(data_tables, path_to_file)
        intersec.load(int(node), conn)
        for _, rec in df.iterrows():
            intersec.add_movement(rec.link, rec.to_link, note="required_by_pt_map_matching", conn=conn)
