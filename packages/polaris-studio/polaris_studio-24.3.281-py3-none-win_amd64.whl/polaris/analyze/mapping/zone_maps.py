# Copyright (c) 2024, UChicago Argonne, LLC
# BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
import json
from copy import deepcopy
from os.path import dirname, join
from pathlib import Path
from typing import List

import numpy as np
import pandas as pd
from pandas.api.types import is_numeric_dtype
from polaris.analyze.activity_metrics import ActivityMetrics
from polaris.analyze.mapping.utils import network_central_point
from polaris.network.data.data_table_cache import DataTableCache
from polaris.runs.scenario_compression import ScenarioCompression
from polaris.utils.database.db_utils import commit_and_close


class ZoneMap:
    def __init__(self, network_file: Path, demand_file: Path, traffic_scale_factor=1.0):
        self.__dem_file = demand_file
        self.__net_file = network_file
        self.__map = None
        self.__multiplier = 1 / traffic_scale_factor

        self.am = ActivityMetrics(self.__net_file, self.__dem_file)
        self.__data = pd.DataFrame([])

        network_file = ScenarioCompression.maybe_extract(network_file)
        with commit_and_close(network_file, spatial=True) as conn:
            self.geo_zones = DataTableCache(network_file).plotting_layer("zone", conn)

        with open(join(dirname(__file__), "configs", "zone_maps_config.json")) as json_file:
            self.__config = json.load(json_file)
            x, y = network_central_point(self.__net_file)
            self.__config["config"]["mapState"]["longitude"] = float(x)
            self.__config["config"]["mapState"]["latitude"] = float(y)

        self.__tool_tip: List[str] = []
        self.__build_dataset()

    @property
    def map_config(self):
        return deepcopy(self.__config)

    @property
    def stats_variables(self) -> List[str]:
        return self.__data.columns.to_list()

    def set_trip_mode(self, mode_name: str, mode_share=False):
        self.am.set_mode(mode_name, mode_share)

    def set_trip_interval(self, start_time: int, end_time: int):
        self.am.set_start_hour(start_time)
        self.am.set_end_hour(end_time)

    def set_time_period(self, time_period: str):
        self.am.set_time_period(time_period)

    def set_height_variable(self, variable_name: str):
        cnf = {"name": variable_name, "type": "float"}
        self.__config["config"]["visState"]["layers"][0]["visualChannels"]["heightField"] = cnf

    def set_color_variable(self, variable_name: str):
        cnf = {"name": variable_name, "type": "float"}
        self.__config["config"]["visState"]["layers"][0]["visualChannels"]["colorField"] = cnf

    def set_tool_tip(self, list_variables: List[str]):
        self.__tool_tip = list_variables
        self.__format_tooltip()

    def __format_tooltip(self):
        formats = []

        for field in self.__tool_tip:
            assert field in self.stats_variables
            frmt = ""
            if is_numeric_dtype(self.__data[field]):
                frmt = ".1%" if np.max(self.__data[field]) <= 1 else ",.0f"
            formats.append({"name": field, "format": frmt})

        self.__config["config"]["visState"]["interactionConfig"]["tooltip"]["fieldsToShow"]["zones"] = formats

    def __build_dataset(self):
        self.__data = self.geo_zones.join(self.am.get_trips()).reset_index()
        if self.__data.trips.max() > 1.1:
            self.__data["trips"] *= self.__multiplier

    def build_map(self):
        from keplergl import KeplerGl  # type: ignore #missing stubs

        self.__build_dataset()
        self.__format_tooltip()
        self.__map = KeplerGl(height=900, data={"zones": self.__data}, config=self.__config)

        return self.__map
