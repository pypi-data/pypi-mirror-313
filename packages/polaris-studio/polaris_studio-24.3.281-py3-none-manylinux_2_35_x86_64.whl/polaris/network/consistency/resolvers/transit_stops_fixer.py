# Copyright (c) 2024, UChicago Argonne, LLC
# BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
import sqlite3

import shapely.wkb

from .fixer import Fixer


class TransitStopsFixer(Fixer):
    def __init__(self, issue, geotool, data_tables, conn: sqlite3.Connection):
        super().__init__(issue, geotool, data_tables, conn)

    def execute(self, conn: sqlite3.Connection):
        """Fixes all issues logged for backlog editing originated from changes in the Transit Stops Table"""

        if [self.issue.field, self.issue.operator] not in [[None, "ADD"], ["zone", "EDIT"], ["geo", "EDIT"]]:
            raise ValueError(f"I don't know how to fix self.issue {self.issue}")

        sql = "Select ST_asbinary(geo) from Transit_Stops where stop=?"
        dt = conn.execute(sql, [self.issue.id_value]).fetchone()
        if not dt:
            return
        wkb = dt[0]

        zone = self.geotool.get_geo_item("zone", shapely.wkb.loads(wkb))
        conn.execute("Update Transit_Stops set zone=? where stop=?", [zone, self.issue.id_value])
