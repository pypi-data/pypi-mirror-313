# Copyright (c) 2024, UChicago Argonne, LLC
# BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
import logging
from pathlib import Path
from typing import List

import numpy as np
import pandas as pd

from polaris.utils.database.db_utils import read_and_close
from polaris.utils.signals import SIGNAL


class GlobalChecker:
    """Model Checker"""

    checking = SIGNAL(object)

    def __init__(self, polaris_path: Path, supply_file: Path, demand_file: Path):

        self._fldr_path = polaris_path
        self._supply_file = polaris_path / supply_file
        self._demand_file = polaris_path / demand_file
        self.logger = logging.getLogger("polaris")

        self.checks_completed = 0
        self.errors: List[str] = []

    def critical(self):
        """Runs set of tests for issues known to crash Polaris"""

        self._trips_valid_locations()
        self._sf1_locations()

    def _trips_valid_locations(self):
        sql = """SELECT DISTINCT(location) FROM (SELECT DISTINCT(origin) location FROM Trip
                                                  UNION ALL
                                                 SELECT DISTINCT(destination) location FROM Trip )"""

        with read_and_close(self._demand_file) as conn:
            trip_locations = pd.read_sql(sql, conn)
            if trip_locations.empty:
                return
        with read_and_close(self._supply_file) as conn:
            supply_locations = pd.read_sql("SELECT location from Location", conn)

        if trip_locations[~trip_locations.location.isin(supply_locations.location)].empty:
            return

        self.errors.append("Trips refer to locations that do not exist in the supply file")

    def _sf1_locations(self):
        with read_and_close(self._supply_file) as conn:
            sql = """SELECT DISTINCT(census_zone) from Location where land_use IN ('RES', 'MIX', 'ALL', 'RESIDENTIAL-SINGLE', 'RESIDENTIAL-MULTI') """
            supply_locations = pd.read_sql(sql, conn).census_zone.astype(np.int64).to_numpy()

        for sf1_name in ["sf1.csv", "sf1.txt"]:
            sf1_file = self._fldr_path / sf1_name
            if sf1_file.exists():
                break

        if not sf1_file.exists():
            return
        sep = "," if sf1_name.endswith(".csv") else "\t"
        sf1 = pd.read_csv(sf1_file, sep=sep)
        col = sf1.columns[0]
        missing = sf1[~sf1[col].astype(np.int64).isin(supply_locations)]
        if missing.empty:
            return
        logging.warning("There is a census tract with population that has no corresponding residential location")
        self.errors.append("There is a census tract with population that has no corresponding residential location")
        self.errors.append(missing[col].to_list())

    def has_critical_errors(self, fail_on_errors):
        self.critical()
        if len(self.errors) > 0:
            if fail_on_errors:
                self.logger.critical(self.errors)
                raise ValueError("YOUR MODEL CONTAINS CONSISTENCY ERRORS")
            return True
        return False
