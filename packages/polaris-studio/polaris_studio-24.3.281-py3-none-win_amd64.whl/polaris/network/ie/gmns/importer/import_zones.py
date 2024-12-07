# Copyright (c) 2024, UChicago Argonne, LLC
# BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
from os.path import join, isfile

import pandas as pd

from polaris.network.utils.srid import get_srid
from polaris.network.ie.gmns.importer.gmns_field_compatibility import zone_field_translation
from polaris.network.ie.gmns.importer.util_functions import apply_transform, add_required_fields


def import_gmns_zones(gmns_folder: str, transformer, conn):
    zone_file = join(gmns_folder, "zone.csv")

    if not isfile(zone_file):
        return

    # We import zones
    zones = pd.read_csv(zone_file)

    # Fields that are completely empty don't need to be imported
    zones.dropna(how="all", axis=1, inplace=True)

    if "boundary" not in zones:
        return

    # We rename the fields to be compatible with Polaris
    zones.rename(columns=zone_field_translation, inplace=True, errors="ignore")

    if transformer is not None:
        zones.loc[:, "geo"] = apply_transform(zones, transformer)

    add_required_fields(zones, "zone", conn)
    # We check if we are importing from an OSM network and if we should keep the IDs
    data_cols = [str(c) for c in zones.columns if c != "geo"]
    cols = ",".join(data_cols) + ",geo"
    param_bindings = ",".join(["?"] * len(data_cols)) + ",GeomFromText(?, ?)"
    sql = f"INSERT INTO zone({cols}) VALUES({param_bindings})"

    zones = zones.assign(srid=get_srid(conn=conn))
    data_cols.extend(["geo", "srid"])
    zones = zones[data_cols]

    conn.executemany(sql, zones[data_cols].to_records(index=False))
    conn.commit()
