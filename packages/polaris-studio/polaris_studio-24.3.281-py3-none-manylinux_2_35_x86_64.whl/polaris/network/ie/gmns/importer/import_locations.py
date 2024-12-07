# Copyright (c) 2024, UChicago Argonne, LLC
# BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
from os import PathLike
from os.path import join, isfile

import pandas as pd
import shapely.wkt
from shapely.geometry import Point

from polaris.network.data.data_table_cache import DataTableCache
from polaris.network.utils.srid import get_srid
from polaris.network.ie.gmns.importer.add_land_uses import add_land_uses
from polaris.network.ie.gmns.importer.gmns_field_compatibility import location_field_translation
from polaris.network.ie.gmns.importer.util_functions import add_required_fields, apply_transform
from polaris.network.starts_logging import logger
from polaris.network.tools.geo import Geo


def import_gmns_locations(gmns_folder: str, transformer, conn, path_to_file: PathLike):
    # Thorough documentation of the assumptions used in this code is provided
    # with the package documentation -> Supply/Import-Export/GMNS
    location_file = join(gmns_folder, "location.csv")
    if not isfile(location_file):
        logger.info("No location file to import from GMNS")
        return

    locs = pd.read_csv(location_file)

    locs.rename(columns=location_field_translation, inplace=True, errors="ignore")
    locs.dropna(how="all", axis=1, inplace=True)

    if "x" not in locs or "y" not in locs:
        logger.error("Location file does not have coordinates.  Import through lr/offset not supported")
        return

    if "x" not in locs or "y" not in locs:
        logger.error("Location file does not have coordinates.  Import through lr/offset not supported")
        return

    for table in ["Zone", "Link"]:
        if DataTableCache(path_to_file).get_table(table, conn=conn).empty:
            logger.error(f"We cannot import locations without importing {table} first, and that table is empty")
            return

    locs = locs.assign(geo=[Point(rec.x, rec.y).wkt for _, rec in locs.iterrows()])

    if transformer is not None:
        locs.loc[:, "geo"] = apply_transform(locs, transformer)
    add_land_uses(locs, conn, path_to_file)

    add_required_fields(locs, "location", conn)

    geotool = Geo(path_to_file)
    for idx, rec in locs.iterrows():  # type: ignore
        loc_geo = shapely.wkt.loads(rec.geo)
        locs.at[idx, "zone"] = geotool.get_geo_item("zone", loc_geo)
        lnk = geotool.get_geo_item("link", loc_geo)
        if lnk >= 0:
            locs.loc[[idx], "link"] = lnk

    cols = [str(x) for x in locs.columns]
    cols.remove("geo")
    cols.append("geo")

    param_bindings = f'{",".join(["?"] * (len(cols) - 1))}, GeomFromText(?,{get_srid(conn=conn)})'
    sql = f'INSERT INTO Location ({",".join(cols)}) VALUES({param_bindings})'

    conn.executemany(sql, locs[cols].to_records(index=False))
    conn.commit()
