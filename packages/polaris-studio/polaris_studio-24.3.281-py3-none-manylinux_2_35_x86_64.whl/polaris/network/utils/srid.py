# Copyright (c) 2024, UChicago Argonne, LLC
# BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
# Copied from AequilibraE
import os
import sqlite3
from typing import Optional

import numpy as np

from polaris.utils.database.db_utils import read_and_close

sqlite3.register_adapter(np.int64, int)
sqlite3.register_adapter(np.int32, int)
sqlite3.register_adapter(np.float32, float)
sqlite3.register_adapter(np.float64, float)
sqlite3.register_adapter(object, str)


def get_srid(database_path: Optional[os.PathLike] = None, conn: Optional[sqlite3.Connection] = None) -> int:
    if database_path is None and conn is None:
        raise Exception("To retrieve an SRID you must provide a database connection OR a path to the database")
    with conn or read_and_close(database_path) as conn:
        dt = conn.execute('select srid from geometry_columns where f_table_name="link"').fetchone()
        return int(dt[0]) if dt else -1
