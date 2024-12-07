# Copyright (c) 2024, UChicago Argonne, LLC
# BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
import sqlite3
import warnings
from os import PathLike
from typing import Dict, Optional

import pandas as pd

from polaris.network.utils.srid import get_srid
from polaris.network.starts_logging import logger
from polaris.utils.database.db_utils import read_and_close
from polaris.utils.optional_deps import check_dependency
from polaris.utils.structure_finder import find_table_index, find_table_fields


class DataTableCache:
    def __init__(self, network_file: PathLike):
        self.logger = logger
        self.__cache_warning = False
        self.__data_tables: Dict[str, pd.DataFrame] = {}
        self._network_file = network_file

    def get_table(self, table_name: str, conn=None) -> pd.DataFrame:
        """Returns a pandas dataframe for a project table

        For geo-enabled tables, the geometry column is filled with Shapely objects

        Args:
            *table_name* (:obj:`str`): Network table name
            *conn* `Optional` (:obj:`sqlite3.Connection`): Connection to the network database
        Return:
            *dataframe* (:obj:`pd.DataFrame`): Corresponding to the database
        """

        tn = table_name.lower()
        if tn not in self.__data_tables:
            with conn or read_and_close(self._network_file, spatial=True) as connec:
                self.__data_tables[tn] = self.__build_layer(table_name, connec)
        elif not self.__cache_warning:
            self.__cache_warning = True
            warnings.warn("THIS TABLE WAS CACHED, USE WITH CAUTION")
        return self.__data_tables[tn]

    def plotting_layer(self, table_name: str, conn: Optional[sqlite3.Connection] = None) -> pd.DataFrame:
        """Returns a pandas dataframe for a project table with geometry formatted as WKT for plotting.
        Layers are always projected to 4326 before they are returned

        Args:
            *table_name* (:obj:`str`): Network table name
            *conn* `Optional` (:obj:`sqlite3.Connection`): Connection to the network database
        Return:
            *dataframe* (:obj:`pd.DataFrame`): Corresponding to the database
        """
        with conn or read_and_close(self._network_file, spatial=True) as connec:
            return self.__build_layer(table_name, connec, "wkt")

    def get_geo_layer(self, table_name: str, conn: Optional[sqlite3.Connection] = None):
        check_dependency("geopandas")
        import geopandas as gpd

        with conn or read_and_close(self._network_file, spatial=True) as conn:
            fields, _, geo_field = find_table_fields(conn, table_name)
            if geo_field is None:
                raise ValueError("Not a geo layer")
            fields = [f'"{x}"' for x in fields]
            fields.append("Hex(ST_AsBinary(geo)) as geo")
            keys = ",".join(fields)
            sql = f"select {keys} from '{table_name}' WHERE geo IS NOT null;"
            return gpd.GeoDataFrame.from_postgis(sql, conn, geom_col="geo", crs=get_srid(conn=conn))

    def __build_layer(self, table_name: str, conn: sqlite3.Connection, geo_type="wkb"):
        fields, _, geo_field = find_table_fields(conn, table_name)
        fields = [f'"{x}"' for x in fields]
        if geo_field is not None:
            if geo_type == "wkb":
                fields.append('ST_AsBinary("geo") geo')
            else:
                fields.append("ST_AsText(ST_Transform(geo, 4326)) geo")
        keys = ",".join(fields)
        df = pd.read_sql_query(f"select {keys} from '{table_name}'", conn)
        idx = find_table_index(conn, table_name)
        if idx is not None:
            df.set_index(idx, inplace=True)
        return df

    def refresh_cache(self, table_name="") -> None:
        """Refreshes a table in memory. Necessary when a table has been edited in disk

        Args:
           *table_name* (:obj:`str`) Name of the table to be refreshed in memory. Defaults to '', which refreshes
           all tables
        """
        if table_name == "":
            self.__data_tables.clear()
        else:
            if table_name.lower() in self.__data_tables:
                _ = self.__data_tables.pop(table_name.lower())
                self.logger.debug(f"Refreshed table in memory: {table_name}")
            else:
                self.logger.debug(f"Attempted to refresh a table that is not in memory: {table_name}")
