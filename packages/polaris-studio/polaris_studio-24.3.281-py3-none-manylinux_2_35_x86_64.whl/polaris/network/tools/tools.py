# Copyright (c) 2024, UChicago Argonne, LLC
# BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
import os
from typing import Dict

import geopandas as gpd
import numpy as np
import pandas as pd

from polaris.network.active.active_networks import ActiveNetworks
from polaris.network.consistency.consistency import Consistency
from polaris.network.consistency.geo_consistency import GeoConsistency
from polaris.network.consistency.network_objects.location_links import (
    location_links_builder,
    loc_link_candidates,
)
from polaris.network.data.data_table_cache import DataTableCache
from polaris.network.utils.srid import get_srid
from polaris.network.starts_logging import logger
from polaris.network.tools.break_links import BreakLinks2Max
from polaris.network.tools.create_connections import CreateConnections
from polaris.network.tools.geo import Geo
from polaris.network.utils.worker_thread import WorkerThread
from polaris.utils.database.db_utils import commit_and_close
from polaris.utils.signals import SIGNAL


class Tools(WorkerThread):
    """Tools for general manipulation of the network

    To ensure that network links are no longer than a certain threshold (e.g. 1,000m), one can do the following

    ::

        project = Network()
        project.open(project_file_path)
        tools.break_links(1000)
        project.close()
    """

    tooling = SIGNAL(object)

    def __init__(self, geo_tools: Geo, data_tables: DataTableCache, path_to_file: os.PathLike):
        WorkerThread.__init__(self, None)
        self.srid = get_srid(database_path=path_to_file)
        self.geo_tools = geo_tools
        self.data_tables = data_tables
        self.logger = logger
        self.path_to_file = path_to_file
        self.__works_to_do: Dict[str, list] = {}

    def break_links(self, max_length: float, rebuild_network=True) -> None:
        """Breaks all links in the road network in such a way that no link is longer than the maximum threshold.
        Links are broken in equal parts. It also enforces consistency after breaking links.

        Args:
            *max_length* (:obj:`float`): Maximum length of any link in the roadway network
            *rebuild_network* (:obj:`bool`): True if required to rebuild the network. DO NOT USE FALSE
        """
        brk_lnks = BreakLinks2Max(max_length, self.path_to_file)
        brk_lnks.breaking = self.tooling
        cons = Consistency(self.path_to_file)
        cons.enforce()

        brk_lnks.execute()

        with commit_and_close(self.path_to_file, spatial=True) as conn:
            conn.execute("DELETE FROM Editing_table")
            conn.commit()

            if not rebuild_network:
                self.tooling.emit(["finished_breaking_procedure"])
                return

            self.geo_tools.clear_cache()
            self.data_tables.refresh_cache()
            wn = ActiveNetworks(self.geo_tools, self.data_tables)
            wn.__do_update_associations__ = False
            wn.build()

        self.geo_tools.clear_cache()
        self.data_tables.refresh_cache()
        gc = GeoConsistency(self.geo_tools, self.data_tables)
        gc.update_all()

        self.geo_tools.clear_cache()
        self.data_tables.refresh_cache()

        self.rebuild_intersections()
        self.rebuild_location_links()

        cons = Consistency(self.path_to_file)
        cons.enforce()
        self.tooling.emit(["finished_breaking_procedure"])

    def rebuild_location_links(self, maximum_distance: float = 300, multiple_links=True):
        """Rebuilds the **Location_Links** table completely

        This method should be called only after all updates to the **Location**
        table have been completed

        Args:
            *maximum_distance* (:obj:`float`): Maximum distance for which a link can be connected to a location (excludes closest link)
            *multiple_links* (:obj:`bool`): Connects each location to multiple links in the same block if True
            and only to the nearest link if false. Defaults to True
        """

        # Updates it all at once instead of method calling
        with commit_and_close(self.path_to_file, spatial=True) as conn:
            conn.execute("Delete from Location_links")
            conn.commit()

            if not multiple_links:
                s = "INSERT INTO Location_Links (location, link, distance) SELECT location, link, setback from Location"
                conn.execute(s)
                conn.commit()
                return

            self.logger.info("Searching for location link candidates")
            locs = self.geo_tools.get_geo_layer("location")[["location", "land_use", "geo"]]
            links_layer = self.geo_tools.get_geo_layer("link")[["link", "use_codes", "type", "geo"]]
            loc_links = loc_link_candidates(locs, links_layer, maximum_distance)

            self.logger.info("      Rebuilding Location Links")
            loc_links_result = location_links_builder(loc_links).sort_values(by=["location", "link"])

            self.logger.info("      Saving Location Links")
            loc_links_result.to_sql("Location_Links", conn, if_exists="append", index=False)

            sql = '''DELETE FROM Editing_Table WHERE table_name="Location_Links"'''
            conn.execute(sql)

    def rebuild_intersections(self, signals=None, signs=None):
        """Rebuilds all intersections and intersection controls

        Args:
            *signals* (:obj:[`list`, `str`], **Optional**): Rebuilds existing signals when not provided, When a list of
                                                            nodes, adds signals for them. May also be 'osm' or 'geometric'.
                                                            see documentation of **Intersection** for details
            *signs* (:obj:[`list`, `str`], **Optional**): List of node IDs with stop signs. When **None**, rebuilds existing signs,
                                                          and when **[]** evaluates all non-signalized intersections
        """
        c = CreateConnections(self.data_tables, self.path_to_file, signals, signs)
        c.connecting = self.tooling
        c.execute()
        self.tooling.emit(["finished_rebuilding_procedure"])

    def rebuild_location_parking(self, maximum_distance: float):
        """Rebuilds the Location_Parking table

        it also creates synthetic Parking entries for each location without parking"""
        with commit_and_close(self.path_to_file, spatial=True) as conn:
            # We collect all the data we need from the model
            park_gdf = self.data_tables.get_geo_layer(table_name="Parking", conn=conn).reset_index()
            loc_gdf = self.data_tables.get_geo_layer(table_name="Location", conn=conn).reset_index()

            # Do the spatial join for the distance specified by the user
            # But we must use only the parking locations that are NOT residential
            park_is_loc = park_gdf.loc[park_gdf["type"] == "location", :]
            gdf1 = gpd.GeoDataFrame(park_is_loc[["parking"]], geometry=park_is_loc.geometry)
            gdf2 = gpd.GeoDataFrame(loc_gdf[["land_use", "location"]], geometry=loc_gdf.geometry)
            park_is_loc = gpd.sjoin(gdf1, gdf2, how="left")
            park_is_loc.land_use = park_is_loc.land_use.fillna(value="NONRES")
            park_is_res = park_is_loc[park_is_loc.land_use.str.lower().str.contains("residential")]
            park_locs_to_add = pd.DataFrame(park_is_res[["parking", "location"]])

            # And we move forward only with the non-residential parking spots
            park_gdf = park_gdf[~park_gdf.parking.isin(park_locs_to_add.parking)]
            park_gdf = gpd.GeoDataFrame(park_gdf[["parking"]], geometry=park_gdf.geometry, crs=park_gdf.crs)

            # We create a buffer of the desired distance and do a spatial join against the parkings
            loc_buff = gpd.GeoDataFrame(loc_gdf[["location"]], geometry=loc_gdf.buffer(maximum_distance))
            loc_buff = gpd.GeoDataFrame(loc_buff[["location"]], geometry=loc_buff.geometry, crs=loc_buff.crs)
            joined = gpd.sjoin(loc_buff, park_gdf, how="left")

            # We get what we found with the buffer search and concatenate with the residential parkings
            park_locs_to_add = pd.concat([park_locs_to_add, pd.DataFrame(joined[["location", "parking"]]).dropna()])

            # Now we have a set of locations for which we don't have a parking spot
            # We have to create parking spots for them
            missing_locs = loc_gdf[~loc_gdf.location.isin(park_locs_to_add.location.unique())]
            missing_locs = missing_locs.to_wkb()
            npc = [
                "offset",
                "setback",
                "link",
                "dir",
                "zone",
                "walk_link",
                "walk_offset",
                "bike_link",
                "bike_offset",
                "geo",
                "location",
            ]
            new_parks = pd.DataFrame(missing_locs[npc])

            if not new_parks.empty:
                max_park = conn.execute("SELECT coalesce(max(parking), 0) from Parking;").fetchone()[0]
                new_parks = new_parks.assign(parking=np.arange(new_parks.shape[0]) + max_park + 1)
                cols = [
                    "parking",
                    "link",
                    "dir",
                    "zone",
                    "offset",
                    "setback",
                    "walk_link",
                    "walk_offset",
                    "bike_link",
                    "bike_offset",
                    "geo",
                ]
                data = new_parks[cols].to_records(index=False)
                sql = f"""insert into Parking(parking, link, dir, zone, offset, setback, "type", "start", "end",
                                             space, time_in, time_out, hourly, daily, walk_link,
                                             walk_offset, bike_link, bike_offset, geo)
                                             values (?, ?, ?, ?, ?, ?, 'location', 0, 0, 1, 0, 86400, 0, 0, ?, ?,
                                             ?, ?, GeomFromWKB(?, {get_srid(conn=conn)}));"""
                conn.executemany(sql, data)
                sql = """DELETE FROM Editing_Table WHERE table_name="Parking" and id_value>?"""
                conn.execute(sql, [max_park])
                park_locs_to_add = pd.concat([park_locs_to_add, pd.DataFrame(new_parks[["location", "parking"]])])

            conn.execute("DELETE FROM Location_Parking")
            conn.commit()
            df = park_locs_to_add.drop_duplicates(subset=["location", "parking"]).assign(distance=0, id=None)

            df.to_sql("Location_Parking", con=conn, if_exists="append", index=False)

    def _set_work_to_do(self, job):
        self.__works_to_do[job[0]] = job[1:]

    def doWork(self):
        """Runs work set in QGIS. Not for use in the Python interface"""

        for job, par in self.__works_to_do.items():
            getattr(self, job)(*par)
