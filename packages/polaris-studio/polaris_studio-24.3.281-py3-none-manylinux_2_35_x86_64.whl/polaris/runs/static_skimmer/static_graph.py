# Copyright (c) 2024, UChicago Argonne, LLC
# BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
from aequilibrae.paths.graph import Graph

from polaris.network.data.data_table_cache import DataTableCache


def build_graph(supply_pth: Path) -> Graph:
    links = DataTableCache(supply_pth).get_geo_layer("Link")
    nodes = DataTableCache(supply_pth).get_geo_layer("Node").drop(columns=["zone"])
    zones = DataTableCache(supply_pth).get_geo_layer("Zone")

    ltype = DataTableCache(supply_pth).get_table("Link_type").reset_index()[["link_type", "use_codes"]]
    links = links.merge(ltype, left_on="type", right_on="link_type")

    # Filter links
    links = links[links.use_codes.str.lower().str.contains("auto") | links.use_codes.str.lower().str.contains("truck")]

    # Let's shift the node IDs to make sure our zone numbers do not conflict with node IDs
    zn_max = zones.zone.max() + 1
    links.node_a += zn_max
    links.node_b += zn_max
    nodes.node += zn_max

    # Let's assert some things about the links so we can get everything we need for a static traffic assignment
    # First, capacities
    links = links.assign(capacity_ab=0, capacity_ba=0)
    capacity_dict = {"LOCAL": 300, "COLLECTOR": 400, "MINOR": 600, "MAJOR": 750, "RAMP": 400, "EXPRESSWAY": 1200}
    for ltype, lanecap in capacity_dict.items():
        for capfield, lanesfield in [("capacity_ab", "lanes_ab"), ("capacity_ba", "lanes_ba")]:
            links.loc[links["type"].str.upper() == ltype, capfield] = (
                links.loc[links["type"].str.upper() == ltype, lanesfield] * lanecap
            )

    # Now free-flow travel times in minutes
    links = links.assign(time_ab=(links["length"] / links.fspd_ab) / 60, time_ba=(links["length"] / links.fspd_ba) / 60)
    links.replace([np.inf, -np.inf], 0, inplace=True)
    # Division can return infinite values, so let's fix them

    # Now, directions
    links = links.assign(direction=0, source="supply_file")
    links.loc[links.lanes_ab == 0, "direction"] = -1
    links.loc[links.lanes_ba == 0, "direction"] = 1
    links = links[links.lanes_ab + links.lanes_ba > 0]

    # Now we get only the columns we need
    links_net = links[
        ["link", "length", "node_a", "node_b", "capacity_ab", "capacity_ba", "time_ab", "time_ba", "direction"]
    ]
    links_net = links_net.rename(
        columns={"link": "link_id", "node_a": "a_node", "node_b": "b_node", "length": "distance"}
    )

    links_net = links_net.assign(connector_penalty=0)
    # Polaris models do not have centroids and connectors, so we need to create them
    # Get nodes and zones
    zones = gpd.GeoDataFrame(zones.zone, geometry=zones.geometry.centroid, crs=zones.crs)

    # Only get the nodes that are actually in the network
    nodes = nodes[(nodes.node.isin(links_net.a_node)) | (nodes.node.isin(links_net.b_node))]

    connectors = nodes.sjoin_nearest(zones, how="left", distance_col="distance").sort_values(by=["distance"])
    connectors = connectors.groupby(["zone"]).head(10).reset_index(drop=True).sort_values(by=["zone"])
    connectors = connectors[["node", "zone", "distance"]]

    connectors2 = zones.sjoin_nearest(nodes, how="left", distance_col="distance").sort_values(by=["distance"])
    connectors2 = connectors2.groupby(["zone"]).head(2).reset_index(drop=True).sort_values(by=["zone"])
    connectors2 = connectors2[["node", "zone", "distance"]]

    connectors = pd.concat([connectors, connectors2], ignore_index=True).drop_duplicates(["node", "zone"])
    # Create connectors with speed of 12 m/s, or 43 km/h
    # This is to make sure that the connector to the closest node will be used, unless not actually connected
    connectors = connectors.assign(
        direction=0,
        capacity_ab=1000000,
        capacity_ba=1000000,
        time_ab=connectors["distance"] / 12 / 60,
        time_ba=connectors["distance"] / 12 / 60,
        connector_penalty=connectors["distance"] * 20,
        source="centroid_connector",
    )
    connectors = connectors.assign(link_id=np.arange(connectors.shape[0]) + links_net.link_id.max() + 1)
    connectors = connectors.rename(columns={"zone": "a_node", "node": "b_node"})
    connectors.distance *= 2  # Compensates for the internal detour missed by using connectors

    graph = Graph()
    graph.network = pd.concat([links_net, connectors], ignore_index=True)
    graph.prepare_graph(zones.zone.to_numpy())
    graph.set_graph("time")
    graph.set_skimming(["distance", "time"])
    graph.set_blocked_centroid_flows(True)

    return graph
