# Copyright (c) 2024, UChicago Argonne, LLC
# BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
import sqlite3

from polaris.network.consistency.network_objects.mobility_dock import MicromobilityDock
from .fixer import Fixer


class MicromobilityDocksFixer(Fixer):
    def __init__(self, issue, geotool, data_tables, conn: sqlite3.Connection):
        super().__init__(issue, geotool, data_tables, conn)

    def execute(self, conn: sqlite3.Connection):
        """Fixes all issues logged for backlog editing originated from changes in the Micromobility_Docks Table"""

        if [self.issue.field, self.issue.operator] not in [
            [None, "ADD"],
            ["zone", "EDIT"],
            ["geo", "EDIT"],
            ["link", "EDIT"],
        ]:
            raise ValueError(f"I don't know how to fix self.issue {self.issue}")

        dock = MicromobilityDock(self.issue.id_value, self.data, self.geotool, conn)

        dock.update_zone(False)
        dock.update_link(False)
        dock.save(conn)
