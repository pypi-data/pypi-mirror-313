# Copyright (c) 2024, UChicago Argonne, LLC
# BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
from os import PathLike
from os.path import join

import numpy as np
import pandas as pd
import shapely.wkb
import shapely.wkt
from shapely.ops import transform

from polaris.network.data.data_table_cache import DataTableCache


def export_zones_to_gmns(gmns_folder: str, transformer, conn, path_to_file: PathLike):
    zones = DataTableCache(path_to_file).get_table("Zone", conn=conn).reset_index()
    zones_no_geo = zones[zones.geo.isna()]
    zones = zones[~zones.geo.isna()]
    geometries = [transform(transformer.transform, geo) for geo in zones.geo.apply(shapely.wkb.loads)]
    zones.loc[:, "geo"] = np.array([shapely.wkt.dumps(geo, rounding_precision=6) for geo in geometries])
    zones = pd.concat([zones, zones_no_geo])
    zones.drop(columns=["x", "y", "z", "area"], inplace=True)
    zones.rename(columns={"zone": "zone_id", "geo": "boundary"}, inplace=True)
    zones.to_csv(join(gmns_folder, "zone.csv"), index=False)
