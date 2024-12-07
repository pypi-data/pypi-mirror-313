# Copyright (c) 2024, UChicago Argonne, LLC
# BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
from os import PathLike

from polaris.utils.database.database_dumper import dump_database_to_csv
from polaris.utils.signals import SIGNAL
from .worker_thread import WorkerThread
from ...utils.database.db_utils import read_and_close


class NetworkDumper(WorkerThread):
    dumping = SIGNAL(object)

    def __init__(self, folder_name: str, path_to_file: PathLike):
        WorkerThread.__init__(self, None)
        self.folder_name = folder_name
        self.path_to_file = path_to_file

    def doWork(self):
        """Alias for execute"""
        with read_and_close(self.path_to_file, spatial=True) as conn:
            dump_database_to_csv(conn, self.folder_name, self.dumping)
