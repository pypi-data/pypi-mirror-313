# Copyright (c) 2024, UChicago Argonne, LLC
# BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
import sqlite3

from polaris.network.consistency.network_objects.ev_charge import EVChargeStation
from polaris.network.consistency.table_issue import TableIssue
from .fixer import Fixer


class EVFixer(Fixer):
    def __init__(self, issue: TableIssue, geotool, data_tables, conn):
        super().__init__(issue, geotool, data_tables, conn)

    def execute(self, conn: sqlite3.Connection):
        ev = EVChargeStation(self.issue.id_value, data_tables=self.data)
        ev.location = self.geotool.get_geo_item("location", ev.geo)
        ev.zone = self.geotool.get_geo_item("zone", ev.geo)
        ev.save(conn)
