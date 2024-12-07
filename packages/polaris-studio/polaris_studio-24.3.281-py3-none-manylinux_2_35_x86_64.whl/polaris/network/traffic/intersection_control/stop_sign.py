# Copyright (c) 2024, UChicago Argonne, LLC
# BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
from sqlite3 import Connection

import pandas as pd

from polaris.network.consistency.link_types_constants import RAMP, FREEWAY, EXPRESSWAY


class StopSign:
    def __init__(self, intersection):
        from polaris.network.traffic.intersec import Intersection

        self.inter: Intersection = intersection
        self.stop_signs = []

    def re_compute(self):
        # No stop signs if there are no conflicts
        no_sign = [RAMP, FREEWAY, EXPRESSWAY]

        self.stop_signs.clear()
        if len(self.inter.incoming) <= 1:
            return

        ranks = [lnk.link_rank for lnk in self.inter.incoming]
        min_ranks = min(ranks)
        no_express = [x for x in ranks if x not in no_sign]
        has_express = len(no_express) != len(ranks)
        ALL_STOP = "ALL_STOP" if not has_express else "STOP"
        ranks = [lnk.link_rank for lnk in self.inter.incoming if lnk.link_rank not in no_sign]

        if len(self.inter.incoming) == 2:
            all_links = {lnk.link for lnk in self.inter.incoming + self.inter.outgoing}
            cardinals = sorted([lnk.cardinal for lnk in self.inter.incoming])

            # These are the two situations that would end with no need for a stop sign
            if cardinals in [["NB", "SB"], ["EB", "WB"]] or len(all_links) <= 2:
                return

        if len(self.inter.incoming) > 4:
            self.stop_signs = [
                [lnk.link, lnk.direction, self.inter.node, ALL_STOP]
                for lnk in self.inter.incoming
                if lnk.link_rank not in no_sign
            ]
            return

        # No stop signs are allowed in the intersection between ramps and freeways
        if no_express == []:
            return

        if len(set(ranks)) == 1:
            self.stop_signs = [
                [lnk.link, lnk.direction, self.inter.node, ALL_STOP]
                for lnk in self.inter.incoming
                if lnk.link_rank not in no_sign
            ]
        else:
            cardinals = sorted([lnk.cardinal for lnk in self.inter.incoming if lnk.link_rank == min_ranks])
            if len(cardinals) == 1 or cardinals in [["NB", "SB"], ["EB", "WB"]]:
                self.stop_signs = [
                    [lnk.link, lnk.direction, self.inter.node, "STOP"]
                    for lnk in self.inter.incoming
                    if lnk.link_rank > min_ranks and lnk.link_rank not in no_sign
                ]
            else:
                self.stop_signs = [
                    [lnk.link, lnk.direction, self.inter.node, ALL_STOP]
                    for lnk in self.inter.incoming
                    if lnk.link_rank not in no_sign
                ]

    def save(self, conn: Connection):
        if not self.stop_signs:
            return
        self.data.to_sql("Sign", conn, if_exists="append", index=False)

    @property
    def data(self):
        return pd.DataFrame(self.stop_signs, columns=["link", "dir", "nodes", "sign"])
