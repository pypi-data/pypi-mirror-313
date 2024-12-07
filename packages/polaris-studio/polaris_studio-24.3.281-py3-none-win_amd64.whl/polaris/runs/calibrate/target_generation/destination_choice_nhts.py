# Copyright (c) 2024, UChicago Argonne, LLC
# BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
import math
from pathlib import Path

import numpy as np
import pandas as pd


def initialize(trip: pd.DataFrame) -> pd.DataFrame:
    # filter dataset for destination choice
    return trip[trip["TRPMILAD"] > 0].copy()


def recode(df_tr_activity: pd.DataFrame):
    # recode activity time and distance
    df_tr_activity["unweighted_time"] = df_tr_activity["ENDTIME"].apply(
        lambda x: math.floor(x / 100) * 60 + x % 100
    ) - df_tr_activity["STRTTIME"].apply(lambda x: math.floor(x / 100) * 60 + x % 100)

    df_tr_activity["weighted_time"] = df_tr_activity["unweighted_time"] * df_tr_activity["WTTRDFIN"]
    df_tr_activity["weighted_distance"] = df_tr_activity["TRPMILAD"] * df_tr_activity["WTTRDFIN"]

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
    return df_tr_activity


def get_targets_from_trips(trips: pd.DataFrame) -> pd.DataFrame:
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
            ]
        )
    ]

    trips = trips.rename(columns={"ACTIVITY": "ACTIVITY_TYPE"})

    destination_choice_targets = trips.groupby(["ACTIVITY_TYPE"]).agg(
        weighted_sum=("WTTRDFIN", "sum"),
        weighted_time_sum=("weighted_time", "sum"),
        weighted_dist_sum=("weighted_distance", "sum"),
    )

    destination_choice_targets["travel_time"] = (
        destination_choice_targets.weighted_time_sum / destination_choice_targets.weighted_sum
    )
    destination_choice_targets["distance"] = (
        destination_choice_targets.weighted_dist_sum / destination_choice_targets.weighted_sum
    )

    destination_choice_targets = destination_choice_targets[["travel_time", "distance"]]
    return destination_choice_targets


def write2file(targets: pd.DataFrame, filename: Path):
    targets.to_csv(filename)
