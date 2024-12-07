# Copyright (c) 2024, UChicago Argonne, LLC
# BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
import sqlite3

import shapely.wkb

from polaris.network.consistency.table_issue import TableIssue
from .fixer import Fixer


class NodeFixer(Fixer):
    def __init__(self, issue: TableIssue, geotool, data_tables, conn: sqlite3.Connection):
        super().__init__(issue, geotool, data_tables, conn)

    def execute(self, conn: sqlite3.Connection):
        if self.issue.operator == "DELETE":
            conn.execute("DELETE from Connection where node=?", [self.issue.id_value])
            conn.execute("DELETE from Signal where nodes=?", [self.issue.id_value])
            conn.execute("DELETE from Sign where nodes=?", [self.issue.id_value])
        elif self.issue.operator in ["EDIT", "ADD"]:
            if self.issue.field not in ["geo", "zone"]:
                raise ValueError(f"How to fix issues for table {self.issue.table_name} and field {self.issue.field}??")

            dt = conn.execute("Select asbinary(geo) from Node where node=?", [self.issue.id_value]).fetchone()
            if not dt:
                return
            geo = dt[0]
            zone = self.geotool.get_geo_item("zone", shapely.wkb.loads(geo))
            conn.execute("Update Node set zone=? where node=?", [zone, self.issue.id_value])
            sql = """Update Editing_Table set checked=1 where table_name="Node" and field="zone" and id_value=?"""
            conn.execute(sql, [str(self.issue.id_value)])
            conn.commit()
