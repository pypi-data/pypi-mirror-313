# Copyright (c) 2024, UChicago Argonne, LLC
# BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
from pathlib import Path

import numpy as np
import pandas as pd


def initialize(trip: pd.DataFrame) -> pd.DataFrame:
    # filter dataset for mode choice use
    trip = trip[trip["NUMONTRP"] > 0]
    trip = trip[trip["TRIPPURP"] != "-9"]
    trip = trip[trip["TRPTRANS"] >= 1]
    trip = trip[trip["TRPTRANS"] != 7]
    trip = trip[trip["TRPTRANS"] != 8]
    trip = trip[trip["TRPTRANS"] != 9]
    trip = trip[trip["TRPTRANS"] != 97]
    return trip.copy()


def recode(df_tr: pd.DataFrame):
    # recode the weight to be vehicle weight
    df_tr["new_weight"] = df_tr.apply(lambda row: row.WTTRDFIN / row.NUMONTRP, axis=1)

    # recode trip purpose
    df_tr["TRIPPURP"] = df_tr["TRIPPURP"].apply(lambda x: "HBO" if (x == "HBSHOP" or x == "HBSOCREC") else x)

    # recode mode choice
    df_tr["TRPTRANS"] = df_tr["TRPTRANS"].apply(lambda x: "WALK" if x == 1 else x)
    df_tr["TRPTRANS"] = df_tr["TRPTRANS"].apply(lambda x: "BIKE" if x == 2 else x)
    df_tr["TRPTRANS"] = df_tr["TRPTRANS"].apply(
        lambda x: "TRANSIT" if (x == 10 or x == 11 or x == 12 or x == 13 or x == 14 or x == 19 or x == 20) else x
    )
    df_tr["TRPTRANS"] = df_tr["TRPTRANS"].apply(lambda x: "TAXI" if x == 17 else x)
    df_tr["TRPTRANS"] = df_tr["TRPTRANS"].apply(
        lambda x: "AUTO" if (x == 3 or x == 4 or x == 5 or x == 6 or x == 18) else x
    )
    df_tr["TRPTRANS"] = df_tr["TRPTRANS"].apply(lambda x: "RAIL" if (x == 15 or x == 16) else x)
    df_tr["TRPTRANS"] = np.where(
        (df_tr["TRPTRANS"] == "AUTO") & (df_tr["NUMONTRP"] != 1), "AUTO-PASS", df_tr["TRPTRANS"]
    )
    return df_tr


def get_targets_from_trips(trips: pd.DataFrame) -> pd.DataFrame:
    # filter to only the modes and purposes we care about
    trips = trips[trips.TRPTRANS.isin(["AUTO", "AUTO-PASS", "WALK", "BIKE", "TAXI", "TRANSIT"])]
    trips = trips[trips.TRIPPURP.isin(["HBO", "HBW", "NHB", "total"])]

    df = trips.groupby(["TRPTRANS", "TRIPPURP"])["new_weight"].sum()
    data = df.reset_index().pivot(columns=["TRPTRANS"], index=["TRIPPURP"], values="new_weight").fillna(0)
    data.loc["total"] = data.sum()
    data = data.div(data.sum(axis=1), axis=0)
    data = data.rename_axis(None).reset_index().rename(columns={"index": "TYPE"})
    return data


def write2file(targets: pd.DataFrame, filename: Path):
    targets.to_csv(filename, index=False)
