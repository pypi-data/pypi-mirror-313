# Copyright (c) 2024, UChicago Argonne, LLC
# BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
import sqlite3

import shapely.wkb

from polaris.network.consistency.table_issue import TableIssue
from .fixer import Fixer


class TransitWalkFixer(Fixer):
    def __init__(self, issue: TableIssue, geotool, data_tables, conn: sqlite3.Connection):
        super().__init__(issue, geotool, data_tables, conn)

    def execute(self, conn: sqlite3.Connection):
        if self.issue.id_field != "walk_link":
            raise ValueError(f"How to fix issues for table {self.issue.table_name} and field {self.issue.id_field}??")

        for table, field in [["Location", "location"], ["Parking", "parking"]]:
            if self.issue.operator == "DELETE":
                sql = f"Select {field}, asbinary(geo) from {table} where walk_link=?"
            elif self.issue.operator in ["EDIT", "ADD"]:
                sql = "Select count(*) from Transit_Walk where walk_link=?"
                if sum(list(conn.execute(sql, [self.issue.id_value]).fetchone())) < 1:
                    return
                sql = f"""select {field}, asbinary(geo) from {table}
                          where MbrContains((Select Buffer(geo, 1000) from Transit_Walk where walk_link=?), geo)"""
            else:
                raise Exception("What do do with this operation?")
            items = list(conn.execute(sql, [self.issue.id_value]).fetchall())
            data = [(self.geotool.get_geo_item("walk_link", shapely.wkb.loads(wkb)), p) for p, wkb in items]
            if data:
                conn.executemany(f"Update {table} set walk_link=? where {field}=?", data)
