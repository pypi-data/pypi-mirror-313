# Copyright (c) 2024, UChicago Argonne, LLC
# BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
from os.path import join

import pandas as pd
from shapely.geometry import Point

from polaris.network.utils.srid import get_srid
from polaris.network.ie.gmns.importer.gmns_field_compatibility import node_field_translation
from polaris.network.ie.gmns.importer.util_functions import add_required_fields, apply_transform


def import_gmns_nodes(gmns_folder: str, transformer, conn):
    proj_crs = get_srid(conn=conn)
    node_file = join(gmns_folder, "node.csv")

    # We import nodes
    nodes = pd.read_csv(node_file)

    # Fields that are completely empty don't need to be imported
    nodes.dropna(how="all", axis=1, inplace=True)

    # We rename the fields to be compatible with Polaris
    nodes.rename(columns=node_field_translation, inplace=True, errors="ignore")

    nodes = nodes.assign(geo=[Point(rec.x, rec.y).wkt for _, rec in nodes.iterrows()])
    if transformer is not None:
        nodes.loc[:, "geo"] = apply_transform(nodes, transformer)

    add_required_fields(nodes, "node", conn)

    data_cols = [str(x) for x in list(nodes.columns)]
    data_cols.remove("geo")
    param_bindings = ",".join(["?"] * len(data_cols)) + f",GeomFromText(?, {proj_crs})"
    data_cols.append("geo")
    sql = f"INSERT INTO node({','.join(data_cols)}) VALUES({param_bindings})"

    conn.executemany(sql, nodes[data_cols].to_records(index=False))
    conn.commit()
