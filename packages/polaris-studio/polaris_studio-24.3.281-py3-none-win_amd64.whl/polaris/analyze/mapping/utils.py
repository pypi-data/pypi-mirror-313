# Copyright (c) 2024, UChicago Argonne, LLC
# BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
from polaris.utils.database.db_utils import commit_and_close


def network_central_point(netfile):
    with commit_and_close(netfile, spatial=True) as conn:
        srid = conn.execute("select srid from geometry_columns where f_table_name='node'").fetchone()[0]

        sql = """SELECT ST_X(ST_Transform(MakePoint(AVG(x), AVG(y),?), 4326)),
                        ST_Y(ST_Transform(MakePoint(AVG(x), AVG(y),?), 4326))  from node"""

        return conn.execute(sql, [srid, srid]).fetchone()
