# Copyright (c) 2024, UChicago Argonne, LLC
# BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
import sqlite3
from typing import Optional

import pandas as pd

from polaris.network.traffic.intersec import Intersection
from .data_record import DataRecord


class Link(DataRecord):
    def __init__(self, link: int, geotool, data_tables, conn=None):
        self.node_a: int
        self.node_b: int
        self.cap_ab: int
        self.cap_ba: int
        self.lanes_ab: int
        self.lanes_ba: int
        self.fspd_ab: int
        self.fspd_ba: int
        super(Link, self).__init__(link, "Link", data_tables, pd.DataFrame([]), conn)
        from polaris.network.tools.geo import Geo

        self.geotool: Geo = geotool
        self.intersection_a: Optional[Intersection] = None
        self.intersection_b: Optional[Intersection] = None

    def save(self, conn: sqlite3.Connection):
        super(Link, self).save(conn)
        self._data.refresh_cache("link")

    def rebuild_intersections(self, conn: sqlite3.Connection):
        self.intersection_a = Intersection(self._data, self.geotool._network_file)
        self.intersection_a.load(self.node_a, conn)
        self.intersection_a.rebuild_intersection(conn)

        self.intersection_b = Intersection(self._data, self.geotool._network_file)
        self.intersection_b.load(self.node_b, conn)
        self.intersection_b.rebuild_intersection(conn)

    def lane_capacity_speed_consistency(self, conn: sqlite3.Connection):
        if self.lanes_ab == 0 and self.fspd_ab + self.cap_ab > 0:
            conn.execute("update link set cap_ab = 0, fspd_ab = 0 where link=?", [self.id])
        if self.lanes_ba == 0 and self.fspd_ba + self.cap_ba > 0:
            conn.execute("update link set cap_ba = 0, fspd_ba = 0 where link=?", [self.id])
        conn.commit()

    def transfer_to_transit_walk(self, conn: sqlite3.Connection):
        # We check if need to transfer to the Transit_Walk layer
        sql = "Select use_codes from Link_Type where link_type=(select type from Link where link=?)"
        dt = "".join([x[0] for x in conn.execute(sql, [self.id])])
        if dt and "WALK" in dt:
            sql = """INSERT INTO Transit_Walk(from_node, to_node, "length", ref_link, geo)
                     SELECT node_a, node_b, "length", link, geo FROM Link WHERE link=?
                     AND NOT EXISTS (SELECT 1 FROM Transit_Walk WHERE from_node=? AND to_node=?);"""
            conn.execute(sql, [self.id, int(self.node_a), int(self.node_b)])
        else:
            conn.execute("Delete from Transit_Walk where ref_link=?", [self.id])
        conn.commit()

    def get_nodes_vicinity(self, fld, tbl, conn: sqlite3.Connection, buffer=150):
        """Buffer is the distance from the link where we should link for points to update"""

        sql = f"""SELECT {fld} FROM {tbl}
                  WHERE ST_Intersects(geo, (select buffer(geo,{buffer}) from link where link={self.id})) AND
                  {tbl}.ROWID IN (SELECT ROWID FROM SpatialIndex WHERE f_table_name = '{tbl}' AND
                                    search_frame = (select buffer(geo,{buffer}) from link where link={self.id})) > 0"""
        return [x[0] for x in conn.execute(sql).fetchall()]

    def fill_area_type(self, conn: sqlite3.Connection):
        """Buffer is the distance from the link where we should link for points to update"""

        sql = f"""update link set area_type = (select area_type from(
                    SELECT zone.area_type, st_length(st_intersection(zone.geo, lnk.geo)) overlap
                    FROM zone, link AS lnk
                    WHERE ST_Intersects(zone.geo, lnk.geo) = 1
                      AND lnk.link={self.id}
                      AND zone.ROWID IN (
                        SELECT ROWID
                        FROM SpatialIndex
                        WHERE f_table_name = 'zone'
                            AND search_frame = (select geo from Link where link={self.id}))
                    order by overlap desc
                    limit 1)
                    ) where link={self.id}"""

        conn.execute(sql)
