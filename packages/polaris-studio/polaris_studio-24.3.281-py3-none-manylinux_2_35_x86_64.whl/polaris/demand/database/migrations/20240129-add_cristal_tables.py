# Copyright (c) 2024, UChicago Argonne, LLC
# BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
from polaris.utils.database.db_utils import has_table
from polaris.utils.database.standard_database import DatabaseType, StandardDatabase


def migrate(conn):
    db = StandardDatabase.for_type(DatabaseType.Demand)
    if not has_table(conn, "firms"):
        db.add_table(conn, "firms", None, add_defaults=False)
    if not has_table(conn, "establishments"):
        db.add_table(conn, "establishments", None, add_defaults=False)
    if not has_table(conn, "industry_make_use"):
        db.add_table(conn, "industry_make_use", None, add_defaults=True)
