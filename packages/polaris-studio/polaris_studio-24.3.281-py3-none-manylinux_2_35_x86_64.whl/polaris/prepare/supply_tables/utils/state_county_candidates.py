# Copyright (c) 2024, UChicago Argonne, LLC
# BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
import geopandas as gpd
import pandas as pd
import pygris


def get_state_counties(model_area: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    states = pygris.states(cache=True)
    model_area = model_area.to_crs(states.crs)
    union = model_area.union_all()

    states_in_model_area = states[states.geometry.intersects(union)].NAME.tolist()

    data = []
    for state in states_in_model_area:
        counties = pygris.counties(state, cache=True).assign(state_name=state)
        data.append(counties[counties.intersects(union)])
    return pd.concat(data) if data else None
