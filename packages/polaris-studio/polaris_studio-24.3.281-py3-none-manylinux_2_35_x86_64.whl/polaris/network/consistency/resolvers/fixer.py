# Copyright (c) 2024, UChicago Argonne, LLC
# BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
import sqlite3
from typing import List

from ..table_issue import TableIssue


class Fixer:
    def __init__(self, issue: TableIssue, geotool, data_tables, conn):
        self.issue = issue
        self.geotool = geotool
        self.data = data_tables
        self.intersections_to_rebuild: List[int] = []

    def close(self, conn: sqlite3.Connection):
        self.issue.tick_off(conn)
        conn.commit()
