# Copyright (c) 2024, UChicago Argonne, LLC
# BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
import logging
import os
from os import PathLike
from os.path import dirname, join
from pathlib import Path
from typing import Optional

from pyproj import CRS

from polaris.network.active.active_networks import ActiveNetworks
from polaris.network.checker.supply_checker import SupplyChecker
from polaris.network.consistency.consistency import Consistency
from polaris.network.consistency.geo_consistency import GeoConsistency
from polaris.network.consistency.network_objects.location import Location
from polaris.network.constants import constants
from polaris.network.create.triggers import create_network_triggers
from polaris.network.data.data_table_cache import DataTableCache
from polaris.network.utils.srid import get_srid
from polaris.network.diagnostics.diag import Diagnostics
from polaris.network.ie.import_export import ImportExport
from polaris.network.osm.osm import OSM
from polaris.network.starts_logging import logger
from polaris.network.tools.geo import Geo
from polaris.network.tools.tools import Tools
from polaris.network.traffic.intersec import Intersection
from polaris.network.transit.transit import Transit
from polaris.network.utils.unzips_spatialite import unzips_base_spatialite
from polaris.utils.database.db_utils import commit_and_close, read_and_close, write_about_model_value
from polaris.utils.database.db_utils import has_table
from polaris.utils.database.migration_manager import MigrationManager
from polaris.utils.database.standard_database import StandardDatabase, DatabaseType
from polaris.utils.logging_utils import add_file_handler, remove_file_handler, ensure_stdout_handler
from polaris.utils.optional_deps import check_dependency
from polaris.version import __version__ as net_version


