# Copyright (c) 2024, UChicago Argonne, LLC
# BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
from copy import deepcopy
from os import PathLike
from typing import List

import numpy as np
import pandas as pd

from polaris.analyze.demand_table_metrics import DemandTableMetrics
from polaris.runs.scenario_compression import ScenarioCompression
from polaris.utils.database.db_utils import read_and_close


class TripMetrics(DemandTableMetrics):
    """Loads all data required for the computation of metrics on vehicle Trips.

    The behavior of time filtering consists of setting to instant zero
    whenever *from_time* is not provided and the end of simulation when
    *to_time* is not provided"""

    def __init__(self, supply_file: PathLike, demand_file: PathLike):
        """
        :param supply_file: Path to the supply file corresponding to the demand file we will compute metrics for
        :param demand_file: Path to the demand file we want to compute metrics for
        """
        super().__init__(supply_file, demand_file)
        self.__start = 0
        self.__end = 24
        self.__data = pd.DataFrame([])
        self.__all_modes: List[str] = []
        self.__all_types: List[str] = []
        self.__modes = {
            0: "SOV_0",
            9: "TAXI_9",
            17: "MD_TRUCK_17",
            18: "HD_TRUCK_18",
            19: "BPLATE_19",
            20: "LD_TRUCK_20",
        }

    @property
    def modes(self):
        if not self.__all_modes:
            self.__all_modes = ["ALL"] + self.data["tmode"].unique().tolist()
        return deepcopy(self.__all_modes)

    @property
    def artificial_trips(self):
        if not self.__all_types:
            self.__all_types = ["ALL"] + self.data["has_artificial_trip"].unique().tolist()
        return deepcopy(self.__all_types)

    @property
    def data(self) -> pd.DataFrame:
        if not self.__data.empty:
            return self.__data

        sql = """Select trip_id,
                    path,
                    mode as tmode,
                    start tstart,
                    end tend,
                    origin,
                    destination,
                    has_artificial_trip,
                    routed_travel_time,
                    travel_distance,
                    0 absolute_gap
                    from Trip
                    WHERE (mode = 0 or mode = 9 or mode = 17 or mode = 18 or mode = 19 or mode = 20)
                    AND has_artificial_trip <> 1
                    """

        ScenarioCompression.maybe_extract(self.__demand_file__)
        with read_and_close(self.__demand_file__) as conn:
            fac = conn.execute("SELECT infovalue from About_Model where infoname=='abs_pop_sample_rate'").fetchone()
            if fac:
                sql += " AND end > start AND routed_travel_time > 0"
            trips = pd.read_sql(sql, conn)
        trips.fillna({"tend": 0, "routed_travel_time": 0, "tstart": 0}, inplace=True)
        trips["absolute_gap"] = trips.absolute_gap.astype(np.float64)
        trips.loc[trips.has_artificial_trip == 0, "absolute_gap"] = abs(
            trips.tend - trips.tstart - trips.routed_travel_time
        )
        trips.loc[trips.has_artificial_trip == 2, "absolute_gap"] = 2 * trips.routed_travel_time
        trips.loc[trips.has_artificial_trip.isin([3, 4]), "absolute_gap"] = (
            trips.tend - trips.tstart - trips.routed_travel_time
        )

        trips.loc[trips.absolute_gap < 0, "absolute_gap"] = 0
        trips = trips.assign(hstart=(trips.tstart / 3600).astype(int), hend=(trips.tend / 3600).astype(int))
        self.__data = trips.assign(mstart=(trips.tstart / 60).astype(int), mend=(trips.tend / 60).astype(int))
        return self.__data

    def vehicle_trip_matrix(self, from_start_time: float, to_start_time: float):
        """Returns the trip matrix for the UNIVERSE of trips starting between *from_start_time* and *to_start_time*,
        according to the results of the simulation seen in the *Trips* table"""
        dt = self.data
        dt = dt[(dt.tstart >= from_start_time) & (dt.tstart <= to_start_time)]
        return self._build_matrices(dt, self.__modes)
