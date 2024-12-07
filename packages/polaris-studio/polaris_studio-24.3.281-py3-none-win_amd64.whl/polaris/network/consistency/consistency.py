# Copyright (c) 2024, UChicago Argonne, LLC
# BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
from os import PathLike
from typing import List

import polaris.network
from polaris.network.consistency.resolvers.ev_fixer import EVFixer
from polaris.network.consistency.resolvers.link_fixer import LinkFixer
from polaris.network.consistency.resolvers.location_fixer import LocationFixer
from polaris.network.consistency.resolvers.location_links_fixer import LocationLinksFixer
from polaris.network.consistency.resolvers.micromobility_docks_fixer import MicromobilityDocksFixer
from polaris.network.consistency.resolvers.node_fixer import NodeFixer
from polaris.network.consistency.resolvers.transit_bike_fixer import TransitBikeFixer
from polaris.network.consistency.resolvers.transit_stops_fixer import TransitStopsFixer
from polaris.network.consistency.resolvers.transit_walk_fixer import TransitWalkFixer
from polaris.network.consistency.resolvers.zone_fixer import ZoneFixer
from polaris.network.consistency.table_issue import TableIssue
from polaris.network.data.data_table_cache import DataTableCache
from polaris.network.utils.srid import get_srid
from polaris.network.starts_logging import logger
from polaris.network.traffic.intersec import Intersection
from polaris.network.utils.worker_thread import WorkerThread
from polaris.utils.database.db_utils import commit_and_close
from polaris.utils.signals import SIGNAL


class Consistency(WorkerThread):
    consistency = SIGNAL(object)

    def __init__(self, network_file: PathLike):
        WorkerThread.__init__(self, None)
        from polaris.network.tools.geo import Geo

        self.srid = get_srid(network_file)
        self.geotools = Geo(network_file)
        self.data_tables = DataTableCache(network_file)
        self.__network_file = network_file
        self.logger = logger
        self.issues_addressed = 0
        self.errors: List[TableIssue] = []
        self.intersections_to_rebuild: List[int] = []
        self.__max_id__ = -1
        self.__populate()
        self.__currently_running = ""
        self.resolvers = {
            "location": LocationFixer,
            "zone": ZoneFixer,
            "transit_walk": TransitWalkFixer,
            "node": NodeFixer,
            "transit_stops": TransitStopsFixer,
            "link": LinkFixer,
            "micromobility_docks": MicromobilityDocksFixer,
            "ev_charging_stations": EVFixer,
            "transit_bike": TransitBikeFixer,
            "location_links": LocationLinksFixer,
        }
        self.master_txt = "Enforcing consistency"

    def doWork(self):
        """Alias for execute"""
        self.enforce()

    def enforce(self):
        """Runs through all records on *Editing_Table* and fixes one at a time"""
        self.clean_data()
        err = len(self.errors)
        if err:
            self.logger.info(f'  Enforcing {err} database consistency issue{"s" if err > 1 else ""}.')
            self.__process_queue()
        self.finish()

    def finish(self):
        """Kills the progress bar so others can be generated"""
        self.consistency.emit(["finished_consistency_procedure"])

    def clean_data(self):
        """Clears all the data and indices from memory"""
        self.data_tables.refresh_cache()
        self.geotools.clear_cache()

    def __process_queue(self):
        self.consistency.emit(["start", "master", 2, self.master_txt])
        self.consistency.emit(["start", "secondary", len(self.errors), self.master_txt, self.master_txt])
        with commit_and_close(self.__network_file, spatial=True) as conn:
            for counter, issue in enumerate(self.errors):  # type: [int, TableIssue]
                self.consistency.emit(["update", "secondary", counter + 1, self.master_txt])
                issue.table_name = issue.table_name.lower()

                if issue.table_name not in self.resolvers:
                    raise ValueError(f"Don't know how to fix issue for table {issue.table_name}")
                rslvr = self.resolvers[issue.table_name](issue, self.geotools, self.data_tables, conn)  # type: Fixer
                rslvr.execute(conn=conn)
                rslvr.close(conn=conn)
                # We eliminate all the new editing corrections created while ensuring database consistency
                # as these are obviously spurious
                # and we do after each one to not loose track of things when it crashes
                conn.execute(
                    """Update Editing_Table set recorded_change="Consistency enforcement",
                                      checked=1 where issue>?;""",
                    [self.__max_id__],
                )
                conn.commit()
                self.intersections_to_rebuild.extend(rslvr.intersections_to_rebuild)

            intersec = list(set(self.intersections_to_rebuild))
            txt_msg = "Rebuilding intersections"
            if intersec:
                self.consistency.emit(["start", "secondary", len(intersec), txt_msg, self.master_txt])
            for counter, nd in enumerate(intersec):
                self.consistency.emit(["update", "secondary", counter + 1, txt_msg, self.master_txt])
                a = Intersection(self.data_tables, self.__network_file)
                a.load(nd, conn)
                has_signal = a.has_signal(conn)
                has_sign = a.has_stop_sign(conn)
                a.rebuild_intersection(conn)
                if has_signal and a.supports_signal(conn):
                    a.delete_signal(conn)
                    a.create_signal(conn)
                if has_sign:
                    a.delete_stop_sign(conn)
                    a.add_stop_sign(conn)

        if len(self.errors):
            chckr = polaris.network.checker.supply_checker.SupplyChecker(self.__network_file)
            chckr.critical()
            chckr.consistency_tests()

    def __populate(self):
        with commit_and_close(self.__network_file, spatial=True) as conn:
            sql = "PRAGMA table_info(Editing_Table);"
            fields = [x[1] for x in conn.execute(sql).fetchall()]

            sql = "SELECT * FROM Editing_Table WHERE checked != 1;"
            errors = [TableIssue(record, fields) for record in conn.execute(sql).fetchall()]
            self.__max_id__ = conn.execute("Select max(issue) from Editing_Table;").fetchone()[0]

        solving_order = ["zone", "node", "link", "transit_stops", "transit_walk", "location", "transit_bike"]
        self.errors = []
        for item in solving_order:
            self.errors.extend([issue for issue in errors if issue.table_name.lower() == item])
