# Copyright (c) 2024, UChicago Argonne, LLC
# BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
from sqlite3 import Connection
from typing import List, Tuple, Any


class TableIssue:
    def __init__(self, record: Tuple, fields: List[str]):
        self.id_value = -1
        self.id_field = ""
        self.field = ""
        self.table_name = ""
        self.operator = ""
        self.issue = -1
        self.field_value: Any = None
        for key, val in zip(fields, record):
            if key == "id_value" and isinstance(val, str) and val.isdigit():
                val = int(val)
            self.__dict__[key] = val

    def tick_off(self, conn: Connection, txt=""):
        conn.execute(
            f"""Update Editing_table set checked=1, recorded_change= "Automatic consistency fixer: {txt}"
                      where issue=?""",
            [self.issue],
        )
        conn.commit()
