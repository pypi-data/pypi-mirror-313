# Copyright (c) 2024, UChicago Argonne, LLC
# BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
import numpy as np
import pandas as pd
from polaris.runs.results.result_version import get_version_from_handle
from tables import open_file


class H5_Results(object):
    def __init__(self, filename):
        self.filename = filename
        with open_file(self.filename, mode="r") as h5file:
            self.version = get_version_from_handle(h5file)
            self.num_timesteps = h5file.root.link_moe._v_attrs.num_timesteps

        self.num_links = self.get_vector("link_moe", "link_uids").shape[0]
        self.num_turns = self.get_vector("turn_moe", "turn_uids").shape[0]
        self.path_lu = self.load_paths()

    def get_vector(self, group, value):
        with open_file(self.filename, mode="r") as h5file:
            return np.array(h5file.root._f_get_child(group)._f_get_child(value)).flatten()

    def get_array(self, group, table):
        with open_file(self.filename, mode="r") as h5file:
            if group not in h5file.root or table not in h5file.root._f_get_child(group):
                return None
            return np.array(h5file.root._f_get_child(group)._f_get_child(table))

    path_cols = ["path_id", "link_first_index", "link_last_index", "unit_first_index", "unit_last_index"]
    path_link_cols = ["path_id", "link_uuid", "entering_time", "travel_time"]
    path_link_cols += ["energy_consumption", "routed_travel_time"]
    timesteps = [14400, 28800, 43200, 57600, 72000, 86399]

    def load_paths(self):
        def load_timestep(t):
            df = pd.DataFrame(self.get_array("paths", f"path_timestep_{t}"), columns=self.path_cols)
            return df.assign(timestep=t)

        paths = pd.concat([load_timestep(i) for i in self.timesteps])
        return {e["path_id"]: (e["timestep"], e["link_first_index"], e["link_last_index"]) for _, e in paths.iterrows()}

    def get_path_links(self, path_id=None):
        if path_id is not None:
            timestep, first_idx, last_idx = self.path_lu.get(path_id)
            links = self.get_path_links_for_timestep(timestep)
            return links.iloc[first_idx : last_idx + 1]

        return pd.concat([self.get_path_links_for_timestep(t) for t in self.timesteps])

    def get_path_links_for_timestep(self, timestep):
        links = pd.DataFrame(
            data=self.get_array("paths", f"path_links_timestep_{timestep}"), columns=self.path_link_cols
        )
        links["link_id"] = np.floor(links.link_uuid.to_numpy() / 2).astype(int)
        links["link_dir"] = (links.link_uuid.to_numpy() % 2).astype(int)
        links["entering_time"] = links["entering_time"] / 1000.0
        links["travel_time"] = links["travel_time"] / 1000.0
        links["routed_travel_time"] = links["routed_travel_time"] / 1000.0
        return links

    def get_array_v0(self, f, group, table):
        tables = {
            "link_moe": [
                "link_travel_time",
                "link_travel_time_standard_deviation",
                "link_queue_length",
                "link_travel_delay",
                "link_travel_delay_standard_deviation",
                "link_speed",
                "link_density",
                "link_in_flow_rate",
                "link_out_flow_rate",
                "link_in_volume",
                "link_out_volume",
                "link_speed_ratio",
                "link_in_flow_ratio",
                "link_out_flow_ratio",
                "link_density_ratio",
                "link_travel_time_ratio",
                "num_vehicles_in_link",
                "volume_cum_BPLATE",
                "volume_cum_LDT",
                "volume_cum_MDT",
                "volume_cum_HDT",
                "entry_queue_length",
            ],
            "turn_moe": [
                "turn_penalty",
                "turn_penalty_sd",
                "inbound_turn_travel_time",
                "outbound_turn_travel_time",
                "turn_flow_rate",
                "turn_flow_rate_cv",
                "turn_penalty_cv",
                "total_delay_interval",
                "total_delay_interval_cv",
            ],
        }
        return f[group][:, :, tables[group].index(table)].T
