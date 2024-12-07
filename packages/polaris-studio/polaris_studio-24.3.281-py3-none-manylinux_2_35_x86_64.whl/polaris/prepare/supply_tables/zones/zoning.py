# Copyright (c) 2024, UChicago Argonne, LLC
# BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
import pygris

from polaris.network.utils.srid import get_srid
from polaris.utils.database.db_utils import commit_and_close
from .population import get_pop


def add_zoning(
    model_area: gpd.GeoDataFrame, state_counties: gpd.GeoDataFrame, zone_level: str, supply_path: Path, year, api_key
):
    """Create zoning system based on census subdivisions

    Args:
        model_area (GeoDataFrame): GeoDataFrame containing polygons with the model area
        zone_level (str): Census subdivision level to use for zoning -> Census tracts or block groups
        supply_path (Path): Path to the supply database we are building
        year (int): Year for which the population should be retrieved for
        api_key (str): Census API key
    """

    data = []
    for _, rec in state_counties.iterrows():
        kwargs = {"state": rec["state_name"], "county": rec["COUNTYFP"], "year": year, "cache": True}
        data.append(pygris.tracts(**kwargs) if zone_level == "tracts" else pygris.block_groups(**kwargs))

    if len(data) == 0:
        raise ValueError("Could not find any US State/county that overlaps the desired modeling area")

    df = pd.concat(data)
    zone_candidates = gpd.GeoDataFrame(df, geometry=data[0]._geometry_column_name, crs=data[0].crs.to_epsg())

    # this is returning None in some case. See: https://pyproj4.github.io/pyproj/stable/gotchas.html#why-does-the-epsg-code-return-when-using-epsg-xxxx-and-not-with-init-epsg-xxxx

    cols = ["zone", "pop_households", "pop_persons", "pop_group_quarters", "percent_white", "percent_black", "wkb_"]
    pop_data = get_pop(zone_level, zone_candidates, year, api_key)

    crs = zone_candidates.crs.to_epsg()
    zone_candidates.GEOID = zone_candidates.GEOID.astype(str)
    zone_candidates = zone_candidates.merge(pop_data, on="GEOID")
    zone_candidates = gpd.GeoDataFrame(zone_candidates, crs=crs, geometry=zone_candidates.geometry)

    model_area = gpd.GeoDataFrame(
        {"__not_keeping_col": np.arange(model_area.shape[0])}, geometry=model_area.geometry.to_crs(zone_candidates.crs)
    )
    cols1 = zone_candidates.columns.tolist()
    a = zone_candidates.sjoin(model_area, how="inner", predicate="intersects")
    zone_candidates = a.loc[a.index.drop_duplicates(keep="first"), :][cols1]

    zone_candidates = zone_candidates.assign(zone=np.arange(zone_candidates.shape[0]) + 1)
    with commit_and_close(supply_path, spatial=True) as conn:
        srid = get_srid(conn=conn)
        zone_candidates = zone_candidates.to_crs(srid)

        zone_candidates = zone_candidates.assign(wkb_=zone_candidates.geometry.to_wkb())
        records = zone_candidates[cols].to_records(index=False)
        c = ",".join(cols[:-1])
        w = ",".join(["?"] * (len(cols) - 1))
        conn.executemany(f"INSERT INTO Zone ({c}, geo) VALUES ({w}, CastToMulti(GeomFromWKB(?, {srid})))", records)
