# Copyright (c) 2024, UChicago Argonne, LLC
# BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
import sqlite3

import shapely.wkb

from polaris.network.consistency.table_issue import TableIssue
from .fixer import Fixer


class ZoneFixer(Fixer):
    def __init__(self, issue: TableIssue, geotool, data_tables, conn: sqlite3.Connection):
        super().__init__(issue, geotool, data_tables, conn)

    def execute(self, conn: sqlite3.Connection):
        tables = ["EV_Charging_Stations", "Location", "Node", "Parking", "Transit_Stops", "Micromobility_Docks"]

        # If Geometry changed or zone was deleted, we get all elements that used to be associated with
        # said zone and recompute it
        if self.issue.operator in ["EDIT", "DELETE"]:
            sql = """SELECT ROWID, asbinary(geo) FROM {0} WHERE zone=?;"""
            for table in tables:
                sql_table = sql.format(table)

                updates = []
                for id, geo in conn.execute(sql_table, [self.issue.id_value]).fetchall():
                    zn = self.geotool.get_geo_item("zone", shapely.wkb.loads(geo))
                    updates.append([zn, id])
                if updates:
                    sql_update = f"""UPDATE {table} set zone=? WHERE ROWID=?;"""
                    conn.executemany(sql_update, updates)
        # Then we recompute the zone for all the elements inside the zone
        # There will be tons of repeated operations for EDIT, but nothing to be done
        if self.issue.operator in ("ADD", "EDIT"):
            sql = """Update {0} set zone=? where ST_Within(geo, (select geo from Zone where zone=?))  and
                        ({0}.rowid in (select rowid from SpatialIndex where f_table_name = {1} and
                        search_frame = (select geo from Zone where zone=?)))"""
            # There is a chance that other items outside any zone would need to be changed
            # As they would be now closer to this newly added zone
            # however, we ignore that possibility for now
            for table in tables:
                sql_table = sql.format(table, f"'{table}'")
                conn.execute(sql_table, [self.issue.id_value, self.issue.id_value, self.issue.id_value])
            conn.commit()