class Network:
    """Polaris Network Class

    ::

        # We can open the network just to figure out its projection
        from polaris.network.network import Network
        n = Network()
        n.open(source)

        # We get the projection used in this project
        srid = n.srid

        # Or we can also get the checker for this network
        checker = n.checker

        # In case we ran some query while with the database open, we can commit it
        n.commit()

        # We can create a new network file from scratch as well
        new_net = Network()

        new_net.srid = srid # We use the SRID from the known network, for example

        # if we don't have Spatialite on our system path environment variables, we can
        # add it manually before attempting to create a new database
        new_net.add_spatialite('path/to/spatialite/folder')

        # If the second parameter is True, an SQLite file pre-populated with Spatialite extensions is used
        new_net.new('path/to/new/file', True)


        # To close the connection is simply
        n.close()

    """

    def __init__(self):
        """Instantiates the network"""
        self.path_to_file: PathLike = Path("")
        self.logger = logger
        self.__logging_level = logging.WARNING
        self.__dict__["srid"] = -1
        self.__transit__: Transit
        self.__tools__: Tools = None
        self.__active__: ActiveNetworks = None
        self.__checker__: SupplyChecker = None
        self.__diagnostics__: Diagnostics = None
        self.__geo_consistency__: GeoConsistency = None
        self.__consistency__: Consistency = None
        self.__geotool__: Geo = None
        self.__transit__: Transit = None
        self.__osm__: Optional[OSM] = None

    @staticmethod
    def from_file(network_file: PathLike, run_consistency=False):
        network = Network()
        network.open(Path(network_file), run_consistency)
        return network

    @staticmethod
    def create(network_file: PathLike, srid: int, jumpstart: bool = False) -> None:
        """Creates new empty network file
        Args:
            *network_file* (:obj:`str`): Full path to the network file to be opened.
            *jumpstart* (:obj:`bool`): Copies base sql already loaded with spatialite extension. It saves a few
            seconds of runtime.
        """
        if srid <= 0:
            raise ValueError("You need to choose an SRID for the project before creating it")

        unzips_base_spatialite(jumpstart, network_file)

        with commit_and_close(network_file, spatial=True, missing_ok=not jumpstart) as conn:
            if not jumpstart:
                conn.execute("SELECT InitSpatialMetaDataFull(1);")
            StandardDatabase.for_type(DatabaseType.Supply).create_tables(conn, srid, add_defaults=True)
            write_about_model_value(conn, "network_model_version", net_version)
            write_about_model_value(conn, "SRID", str(srid))
            create_network_triggers(conn, srid)

    def new(self, network_file: str, jumpstart=False) -> None:
        raise DeprecationWarning("Deprecated, use create instead")

    def open(self, network_file: PathLike, run_consistency=False):
        """Opens project for editing/querying

        Args:
            *network_file* (:obj:`str`): Full path to the network file to be opened.
        """

        if not os.path.isfile(network_file):
            raise FileNotFoundError
        self.path_to_file = network_file
        self.__log_setter()
        self.logger.info(f"Working with file on {network_file}")
        self.__gets_srid()
        self.__start_end(run_consistency)

    def upgrade(self) -> None:
        """Updates the network to the latest version available"""
        MigrationManager.upgrade(self.path_to_file, DatabaseType.Supply, redo_triggers=True)
        self.__log_setter()

    def close(self, clear_issues=False):
        """Closes database connection"""

        self.geotools.clear_layers()
        self.__start_end(clear_issues)
        self.logger.info(f"Network closed at {self.path_to_file}")
        remove_file_handler(self.logger, "LOGFILE")

        self.path_to_file = ""

    def set_debug(self, level=logging.DEBUG):
        """Sets logging to debug mode throughout the package.

        As a result of this method_call, logging will become extremely verbose. Use only when necessary

        Args:
            *level* (:obj:`int`): Logging level to be used (DEBUG:10, INFO:20, WARN:30, ERROR:40 CRITICAL:50)
        """
        self.__logging_level = level
        self.logger.setLevel(level)
        for ch in self.logger.handlers:
            ch.setLevel(self.__logging_level)

    def log_to_terminal(self):
        """Adds the terminal as a logging output"""
        ensure_stdout_handler(self.logger, logging.ERROR)

    @property
    def tools(self) -> Tools:
        """Tools for general manipulation of the network"""
        if not self.__checks_valid():
            raise Exception("Not a valid network")
        self.__tools__ = self.__tools__ or Tools(self.geotools, self.data_tables, self.path_to_file)
        return self.__tools__

    @property
    def transit(self) -> Transit:
        """Transit manipulation class"""
        if not self.__checks_valid():
            raise Exception("Not a valid network")
        self.__transit__ = self.__transit__ or Transit(self)
        return self.__transit__

    @property
    def active(self):
        """Active transport network creation class"""
        if not self.__checks_valid():
            raise Exception("Not a valid network")
        self.__active__ = self.__active__ or ActiveNetworks(self.geotools, self.data_tables)
        return self.__active__

    @property
    def checker(self):
        """Network checker class"""
        if not self.__checks_valid():
            raise Exception("Not a valid network")

        self.__checker__ = self.__checker__ or SupplyChecker(self.path_to_file)
        return self.__checker__

    @property
    def populate(self):
        """Network checker class"""
        if not self.__checks_valid():
            raise Exception("Not a valid network")

        from polaris.prepare.supply_tables.populate_tables import Populator

        return Populator(self.path_to_file)

    @property
    def diagnostics(self):
        """Network checker class"""
        if not self.__checks_valid():
            raise Exception("Not a valid network")

        self.__diagnostics__ = self.__diagnostics__ or Diagnostics(self.geotools, self.data_tables)
        return self.__diagnostics__

    @property
    def geo_consistency(self):
        """Geo-consistency analysis class"""
        if not self.__checks_valid():
            raise Exception("Not a valid network")

        self.__geo_consistency__ = self.__geo_consistency__ or GeoConsistency(self.geotools, self.data_tables)
        return self.__geo_consistency__

    @property
    def osm(self) -> OSM:
        if not self.__checks_valid():
            raise Exception("Not a valid network")
        self.__osm__ = self.__osm__ or OSM(self.path_to_file)
        return self.__osm__

    @property
    def geotools(self):
        if not self.__checks_valid():
            raise Exception("Not a valid network")

        self.__geotool__ = self.__geotool__ or Geo(self.path_to_file)
        return self.__geotool__

    @property
    def data_tables(self) -> DataTableCache:
        if not self.__checks_valid():
            raise Exception("Not a valid network")
        return DataTableCache(self.path_to_file)

    @property
    def consistency(self):
        """Network checker class"""
        if not self.__checks_valid():
            raise Exception("Not a valid network")
        self.__consistency__ = self.__consistency__ or Consistency(self.path_to_file)
        return self.__consistency__

    @property
    def ie(self) -> ImportExport:
        """Network Import-Export class"""

        if not self.__checks_valid():
            raise Exception("Not a valid network")
        return ImportExport(self.path_to_file)

    def get_location(self, location_id: int) -> Location:
        """Location object"""

        return Location(location_id, self.geotools, self.data_tables, None)

    def get_intersection(self, node: int) -> Intersection:
        """Network intersection class"""

        inter = Intersection(self.data_tables, self.path_to_file)
        inter.load(node)
        return inter

    def clear_editing_records(self):
        """ "Removes previously addressed records from the editing table"""
        with commit_and_close(self.path_to_file, spatial=True) as conn:
            conn.execute("DELETE FROM Editing_table WHERE checked=1;")
            conn.commit()
            conn.execute("VACUUM;")

    def clear_log(self):
        """Clears log file"""

        log_path = join(dirname(self.path_to_file), "polaris.log")
        with open(log_path, "w") as _:
            pass

    def __checks_valid(self) -> bool:
        if not os.path.isfile(self.path_to_file):
            self.logger.error("You don't have a valid project open. Fix that and try again")
            return False
        return True

    def __gets_srid(self):
        self.srid = get_srid(database_path=self.path_to_file)
        c = constants()
        c.srid["srid"] = self.srid

    def __setattr__(self, instance, value):
        if instance == "srid":
            crs = CRS.from_user_input(value)
            if crs.coordinate_system.axis_list[0].unit_name not in ["meter", "metre"]:
                raise ValueError("SRID needs to correspond to a CRS with units in meters")
        self.__dict__[instance] = value

    def __run_consistency(self, look_into_consistency):
        cons = Consistency(self.path_to_file)
        if look_into_consistency:
            cons.enforce()
        else:
            if len(cons.errors) > 0:
                self.logger.error(f"There are {len(cons.errors)} consistency issues to be addressed the network")

    def __log_setter(self):
        self.logger = logging.getLogger("polaris")
        self.logger.setLevel(self.__logging_level)

        add_file_handler(self.logger, self.__logging_level, Path(self.path_to_file).parent)

        for ch in self.logger.handlers:
            ch.setLevel(self.__logging_level)

    def __start_end(self, look_into_consistency: bool):
        if self.has_edit_table(self.path_to_file):
            self.__run_consistency(look_into_consistency)

    @staticmethod
    def has_edit_table(path_to_file):
        with read_and_close(path_to_file, spatial=False) as conn:
            return has_table(conn, "Editing_Table")

    def __network_dependencies(self):
        for req in ["shapely", "geopandas", "aequilibrae"]:
            check_dependency(req, raise_error=True)
