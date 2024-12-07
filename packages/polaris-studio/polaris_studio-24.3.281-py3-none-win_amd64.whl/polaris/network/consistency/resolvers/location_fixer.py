# Copyright (c) 2024, UChicago Argonne, LLC
# BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
import sqlite3

import shapely.wkb

from polaris.network.consistency.network_objects.location import Location
from polaris.network.consistency.table_issue import TableIssue
from .fixer import Fixer
from .raise_me import raise_me


class LocationFixer(Fixer):
    def __init__(self, issue: TableIssue, geotool, data_tables, conn):
        super().__init__(issue, geotool, data_tables, conn)

    def execute(self, conn: sqlite3.Connection):
        new_location_ev = []
        sql_near = """select ID, asbinary(geo), location from EV_Charging_Stations
                       where MbrContains((Select Buffer(geo, 1000) from Location where Location.location=?), geo)"""

        if self.issue.operator == "DELETE":
            sql = "Select ID, asbinary(geo), location from EV_Charging_Stations where location=?"
            new_location_ev = list(conn.execute(sql, [self.issue.id_value]).fetchall())

        else:
            location = Location(self.issue.id_value, self.geotool, self.data, conn)
            if not location.__exists__:
                return

            if self.issue.operator == "ADD":
                location.all_geo_updates(conn)
                conn.commit()
                new_location_ev = list(conn.execute(sql_near, [location.id]).fetchall())

            elif self.issue.operator == "EDIT":
                if self.issue.field == "geo":
                    location.all_geo_updates(conn)
                    new_location_ev = list(conn.execute(sql_near, [location.id]).fetchall())

                elif self.issue.field == "link":
                    location.update_link(conn)
                    location.update_location_links(conn)
                elif self.issue.field == "walk_link":
                    location.update_walk_link(conn)
                elif self.issue.field == "bike_link":
                    location.update_bike_link(conn)
                elif self.issue.field == "zone":
                    location.update_zone(conn)
                else:
                    raise_me(self.issue)

        ev_fixer = []
        for ev_id, wkb, loc in new_location_ev:
            new_loc = self.geotool.get_geo_item("location", shapely.wkb.loads(wkb))
            if new_loc != loc:
                ev_fixer.append([new_loc, ev_id])

        if ev_fixer:
            conn.executemany("Update EV_Charging_Stations set location=? where ID=?", ev_fixer)
            ev_ids = [[e[1]] for e in ev_fixer]
            sql = "Update editing_table set checked=1 where table_name='EV_Charging_Stations' and id_value=?"
            conn.executemany(sql, ev_ids)
            conn.commit()
