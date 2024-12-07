# Copyright (c) 2024, UChicago Argonne, LLC
# BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
import sqlite3

from polaris.network.consistency.network_objects.location import Location
from polaris.network.consistency.table_issue import TableIssue
from .fixer import Fixer


class LocationLinksFixer(Fixer):
    def __init__(self, issue: TableIssue, geotool, data_tables, conn):
        super().__init__(issue, geotool, data_tables, conn)

    def execute(self, conn: sqlite3.Connection):
        if self.issue.operator != "DELETE":
            raise ValueError("We do not know how to solve this issue")

        sql_exists = "select count(*) from Location where Location.location=?), geo)"
        if sum(conn.execute(sql_exists).fetchone()) == 0:
            return

        location = Location(self.issue.id_value, self.geotool, self.data, conn=conn)
        location.update_location_links(conn=conn)
