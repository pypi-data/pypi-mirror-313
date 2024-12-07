# Copyright (c) 2024, UChicago Argonne, LLC
# BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
import shapely.wkb

from .table_issue import TableIssue


def transit_walk_issues(issue: TableIssue, net):
    if issue.id_field != "walk_link":
        raise ValueError(f"How to fix issues for table {issue.table_name} and field {issue.id_field}??")

    for table, field in [["Location", "location"], ["Parking", "parking"]]:
        if issue.operator == "DELETE":
            sql = f"Select {field}, asbinary(geo) from {table} where walk_link=?"
        elif issue.operator in ["EDIT", "ADD"]:
            sql = f"""select {field}, asbinary(geo) from {table}
                      where MbrContains((Select Buffer(geo, 1000) from Transit_Walk where walk_link=?), geo)"""
        items = net.conn.execute(sql).fetchall()
        data = [(net.geo.get_geo_item("walk_link", shapely.wkb.loads(wkb)), p) for p, wkb in items]
        if data:
            net.conn.executemany(f"Update {table} set walk_link=? where {field}=?", data)
        net.conn.commit()
