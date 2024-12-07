# Copyright (c) 2024, UChicago Argonne, LLC
# BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
import os
from pathlib import Path
from typing import List, Any, Optional

import numpy as np
import pandas as pd
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components

from polaris.network.checker.checks.connection_table import CheckConnectionTable
from polaris.network.starts_logging import logger
from polaris.utils.database.db_utils import read_and_close
from polaris.utils.database.standard_database import DatabaseType
from polaris.utils.model_checker import ModelChecker
from polaris.utils.signals import SIGNAL


class SupplyChecker(ModelChecker):
    """Network checker

    ::

        # We open the network
        from polaris.network.network import Network
        n = Network()
        n.open(source)

        # We get the checker for this network
        checker = n.checker

        # We can run the critical checks (those that would result in model crashing)
        checker.critical()

        # The auto network connectivity
        checker.connectivity_auto()

        # The connections table
        checker.connections_table()

    """

    checking = SIGNAL(object)

    def __init__(self, database_path: os.PathLike):
        ModelChecker.__init__(self, DatabaseType.Supply, Path(__file__).parent.absolute(), database_path)

        self._path_to_file = database_path
        self.logger = logger
        self.__networks: Optional[Any] = None

        self.checks_completed = 0
        self.errors: List[Any] = []
        self._network_file = database_path
        self._test_list.extend(["connectivity_auto", "connections_table"])

    def has_critical_errors(self, fail_on_errors):
        self.critical()
        if len(self.errors) > 0:
            if fail_on_errors:
                self.logger.critical(self.errors)
                raise ValueError("YOUR SUPPLY FILE CONTAINS ERRORS")
            return True
        return False

    def _other_critical_tests(self):
        self.connectivity_auto()

    def connectivity_auto(self) -> None:
        """Checks auto network connectivity

        It computes paths between nodes in the network or between every single link/direction combination
        in the network
        """

        get_qry = "SELECT link flink, dir fdir, to_link tlink, to_dir tdir, 1.0 distance from Connection"

        with read_and_close(self._path_to_file) as conn:
            records = pd.read_sql(get_qry, conn)
            loc_links = pd.read_sql("Select location, link from Location_Links", conn)
            locations = pd.read_sql("Select location from Location", conn)

        auto_net = records.assign(fnode=records.flink * 2 + records.fdir, tnode=records.tlink * 2 + records.tdir)
        if auto_net.empty:
            if not locations.empty:
                self.errors.append({"connectivity auto": {"locations not connected": locations.location.to_list()}})
            return

        # The graph is composed by connections, which behave as the edges, and link/directions, which represent
        # the vertices in the connected component analysis
        n = max(auto_net.fnode.max() + 1, auto_net.tnode.max() + 1)
        csr = coo_matrix(
            (
                auto_net.distance.to_numpy(),
                (auto_net.fnode.astype(np.int64).to_numpy(), auto_net.tnode.astype(np.int64).to_numpy()),
            ),
            shape=(n, n),
        ).tocsr()

        n_components, labels = connected_components(csgraph=csr, directed=True, return_labels=True, connection="strong")

        # We then identify all the link/directions that have the highest connectivity degree (i.e. the biggest island)
        bc = np.bincount(labels)
        max_label = np.where(bc == bc.max())[0][0]
        isconn = np.where(labels == max_label)[0]

        # And compare them to the contents of the location_links table
        # Locations that don't have at least one associated link in the biggest island
        # are considered disconnected
        connected = np.unique(np.hstack((np.floor(isconn / 2).astype(np.int64), np.ceil(isconn / 2).astype(np.int64))))
        loc_links = loc_links[loc_links.link.isin(connected)]
        connected_locations = loc_links.location.unique()
        disconnected_locations = locations[~locations.location.isin(connected_locations)].location.to_list()

        errors = {"locations not connected": disconnected_locations} if disconnected_locations else {}

        if errors:
            self.errors.append({"connectivity auto": errors})
            self.logger.warning("There are locations in the auto network that are not fully connected")

    def connections_table(self, basic=True):
        """Includes
        * search for pockets that are not used in the connection table
        * search for pockets missing from the pockets table
        * search for lanes not connected to any other link at an intersection
        """

        checker = CheckConnectionTable(self._path_to_file)

        if basic:
            checker.lane_connection(False)
        else:
            checker.full_check()
        errors = checker.errors

        for key, val in errors.items():
            self.logger.error(key)
            self.logger.error(val)
