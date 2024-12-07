# Copyright (c) 2024, UChicago Argonne, LLC
# BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
import os

from polaris.network.ie.gmns.export_gmns import export_to_gmns
from polaris.network.ie.gmns.import_gmns import import_from_gmns
from polaris.network.utils.network_dump_loader import LoadNetworkDump
from polaris.utils.database.database_dumper import dump_database_to_csv
from polaris.utils.database.db_utils import read_and_close


class ImportExport:
    """
    This class allows for importing and exporting to the GMNS format.
    """

    def __init__(self, supply_database_path: os.PathLike):
        self.supply_database = supply_database_path

    def dump(self, folder_name: str) -> None:
        """Creates a folder and dumps all tables in the database to CSV files

        Args:
            *folder_name* (:obj:`str`): Folder where the dump files are to be placed"""

        # self.__run_consistency()
        with read_and_close(self.supply_database, spatial=True) as conn:
            dump_database_to_csv(conn, folder_name)

    def restore(self, folder_name: os.PathLike, jumpstart=False) -> None:
        """Reloads the network from a previous dump to csv

        Args:
            *folder_name* (:obj:`str`): Folder where the dump files are located
            *jumpstart* (:obj:`bool`): Copies base sql already initialized with spatialite base tables. It saves about
                                       a minute of runtime.
        """

        if not os.path.isdir(folder_name):
            raise FileNotFoundError
        network_loader = LoadNetworkDump(folder_name, jumpstart)
        network_loader.doWork()

    def from_gmns(self, gmns_folder: str, crs: str):
        """Imports the network data from the GMNS format

        Args:
            *gmns_folder* (:obj:`str`): Folder where the GMNS files are located
            *crs* (:obj:`str`): CRS of the exported dataset in readable format by PyProj (e.g. 'epsg:4326')"""
        import_from_gmns(gmns_folder, crs, self.supply_database)

    def to_gmns(self, gmns_folder: str, crs: str):
        """Exports the network data to the GMNS format

        Args:
            *gmns_folder* (:obj:`str`): Folder where the GMNS files are to be placed
            *crs* (:obj:`str`): CRS of the exported dataset in readable format by PyProj (e.g. 'epsg:4326')"""
        with read_and_close(self.supply_database, spatial=True) as conn:
            export_to_gmns(gmns_folder, crs, conn, self.supply_database)

    def __run_consistency(self):
        from polaris.network.consistency.consistency import Consistency

        Consistency(self.supply_database).enforce()
