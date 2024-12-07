# Copyright (c) 2024, UChicago Argonne, LLC
# BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
import os
import uuid
from os.path import join, isfile
from shutil import copyfile, rmtree
from tempfile import gettempdir

from polaris.network.network import Network
from polaris.utils.database.spatialite_utils import connect_spatialite


class TempNetwork:
    # d = datetime.today().strftime("%Y_%m_%d")
    __empty_network_file = join(gettempdir(), "polaris_empty_network.sqlite")

    def __init__(self, from_network_path=None):
        from_network_path = from_network_path or self.__create_empty_network_db()

        self.dir = join(gettempdir(), f"polaris_{uuid.uuid4().hex}")
        os.mkdir(self.dir)
        self.network_db_file = join(self.dir, "polaris_network.sqlite")
        copyfile(from_network_path, self.network_db_file)
        self.network = Network.from_file(self.network_db_file, False)
        self.network_methods = [f for f in dir(self.network) if not f.startswith("_")]
        self.conn = connect_spatialite(self.network_db_file)
        self.conn.commit()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self, clear_issues=False):
        self.network.close(clear_issues=clear_issues)
        try:
            rmtree(self.dir)
        except Exception as e:
            print(e.args)  # Oh well, we tried

    def __getattr__(self, func):
        """Delegate all incoming method calls and attributes to the underlying network object."""
        if func not in self.network_methods:
            raise AttributeError
        return getattr(self.network, func)

    @staticmethod
    def __create_empty_network_db():
        if not isfile(TempNetwork.__empty_network_file):
            Network.create(TempNetwork.__empty_network_file, srid=26916, jumpstart=True)
        return TempNetwork.__empty_network_file
