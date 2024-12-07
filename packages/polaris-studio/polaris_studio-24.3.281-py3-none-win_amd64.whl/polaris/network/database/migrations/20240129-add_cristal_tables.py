# Copyright (c) 2024, UChicago Argonne, LLC
# BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
from polaris.utils.database.db_utils import has_table
from polaris.utils.database.standard_database import DatabaseType, StandardDatabase


def migrate(conn):
    db = StandardDatabase.for_type(DatabaseType.Supply)
    if not has_table(conn, "county_skims"):
        db.add_table(conn, "county_skims", None, add_defaults=False)
