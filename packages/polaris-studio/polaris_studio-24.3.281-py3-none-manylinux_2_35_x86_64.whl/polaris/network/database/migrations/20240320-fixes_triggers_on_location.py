# Copyright (c) 2024, UChicago Argonne, LLC
# BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
from polaris.network.create.triggers import recreate_network_triggers
from polaris.network.utils.srid import get_srid


def migrate(conn):
    recreate_network_triggers(conn, get_srid(conn=conn))
