# Copyright (c) 2024, UChicago Argonne, LLC
# BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
from pathlib import Path

import numpy as np
import pandas as pd


def initialize(trip: pd.DataFrame) -> pd.DataFrame:
    # filter dataset for activity choice
    return trip[~trip["WHYTO"].isin([-9, -8, -7, 97, 7])].copy()


def recode(df_tr_activity: pd.DataFrame, df_person: pd.DataFrame) -> pd.DataFrame:
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

    # merge person file
    df_tr_activity = df_tr_activity.merge(
        df_person[["HOUSEID", "PERSONID", "WKFTPT"]], left_on=["HOUSEID", "PERSONID"], right_on=["HOUSEID", "PERSONID"]
    )

    # recode person type
    df_tr_activity["PRESCHOOL"] = np.where(df_tr_activity["R_AGE"] < 5, 1, 0)
    df_tr_activity["SCHOOL_CHILD"] = np.where((df_tr_activity["R_AGE"] >= 5) & (df_tr_activity["R_AGE"] < 16), 1, 0)
    df_tr_activity["STUDENT_DRIVER"] = np.where((df_tr_activity["R_AGE"] >= 16) & (df_tr_activity["R_AGE"] <= 18), 1, 0)
    df_tr_activity["FULLTIME_WORKER"] = np.where(df_tr_activity["WKFTPT"] == 1, 1, 0)
    df_tr_activity["PARTTIME_WORKER"] = np.where(df_tr_activity["WKFTPT"] == 2, 1, 0)
    df_tr_activity["ADULT_STUDENT"] = np.where((df_tr_activity["R_AGE"] >= 18) & (df_tr_activity["PRMACT"] == 5), 1, 0)
    df_tr_activity["SENIOR"] = np.where(df_tr_activity["R_AGE"] >= 65, 1, 0)
    df_tr_activity["NONWORKER"] = np.where(df_tr_activity["WORKER"] == 2, 1, 0)

    # same recoding for person file
    df_person["PRESCHOOL"] = np.where(df_person["R_AGE"] < 5, 1, 0)
    df_person["SCHOOL_CHILD"] = np.where((df_person["R_AGE"] >= 5) & (df_person["R_AGE"] < 16), 1, 0)
    df_person["STUDENT_DRIVER"] = np.where((df_person["R_AGE"] >= 16) & (df_person["R_AGE"] <= 18), 1, 0)
    df_person["FULLTIME_WORKER"] = np.where(df_person["WKFTPT"] == 1, 1, 0)
    df_person["PARTTIME_WORKER"] = np.where(df_person["WKFTPT"] == 2, 1, 0)
    df_person["ADULT_STUDENT"] = np.where((df_person["R_AGE"] >= 18) & (df_person["PRMACT"] == 5), 1, 0)
    df_person["SENIOR"] = np.where(df_person["R_AGE"] >= 65, 1, 0)
    df_person["NONWORKER"] = np.where(df_person["WORKER"] == 2, 1, 0)

    return df_tr_activity, df_person


def get_targets_from_trips(df_tr_activity: pd.DataFrame, df_people: pd.DataFrame) -> pd.DataFrame:
    p_type = [
        "FULLTIME_WORKER",
        "PARTTIME_WORKER",
        "ADULT_STUDENT",
        "SENIOR",
        "NONWORKER",
        "STUDENT_DRIVER",
        "SCHOOL_CHILD",
        "PRESCHOOL",
    ]
    a_type = [
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

    # write results
    data = []
    for i in p_type:
        df_tr_activity_ = df_tr_activity[df_tr_activity[i] == 1]
        df_people_ = df_people[df_people[i] == 1]
        activity_targets = df_tr_activity_.groupby(["ACTIVITY"]).agg(weighted_sum=("WTTRDFIN", "sum"))
        activities_of_interest = activity_targets.index.tolist()
        activity_personsum = df_people_.WTPERFIN.sum()
        for j in a_type:
            if j in activities_of_interest:
                sum = activity_targets.loc[j, "weighted_sum"]
                value = sum / activity_personsum / 365
            else:
                value = 0
            data += [[i, j, value]]
    return pd.DataFrame(data, columns=["pertype", "acttype", "target"])


def write2file(targets: pd.DataFrame, filename: Path):
    targets.to_csv(filename)
