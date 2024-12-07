# Copyright (c) 2024, UChicago Argonne, LLC
# BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
import sqlite3
from typing import Optional

import pandas as pd

from .data_record import DataRecord


class LocParkBase(DataRecord):
    def __init__(
        self, element_id: int, table_name, geotool, data_table, data: pd.DataFrame, conn: Optional[sqlite3.Connection]
    ):
        self.dir: int
        self.setback: float
        self.link: int
        self.walk_link: Optional[int]
        self.bike_link: Optional[int]
        self.zone: int
        self.offset: float
        super().__init__(element_id, table_name, data_table, data, conn)
        from polaris.network.tools.geo import Geo

        self.geotool: Geo = geotool
        self.link_corrected = False
        self.walk_link_corrected = False
        self.bike_link_corrected = False
        self.zone_corrected = False

    def update_link(self, conn: sqlite3.Connection, force_update=False, save=True):
        """Update the link and offset to this Point (Location or Parking)

        Setback is computed automatically through triggers

        Args:
            *force_update* (:obj:`bool`, optional ): Re-computes offset even the if the current link
            info is correct. Defaults to False
            *save* (:obj:`bool`, optional ): Saves it to the database after re-computation. Defaults to True
        """

        new_link = self.geotool.get_link_for_point_by_mode(self.geo, ["AUTO"])
        if new_link == self.link and not force_update:
            return
        ofst = self.geotool.offset_for_point_on_link(new_link, self.geo)
        if [new_link, round(ofst, 2)] != [self.link, round(self.offset, 2)]:
            self.link_corrected = True
            self.link, self.offset = new_link, ofst
            if save:
                self.save(conn=conn)
                sql = f'Update Editing_Table set checked=1 where table_name="{self._table_name}" and field="link" and id_value=?'
                conn.execute(sql, [self.id])
                conn.commit()

    def update_walk_link(self, conn: sqlite3.Connection, save=True):
        """Updates the walk_link to this Point (Location or Parking)

        Only considers links from Transit_Walk that correspond to a physical link in the Link table

        Args:
            *save* (:obj:`bool`, optional ): Saves it to the database after re-computation. Defaults to True

        """
        new_link = self.geotool.get_geo_item("walk_link", self.geo)
        if new_link != self.walk_link:
            self.walk_link = new_link
            self.walk_link_corrected = True
            if save:
                self.save(conn=conn)
                sql = 'Update Editing_Table set checked=1 where table_name=? and field="walk_link" and id_value=?'
                conn.execute(sql, [self._table_name, self.id])
                conn.commit()

    def update_bike_link(self, conn: sqlite3.Connection, save=True):
        """Updates the bike_link to this Point (Location or Parking)

        Only considers links from Transit_Bike that correspond to a physical link in the Link table

        Args:
            *save* (:obj:`bool`, optional ): Saves it to the database after re-computation. Defaults to True

        """
        new_link = self.geotool.get_geo_item("bike_link", self.geo)
        if new_link != self.bike_link:
            self.bike_link = new_link
            self.bike_link_corrected = True
            if save:
                self.save(conn)
                sql = 'Update Editing_Table set checked=1 where table_name=? and field="bike_link" and id_value=?'
                conn.execute(sql, [self._table_name, self.id])
                conn.commit()

    def update_zone(self, conn: sqlite3.Connection, save=True):
        """Updates the zone for this Point (Location or Parking)

        If the point is not contained inside a zone, it uses the closest.

        Args:
            *save* (:obj:`bool`, optional ): Saves it to the database after re-computation. Defaults to True
        """
        new_zone = self.geotool.get_geo_item("zone", self.geo)
        if new_zone != self.zone:
            self.zone = new_zone
            self.zone_corrected = True
            if save:
                self.save(conn)
                sql = f"""Update Editing_Table set checked=1
                          where table_name="{self._table_name}" and field="zone" and id_value=?"""
                conn.execute(sql, [self.id])
                conn.commit()
