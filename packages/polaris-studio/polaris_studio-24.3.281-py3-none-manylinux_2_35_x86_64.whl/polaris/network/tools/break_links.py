# Copyright (c) 2024, UChicago Argonne, LLC
# BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
import os
from copy import deepcopy
from math import ceil

import pandas as pd
import shapely.wkb
from shapely.ops import substring

from polaris.network.data.data_table_cache import DataTableCache
from polaris.network.utils.srid import get_srid
from polaris.network.starts_logging import logger
from polaris.network.utils.worker_thread import WorkerThread
from polaris.utils.database.db_utils import commit_and_close
from polaris.utils.signals import SIGNAL


class BreakLinks2Max(WorkerThread):
    breaking = SIGNAL(object)

    def __init__(self, maximum_length: float, path_to_file: os.PathLike):
        WorkerThread.__init__(self, None)
        self.maximum_length = maximum_length
        self.path_to_file = path_to_file

    def doWork(self):
        """alias for execute"""
        self.execute()
        self.breaking.emit(["finished_threaded_procedure"])

    def execute(self):
        with commit_and_close(self.path_to_file, spatial=True) as conn:
            srid = get_srid(conn=conn)

            max_node = [x[0] for x in conn.execute("select max(node) from node")][0] + 1
            max_link = [x[0] for x in conn.execute("select max(link) from link")][0] + 1

            sql = f'select link, asBinary(geo), node_a, node_b geo from link where "length">{self.maximum_length}'
            dt = list(conn.execute(sql))
            link_geometries = {x[0]: shapely.wkb.loads(x[1]) for x in dt}
            link_records = pd.read_sql(f'select * from link where "length">{self.maximum_length}', conn)

            if link_records.empty:
                return

            logger.critical("BREAKING LINKS INTRODUCES NODES WITH NO ELEVATION INFORMATION")
            logger.critical("AS A CONSEQUENCE, THE GRADE FOR ALL NEW LINKS WILL BE WRONG")
            txt_hdr = "Breaking links"
            self.breaking.emit(["start", "master", 4, txt_hdr])
            self.breaking.emit(["start", "secondary", len(link_records.keys()), txt_hdr, txt_hdr])
            self.breaking.emit(["start", "secondary", 1, "Adding link data", txt_hdr])

            new_link_geo = {}
            all_new_links = []
            for counter, (_, rec) in enumerate(link_records.iterrows()):
                self.breaking.emit(["update", "secondary", counter + 1, txt_hdr, txt_hdr])
                parts = ceil(rec.length / self.maximum_length)
                link_geo = link_geometries[rec.link]

                for i in range(parts):
                    link_segment = deepcopy(rec)
                    link_segment.link = max_link
                    link_segment.node_a = max_node
                    if i + 1 < parts:
                        link_segment.node_b = max_node + 1
                    link_segment.length = link_segment.length / parts
                    new_link_geo[max_link] = substring(link_geo, i / parts, (i + 1) / parts, normalized=True)
                    all_new_links.append(link_segment)
                    max_node += 1
                    max_link += 1

            # Cleans the Transit_Pattern_Mapping table
            tables = DataTableCache(self.path_to_file)
            tpm = tables.get_table("Transit_Pattern_Mapping").reset_index()
            links_used = tpm[tpm.link.isin(link_records.link)]
            to_delete = [[x] for x in links_used.pattern_id.unique()]
            conn.executemany("DELETE FROM Transit_Pattern_Mapping WHERE pattern_id=?", to_delete)
            conn.commit()
            if to_delete:
                logger.critical(f"Map-matching for {len(to_delete)} were removed to maintain compatibility")

            new_links = pd.DataFrame(all_new_links)
            new_links.to_sql("Link", conn, if_exists="append", index=False)
            self.breaking.emit(["update", "secondary", 1, "Adding link data", txt_hdr])

            self.breaking.emit(["start", "secondary", len(new_link_geo.keys()), "Adding link geo", txt_hdr])
            for counter, (k, v) in enumerate(new_link_geo.items()):
                self.breaking.emit(["update", "secondary", counter + 1, "Adding link geo", txt_hdr])
                conn.execute("Update Link set geo=GeomFromWKB(?, ?) where link=?", [v.wkb, srid, k])
            conn.commit()

            self.breaking.emit(["start", "secondary", 1, "Removing old links", txt_hdr])
            conn.execute('delete from Link where "length">?', [self.maximum_length])
        self.breaking.emit(["update", "secondary", 1, "Removing old links", txt_hdr])
