# Copyright (c) 2024, UChicago Argonne, LLC
# BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
import logging
import os
import sqlite3
from typing import Dict, Optional

import pandas as pd
from polaris.demand.checker.demand_checker import DemandChecker
from polaris.utils.database.db_utils import commit_and_close
from polaris.utils.database.db_utils import safe_connect
from polaris.utils.logging_utils import ensure_stdout_handler


class Demand:
    """Polaris Demand Class"""

    def __init__(self):
        """Instantiates the network"""
        self.path_to_file: os.PathLike
        self.conn: Optional[sqlite3.Connection] = None
        self.modes: Optional[Dict[int, str]] = None

    @staticmethod
    def from_file(demand_file: os.PathLike):
        demand = Demand()
        demand.open(demand_file)
        return demand

    @staticmethod
    def create(demand_file: str) -> None:
        """Creates new empty demand file. Fails if file exists
        Args:
            *demand_file* (:obj:`str`): Full path to the demand file to be created.
        """
        from polaris.utils.database.standard_database import StandardDatabase, DatabaseType

        if os.path.isfile(demand_file):
            raise FileExistsError

        with commit_and_close(demand_file, missing_ok=True) as conn:
            StandardDatabase.for_type(DatabaseType.Demand).create_tables(conn, None, add_defaults=True)

    def open(self, demand_file: os.PathLike):
        """Opens demand for editing/querying

        Args:
            *demand_file* (:obj:`str`): Full path to the demand file to be opened.
        """

        if not os.path.isfile(demand_file):
            raise FileNotFoundError
        self.path_to_file = demand_file
        logging.getLogger("polaris").info(f"Working with file on {demand_file}")
        self.conn = safe_connect(demand_file, False)

    def upgrade(self) -> None:
        """Updates the network to the latest version available"""
        from polaris.utils.database.migration_manager import MigrationManager
        from polaris.utils.database.standard_database import DatabaseType

        MigrationManager.upgrade(self.path_to_file, DatabaseType.Demand, redo_triggers=False)

    def close(self):
        """Closes database connection"""
        self.conn.close()
        logging.getLogger("polaris").info(f"Demand closed at {self.path_to_file}")

    def set_debug(self, level=logging.DEBUG):
        """Sets logging to debug mode throughout the package.

        As a result of this method_call, logging will become extremely verbose. Use only when necessary

        Args:
            *level* (:obj:`int`): Logging level to be used (DEBUG:10, INFO:20, WARN:30, ERROR:40 CRITICAL:50)
        """
        self.__logging_level = level
        logger = logging.getLogger("polaris")
        logger.setLevel(level)
        for ch in logger.handlers:
            ch.setLevel(self.__logging_level)

    def log_to_terminal(self):
        """Adds the terminal as a logging output"""
        ensure_stdout_handler(logging.getLogger("polaris"), logging.ERROR)

    @property
    def checker(self) -> DemandChecker:
        return DemandChecker(self.path_to_file)

    @property
    def mode_lookup(self):
        self.modes = self.modes or Demand.load_modes(self.conn)
        return self.modes

    @staticmethod
    def load_modes(conn):
        return pd.read_sql("SELECT * FROM mode;", conn).set_index("mode_id").mode_description.to_dict()

    def commit(self):
        """Commits all changes to the database"""
        self.conn.commit()
