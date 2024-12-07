# Copyright (c) 2024, UChicago Argonne, LLC
# BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
from os import PathLike

from polaris.network.utils.srid import get_srid
from polaris.network.ie.gmns.importer.import_links import import_gmns_links
from polaris.network.ie.gmns.importer.import_locations import import_gmns_locations
from polaris.network.ie.gmns.importer.import_nodes import import_gmns_nodes
from polaris.network.ie.gmns.importer.import_zones import import_gmns_zones
from polaris.utils.database.db_utils import commit_and_close
from polaris.utils.optional_deps import check_dependency


def import_from_gmns(gmns_folder: str, crs: str, path_to_file: PathLike):
    proj_crs = get_srid(path_to_file)

    transformer = None
    if crs.lower() != "epsg:{proj_crs}":
        check_dependency("pyproj")
        from pyproj import Transformer

        transformer = Transformer.from_crs(crs, f"epsg:{proj_crs}", always_xy=True)

    with commit_and_close(path_to_file, spatial=True) as conn:
        import_gmns_nodes(gmns_folder, transformer, conn)
        import_gmns_links(gmns_folder, transformer, conn, path_to_file)
        import_gmns_zones(gmns_folder, transformer, conn)
        import_gmns_locations(gmns_folder, transformer, conn, path_to_file)
