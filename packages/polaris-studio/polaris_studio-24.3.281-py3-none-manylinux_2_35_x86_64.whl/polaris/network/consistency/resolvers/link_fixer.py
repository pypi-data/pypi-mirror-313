# Copyright (c) 2024, UChicago Argonne, LLC
# BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
import sqlite3

from polaris.network.consistency.network_objects.location import Location
from polaris.network.consistency.network_objects.parking import Parking
from polaris.network.consistency.table_issue import TableIssue
from .fixer import Fixer
from .raise_me import raise_me


class LinkFixer(Fixer):
    def __init__(self, issue: TableIssue, geotool, data_tables, conn):
        super().__init__(issue, geotool, data_tables, conn)

    def execute(self, conn: sqlite3.Connection):
        from polaris.network.consistency.network_objects.link import Link

        if self.issue.operator != "DELETE":
            link = Link(int(self.issue.id_value), self.geotool, self.data, conn)
            if not link.__exists__:
                return
        locations_to_fix = []
        parking_to_fix = []
        if self.issue.operator == "DELETE":
            # Deleting items from Location_links, Pocket, Sign and Connection is done at run time
            if self.issue.field is None:
                sql = "Select location from Location where link=?"
                locations_to_fix = [x[0] for x in conn.execute(sql, [self.issue.id_value]).fetchall()]

                sql = "Select parking from Parking where link=?"
                parking_to_fix = [x[0] for x in conn.execute(sql, [self.issue.id_value]).fetchall()]
            elif self.issue.field in ["node_a", "node_b"]:
                # We rebuild intersection around node a or b
                self.intersections_to_rebuild.append(self.issue.field_value)
            else:
                raise_me(self.issue)

        elif self.issue.operator == "ADD":
            locations_to_fix = link.get_nodes_vicinity("location", "Location", conn=conn)
            parking_to_fix = link.get_nodes_vicinity("parking", "Parking", conn=conn)

            link.lane_capacity_speed_consistency(conn)
            link.fill_area_type(conn)
            link.transfer_to_transit_walk(conn)
            self.intersections_to_rebuild.extend([link.node_a, link.node_b])

        elif self.issue.operator == "EDIT":
            if self.issue.field in ["type", "geo"]:
                locations_to_fix = link.get_nodes_vicinity("location", "Location", conn=conn)
                parking_to_fix = link.get_nodes_vicinity("parking", "Parking", conn=conn)
                link.transfer_to_transit_walk(conn)
                self.intersections_to_rebuild.extend([link.node_a, link.node_b])
                if self.issue.field == "geo":
                    link.fill_area_type(conn)
            elif self.issue.field in ["lanes_ab", "lanes_ba"]:
                self.intersections_to_rebuild.extend([link.node_a, link.node_b])
            elif self.issue.field in ["node_a", "node_b"]:
                self.intersections_to_rebuild.append(self.issue.field_value)
            elif self.issue.field in ["area_type"]:
                link.fill_area_type(conn)
            else:
                raise_me(self.issue)

        else:
            raise_me(self.issue)

        for loc in set(locations_to_fix):
            locat = Location(loc, self.geotool, self.data, conn=conn)
            locat.update_link(force_update=True, conn=conn)
            locat.update_walk_link(conn=conn)
            locat.update_location_links(conn)

        for park in set(parking_to_fix):
            p = Parking(park, self.geotool, self.data, conn=conn)
            p.update_link(conn=conn, force_update=True)
            p.update_walk_link(conn=conn)
