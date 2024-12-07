# Copyright (c) 2024, UChicago Argonne, LLC
# BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
import ctypes
import os.path
import warnings
from ctypes import c_float, c_longlong, c_int64, POINTER, c_uint32, byref, c_bool, c_int32
from pathlib import Path
from typing import Optional

import numpy as np
from polaris.runs.convergence.convergence_config import ConvergenceConfig
from polaris.runs.router.path_results import PathResults
from polaris.utils.database.db_utils import read_and_close
from polaris.utils.dir_utils import with_dir
from polaris.utils.env_utils import is_windows


class BatchRouter:
    def __init__(self, convergence_config: ConvergenceConfig, supply_file: Optional[Path] = None):
        bin_path = Path(convergence_config.polaris_exe).parent
        dll = "Batch_Router.dll" if is_windows() else "libBatch_Router.so"

        if not os.path.exists(bin_path / dll):
            raise FileNotFoundError(f"{bin_path / dll} is not available")
        with with_dir(bin_path):
            self.__router_dll = ctypes.cdll.LoadLibrary(str(bin_path / dll))
            self.__dll_path = bin_path / dll
        self.__supply_path = supply_file or convergence_config.data_dir / convergence_config.result_file()
        convergence_config: ConvergenceConfig = convergence_config
        self.load_scenario(convergence_config)

    def load_scenario(self, convergence_config: ConvergenceConfig):
        warnings.warn("Loading scenario into the router. This may take some time")
        scen_name = str(convergence_config.scenario_main)
        db_name = convergence_config.db_name

        with with_dir(convergence_config.data_dir):
            self.__router_dll.load(
                f"{db_name}-Demand".encode("utf-8"), f"{db_name}-Result".encode("utf-8"), scen_name.encode("ASCII")
            )

        with read_and_close(convergence_config.data_dir / convergence_config.supply_file()) as conn:
            self.__traffic_links = sum(conn.execute("select 2 * count(*) from link").fetchone())
            self.__pt_links = sum(conn.execute("select count(*) from transit_walk").fetchone())
            self.__pt_links += sum(conn.execute("select count(*) from Transit_Pattern_Links").fetchone())

    def multimodal(self, origin, destination, mode, departure_time=28800) -> PathResults:
        """Computes the multi-modal shortest path between two locations"""

        return self.__route_multimodal(origin, destination, mode, departure_time)

    def route(self, origin, destination, departure_time=28800) -> PathResults:
        """Computes the shortest path between two locations"""

        return self.__route_location(origin, destination, departure_time)

    def route_links(self, link_origin, link_destination, origin_dir=0, destination_dir=0, departure_time=28800):
        """Computes the shortest path between two links"""
        assert origin_dir in (0, 1)
        assert destination_dir in (0, 1)
        return self.__route(2 * link_origin + origin_dir, 2 * link_destination + destination_dir, departure_time)

    def __route(self, link_origin, link_destination, departure_time) -> PathResults:
        """computes the routes between two links"""

        tt = c_float(0)
        num_links = c_int64(self.__traffic_links)
        trajectory = np.zeros(self.__traffic_links, dtype=np.uint32)
        ttimes = np.zeros(self.__traffic_links, dtype=np.float32)
        self.__router_dll.compute_route(
            c_longlong(link_origin),
            c_longlong(link_destination),
            c_int64(departure_time),
            c_bool(True),
            byref(tt),
            ctypes.pointer(num_links),
            trajectory.ctypes.data_as(POINTER(c_uint32)),
            ttimes.ctypes.data_as(POINTER(c_float)),
        )

        travel_time = float(tt.value) if float(tt.value) < 1e30 else np.inf
        directions, trajectory = np.modf(trajectory[: num_links.value] / 2)
        ttimes = ttimes[: num_links.value]
        del num_links, tt

        return PathResults(
            travel_time=travel_time,
            departure=departure_time,
            links=trajectory.astype(int),
            link_directions=np.ceil(directions).astype(int),
            cumulative_time=ttimes,
        )

    def __route_location(self, loc_origin, loc_destination, departure_time) -> PathResults:
        """computes the routes between two locations"""
        tt = c_float(0)
        num_links = c_int64(self.__traffic_links)
        trajectory = np.zeros(self.__traffic_links, dtype=np.uint32)
        ttimes = np.zeros(self.__traffic_links, dtype=np.float32)
        self.__router_dll.compute_location_route(
            c_longlong(loc_origin),
            c_longlong(loc_destination),
            c_int64(departure_time),
            c_bool(True),
            byref(tt),
            ctypes.pointer(num_links),
            trajectory.ctypes.data_as(POINTER(c_uint32)),
            ttimes.ctypes.data_as(POINTER(c_float)),
        )
        travel_time = float(tt.value) if (float(tt.value) < 1e30 and np.count_nonzero(trajectory)) else np.inf
        directions, trajectory = np.modf(trajectory[: num_links.value] / 2)
        ttimes = ttimes[: num_links.value]
        del num_links, tt

        return PathResults(
            travel_time=travel_time,
            departure=departure_time,
            links=trajectory.astype(int),
            link_directions=np.ceil(directions).astype(int),
            cumulative_time=ttimes,
        )

    def __route_multimodal(self, loc_origin, loc_destination, mode, departure_time) -> PathResults:
        """computes the routes between two locations"""

        tt = c_float(0)
        num_links = c_int64(self.__pt_links)
        trajectory = np.zeros(self.__pt_links, dtype=np.uint32)
        ttimes = np.zeros(self.__traffic_links, dtype=np.float32)
        self.__router_dll.compute_multimodal_route(
            c_longlong(loc_origin),
            c_longlong(loc_destination),
            c_int64(departure_time),
            c_int32(mode),
            c_bool(True),
            byref(tt),
            ctypes.pointer(num_links),
            trajectory.ctypes.data_as(POINTER(c_uint32)),
            ttimes.ctypes.data_as(POINTER(c_float)),
        )

        travel_time = float(tt.value) if float(tt.value) < 1e30 else np.inf
        directions, trajectory = np.modf(trajectory[: num_links.value] / 2)
        ttimes = ttimes[: num_links.value]
        del num_links, tt

        return PathResults(
            travel_time=travel_time,
            departure=departure_time,
            links=trajectory.astype(int),
            link_directions=np.ceil(directions).astype(int),
            cumulative_time=ttimes,
        )
