# Copyright (c) 2024, UChicago Argonne, LLC
# BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
import sqlite3

import shapely.wkb

from .table_issue import TableIssue


def node_issues(conn: sqlite3.Connection, issue: TableIssue, net):
    if issue.field not in ["geo", "zone"]:
        raise ValueError(f"How to fix issues for table {issue.table_name} and field {issue.field}??")

    if issue.operator == "DELETE":
        pass
    elif issue.operator in ["EDIT", "ADD"]:
        geo = net.conn.execute("Select asbinary(geo) from Node where node=?").fetchone()[0]
        zone = net.geo.get_geo_item("zone", shapely.wkb.loads(geo))
        conn.execute("Update Node set zone=? where node=?", [zone, issue.id_value])
        conn.execute(
            "Update Editing_Table set checked=1 " "where table_name='Node' and field='zone' and id_value=?",
            [str(issue.id_value)],
        )
        conn.commit()
