# Copyright (c) 2024, UChicago Argonne, LLC
# BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
from pathlib import Path

import numpy as np
import pandas as pd


def initialize(trip: pd.DataFrame) -> pd.DataFrame:
    # filter dataset for mode choice use
    return trip[~trip["WHYTO"].isin([-9, -8, -7, 97, 7])].copy()


def recode(df_tr_activity: pd.DataFrame):
    # recode activity
    df_tr_activity["ACTIVITY"] = np.where(df_tr_activity["WHYTO"] == 1, "HOME", "UNKNOWN")
    df_tr_activity["ACTIVITY"] = np.where(df_tr_activity["WHYTO"] == 4, "WORK_PART", df_tr_activity["ACTIVITY"])
    df_tr_activity["ACTIVITY"] = np.where(df_tr_activity["WHYTO"] == 6, "PICKUP", df_tr_activity["ACTIVITY"])
    df_tr_activity["ACTIVITY"] = np.where(df_tr_activity["WHYTO"] == 19, "RELIGIOUS", df_tr_activity["ACTIVITY"])
    df_tr_activity["ACTIVITY"] = np.where(df_tr_activity["WHYTO"] == 8, "SCHOOL", df_tr_activity["ACTIVITY"])
    df_tr_activity["ACTIVITY"] = np.where(df_tr_activity["WHYTO"] == 5, "SERVICE", df_tr_activity["ACTIVITY"])
    df_tr_activity["ACTIVITY"] = np.where(df_tr_activity["WHYTO"] == 11, "SHOP_MAJOR", df_tr_activity["ACTIVITY"])
    df_tr_activity["ACTIVITY"] = np.where(df_tr_activity["WHYTO"] == 12, "SHOP_OTHER", df_tr_activity["ACTIVITY"])
    df_tr_activity["ACTIVITY"] = np.where(df_tr_activity["WHYTO"] == 17, "SOCIAL", df_tr_activity["ACTIVITY"])
    df_tr_activity["ACTIVITY"] = np.where(df_tr_activity["WHYTO"] == 15, "LEISURE", df_tr_activity["ACTIVITY"])
    df_tr_activity["ACTIVITY"] = np.where(df_tr_activity["WHYTO"] == 3, "WORK", df_tr_activity["ACTIVITY"])
    df_tr_activity["ACTIVITY"] = np.where(df_tr_activity["WHYTO"] == 2, "WORK_HOME", df_tr_activity["ACTIVITY"])
    df_tr_activity["ACTIVITY"] = np.where(df_tr_activity["WHYTO"] == 14, "ERRANDS", df_tr_activity["ACTIVITY"])
    df_tr_activity["ACTIVITY"] = np.where(
        (df_tr_activity["WHYTO"] == 9) | (df_tr_activity["WHYTO"] == 10) | (df_tr_activity["WHYTO"] == 16),
        "PERSONAL",
        df_tr_activity["ACTIVITY"],
    )
    df_tr_activity["ACTIVITY"] = np.where(df_tr_activity["WHYTO"] == 18, "HEALTHCARE", df_tr_activity["ACTIVITY"])
    df_tr_activity["ACTIVITY"] = np.where(df_tr_activity["WHYTO"] == 13, "EAT_OUT", df_tr_activity["ACTIVITY"])

    # recode departure time
    df_tr_activity["DEPARTURE"] = np.where(
        (df_tr_activity["STRTTIME"] >= 0) & (df_tr_activity["STRTTIME"] < 600), "NIGHT", "UNKNOWN"
    )
    df_tr_activity["DEPARTURE"] = np.where(
        (df_tr_activity["STRTTIME"] >= 600) & (df_tr_activity["STRTTIME"] < 900), "AMPEAK", df_tr_activity["DEPARTURE"]
    )
    df_tr_activity["DEPARTURE"] = np.where(
        (df_tr_activity["STRTTIME"] >= 900) & (df_tr_activity["STRTTIME"] < 1200),
        "AMOFFPEAK",
        df_tr_activity["DEPARTURE"],
    )
    df_tr_activity["DEPARTURE"] = np.where(
        (df_tr_activity["STRTTIME"] >= 1200) & (df_tr_activity["STRTTIME"] < 1600),
        "PMOFFPEAK",
        df_tr_activity["DEPARTURE"],
    )
    df_tr_activity["DEPARTURE"] = np.where(
        (df_tr_activity["STRTTIME"] >= 1600) & (df_tr_activity["STRTTIME"] < 1900),
        "PMPEAK",
        df_tr_activity["DEPARTURE"],
    )
    df_tr_activity["DEPARTURE"] = np.where(
        (df_tr_activity["STRTTIME"] >= 1900) & (df_tr_activity["STRTTIME"] <= 2359),
        "EVENING",
        df_tr_activity["DEPARTURE"],
    )

    return df_tr_activity


def get_targets_from_trips(trips: pd.DataFrame) -> pd.DataFrame:
    # filter to only the time and activity we care about
    trips = trips[trips.DEPARTURE.isin(["NIGHT", "AMPEAK", "AMOFFPEAK", "PMOFFPEAK", "PMPEAK", "EVENING"])]
    trips = trips[
        trips.ACTIVITY.isin(
            [
                "EAT_OUT",
                "ERRANDS",
                "HEALTHCARE",
                "LEISURE",
                "PERSONAL",
                "RELIGIOUS",
                "SERVICE",
                "SHOP_MAJOR",
                "SHOP_OTHER",
                "SOCIAL",
                "WORK",
                "WORK_PART",
                "WORK_HOME",
                "SCHOOL",
                "PICKUP",
                "HOME",
                "TOTAL",
            ]
        )
    ]

    df = trips.groupby(["DEPARTURE", "ACTIVITY"])["WTTRDFIN"].sum()

    data = df.reset_index().pivot(columns=["DEPARTURE"], index=["ACTIVITY"], values="WTTRDFIN").fillna(0)
    data.loc["TOTAL"] = data.sum()
    data = data.div(data.sum(axis=1), axis=0)
    data = data.T.rename_axis(None).reset_index().rename(columns={"index": "PERIOD"})
    return data


def write2file(targets: pd.DataFrame, filename: Path):
    targets.to_csv(filename, index=False)
