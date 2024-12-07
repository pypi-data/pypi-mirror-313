# Copyright (c) 2024, UChicago Argonne, LLC
# BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
import csv
from os import PathLike
from os.path import join

import pandas as pd

from polaris.network.data.data_table_cache import DataTableCache


def write_fares(folder_path: str, conn, path_to_file: PathLike):
    fattr = DataTableCache(path_to_file).get_table("Transit_Fare_Attributes", conn).reset_index()
    fattr.rename(columns={"currency": "currency_type", "transfer": "transfers"}, inplace=True)
    fattr.transfer_duration = fattr.transfer_duration.astype(int)

    headers = ["fare_id", "price", "currency_type", "payment_method", "transfers", "agency_id", "transfer_duration"]

    fattr[headers].to_csv(join(folder_path, "fare_attributes.txt"), quoting=csv.QUOTE_NONNUMERIC, index=False)

    frls = DataTableCache(path_to_file).get_table("Transit_Fare_Rules", conn).reset_index()
    cols = [str(fld) for fld in list(frls.columns) if "id" not in str(fld)]
    frls.rename(columns={fld: f"{fld}_id" for fld in cols}, inplace=True)
    frls = frls[["fare_id", "route_id", "origin_id", "destination_id", "contains_id"]]

    for fld in ["origin_id", "destination_id"]:
        frls[fld] = frls[fld].fillna(value=-99999.0)
        frls[fld] = frls[fld].astype(int).astype(str)
        frls.loc[frls[fld] == "-99999", fld] = pd.NA  # type: ignore
    frls.to_csv(join(folder_path, "fare_rules.txt"), quoting=csv.QUOTE_NONNUMERIC, index=False)
