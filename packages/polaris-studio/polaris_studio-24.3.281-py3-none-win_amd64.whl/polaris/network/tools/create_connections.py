# Copyright (c) 2024, UChicago Argonne, LLC
# BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
import logging
import os
from typing import Dict

import pandas as pd
from polaris.network.utils.srid import get_srid
from polaris.network.osm.osm import OSM
from polaris.network.starts_logging import logger
from polaris.network.traffic.intersection_control.stop_sign import StopSign
from polaris.network.utils.worker_thread import WorkerThread
from polaris.utils.database.db_utils import commit_and_close, read_and_close
from polaris.utils.signals import SIGNAL


class CreateConnections(WorkerThread):
    connecting = SIGNAL(object)

    def __init__(self, data_tables, path_to_file: os.PathLike, signals, signs):
        WorkerThread.__init__(self, None)
        self.data_tables = data_tables
        self.logger = logging.getLogger("polaris")
        self.do_all_signs = False

        sql = """select distinct(node_a) node from Link l
                                inner join link_type lt on l.type=lt.link_type
                                where lt.use_codes like "%AUTO%"
                         union all
                         select distinct(node_b) node from Link l
                                inner join link_type lt on l.type=lt.link_type
                                where lt.use_codes like "%AUTO%" """
        with read_and_close(path_to_file) as conn:
            self.signals = [x[0] for x in conn.execute("Select nodes from Signal")] if signals is None else signals
            self.signs = [x[0] for x in conn.execute("Select nodes from Sign")] if signs is None else signs
            self.all_nodes = sorted({node[0] for node in conn.execute(sql)})
            if signs is not None:
                self.do_all_signs = len(signs) == 0

        self.osm = OSM(path_to_file)
        self.__path_to_file = path_to_file

    def doWork(self):
        """Alias for execute"""
        self.execute()

    def finish(self):
        """Kills the progress bar so others can be generated"""
        self.connecting.emit(["finished_connections_procedure"])

    def execute(self) -> None:
        """Rebuilds all connections in the network after clearing all existing connections and signals

        Args:
            *signals* (:obj:`List[int]`): List of nodes that should have signals rebuilt after connections are done
        """
        logger.info("Starting connection rebuild")
        self.data_tables.refresh_cache("Connection")
        with commit_and_close(self.__path_to_file, spatial=True) as conn:
            self.__processer(conn)
        logger.info("Finishing connection rebuild")

    def __processer(self, conn):
        from polaris.network.traffic.intersec import Intersection

        logger.info("Removing existing connections, signals and stop signs")
        curr = conn.cursor()

        sig_tables = [
            "signal",
            "signal_nested_records",
            "phasing",
            "phasing_nested_records",
            "timing",
            "timing_nested_records",
            "Pocket",
            "connection",
            "Sign",
        ]
        for table in sig_tables:
            curr.execute(f"delete from {table};")
        conn.commit()

        txt = "Rebuilding connections"
        self.connecting.emit(["start", "master", 1, txt])
        self.connecting.emit(["start", "secondary", len(self.all_nodes), txt, txt])

        connection_sets = []
        pocket_sets = []
        tables = [
            "Signal",
            "Phasing",
            "Timing",
            "Signal_Nested_Records",
            "Phasing_Nested_Records",
            "Timing_Nested_Records",
            "Sign",
        ]
        signal_sets: Dict[str, list] = {x: [] for x in tables}

        self.logger.info("      Recreating intersections")
        portions = max(1, len(self.all_nodes) // 20)
        for counter, node in enumerate(self.all_nodes):
            if counter % portions == 0:
                self.logger.info(f"      Processed {counter}/{len(self.all_nodes)} intersections")
            self.connecting.emit(["update", "secondary", counter + 1, txt, txt])

            inter = Intersection(self.data_tables, self.__path_to_file, conn, self.osm)
            inter.__bulk_loading__ = True
            inter.load(node, conn)

            c = inter._creates_connections(conn)
            connection_sets.append(c)
            pocket_sets.append(inter._builds_pockets)

            add_signal = False
            if isinstance(self.signals, list) and node in self.signals:
                add_signal = inter.supports_signal(conn)
            elif self.signals in ["osm", "geometric"] and node not in self.signs:
                if inter.supports_signal(conn):
                    if self.signals in ["osm", "geometric"]:
                        if self.signals == "osm":
                            add_signal = inter.osm_signal()
                        elif self.signals == "geometric":
                            add_signal = inter.determine_geometric_need_for_signal(conn)

            if (node in self.signs or self.do_all_signs) and not add_signal:
                ss = StopSign(inter)
                ss.re_compute()
                if ss.stop_signs:
                    signal_sets["Sign"].append(ss.data)
            elif add_signal:
                sig = inter.create_signal(conn, compute_and_save=False)
                sig.re_compute(conn)
                for table_name, data in sig.data.items():
                    signal_sets[table_name].append(data)

            logger.info(f"node {node}")
        # saves the data into the database
        conn_sets = pd.concat(connection_sets)
        cols = [x for x in conn_sets.columns if str(x).lower() != "geo"]
        conn_sets[cols].to_sql("Connection", conn, if_exists="append", index=False)
        geos = conn_sets[["geo", "link", "to_link"]].assign(srid=get_srid(conn=conn))
        npgeos = geos[["geo", "srid", "link", "to_link"]].to_records(index=False)
        conn.executemany("Update Connection set Geo=GeomFromWKB(?,?) where link=? and to_link=?", npgeos)
        pd.concat(pocket_sets).to_sql("Pocket", conn, if_exists="append", index=False)

        for table_name, data in signal_sets.items():
            if data:
                pd.concat(data).to_sql(table_name, conn, if_exists="append", index=False)

        self.connecting.emit(["finished_create_connections_procedure"])

        for table in sig_tables:
            self.data_tables.refresh_cache(table)
