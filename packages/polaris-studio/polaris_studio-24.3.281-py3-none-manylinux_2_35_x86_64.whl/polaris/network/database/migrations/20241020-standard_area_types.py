# Copyright (c) 2024, UChicago Argonne, LLC
# BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
import warnings
from pathlib import Path

import pandas as pd

from polaris.network.create.triggers import recreate_network_triggers
from polaris.network.utils.srid import get_srid


def migrate(conn):

    df = pd.read_csv(Path(__file__).parent.parent / "default_values/Area_Type.csv")

    recs = df[["area_type", "name"]].to_records(index=False)
    conn.executemany("INSERT OR IGNORE INTO Area_Type(area_type, name) VALUES(?,?)", recs)
    conn.execute("DELETE FROM Area_Type WHERE area_type not in (1,2,3,4,5,6,7,8,98,99)")
    conn.execute("UPDATE Link SET area_type=98 WHERE area_type not in (1,2,3,4,5,6,7,8,98,99)")
    conn.execute("UPDATE Zone SET area_type=98 WHERE area_type not in (1,2,3,4,5,6,7,8,98,99)")

    # INSERT OR IGNORE INTO Area_Types(land_use, is_home, is_work,is_school,is_discretionary,notes) VALUES('RESIDENTIAL-SINGLE',1,0,0,1,'Inserted by the network upgrader');
    recreate_network_triggers(conn, get_srid(conn=conn))
    warnings.warn("Area_Type table has been updated. Please run geo-consistency checks to update the network")
