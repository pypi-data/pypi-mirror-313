# Copyright (c) 2024, UChicago Argonne, LLC
# BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
import shutil
import subprocess
from datetime import datetime, timezone
from os.path import join, exists
from pathlib import Path

from polaris.network.create.triggers import create_network_triggers, delete_network_triggers
from polaris.network.utils.unzips_spatialite import unzips_base_spatialite
from polaris.utils.database.database_loader import load_database_from_csvs, GeoInfo
from polaris.utils.database.db_utils import commit_and_close, write_about_model_value
from polaris.utils.database.migration_manager import MigrationManager
from polaris.utils.database.spatialite_utils import get_spatialite_version, spatialize_db
from polaris.utils.database.standard_database import StandardDatabase, DatabaseType
from polaris.utils.dir_utils import mkdir_p
from polaris.utils.signals import SIGNAL


def restore_project_from_csv(target_dir, git_dir, project_name, overwrite):
    mkdir_p(target_dir)

    if target_dir != git_dir:
        if overwrite:
            shutil.rmtree(target_dir)
        shutil.copytree(git_dir, target_dir, ignore=_ignore_files, dirs_exist_ok=True)

    signal = SIGNAL(object)

    network_file_name = join(target_dir, f"{project_name}-Supply.sqlite")
    demand_file_name = join(target_dir, f"{project_name}-Demand.sqlite")

    create_demand_db_from_csv(demand_file_name, join(git_dir, "demand"), signal, overwrite)
    create_network_db_from_csv(network_file_name, join(git_dir, "supply"), signal, overwrite)


def _ignore_files(directory, contents):
    ignore = directory.endswith("supply") or directory.endswith("demand") or ".git" in directory
    return contents if ignore else []


def create_demand_db_from_csv(demand_db_name, demand_csv_dir, signal=None, overwrite=False):
    if exists(demand_db_name) and not overwrite:
        raise RuntimeError(f"Network DB [{demand_db_name}] already exists and overwrite = False")
    Path(demand_db_name).unlink(missing_ok=True)
    demand_db = StandardDatabase.for_type(DatabaseType.Demand)
    with commit_and_close(demand_db_name, missing_ok=True, spatial=True) as conn:
        demand_db.create_tables(conn, None, add_defaults=False)
        load_database_from_csvs(demand_csv_dir, conn, demand_db.default_values_directory, signal)

    MigrationManager.upgrade(demand_db_name, DatabaseType.Demand, redo_triggers=False)


def create_network_db_from_csv(network_db_name, network_csv_dir, signal=None, overwrite=False, jumpstart=True):
    if exists(network_db_name) and not overwrite:
        raise RuntimeError(f"Network DB [{network_db_name}] already exists and overwrite = False")

    unzips_base_spatialite(jumpstart, network_db_name)
    with commit_and_close(network_db_name, spatial=True) as conn:
        spatialize_db(conn)
        geo_info = GeoInfo.from_folder(network_csv_dir)
        if not geo_info.is_geo_db:
            raise RuntimeError(f"Network csv folder [{network_csv_dir}] wasn't geo-spatial (missing srids.txt)")
        srid = geo_info.get_one_and_only_srid()

        supply_db = StandardDatabase.for_type(DatabaseType.Supply)

        supply_db.create_tables(conn, srid, add_defaults=False)
        delete_network_triggers(conn)
        load_database_from_csvs(network_csv_dir, conn, supply_db.default_values_directory, signal)

        MigrationManager.upgrade(network_db_name, DatabaseType.Supply, redo_triggers=False)
        create_network_triggers(conn, srid)

        write_about_model_value(conn, "Build time", datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%MZ"))
        write_about_model_value(conn, "Files source", str(network_csv_dir))
        write_about_model_value(conn, "SRID", str(srid))
        write_about_model_value(conn, "spatialite_version", get_spatialite_version(conn))
        try:
            git_sha = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=str(Path(network_csv_dir).parent))
        except Exception:
            git_sha = "not found"
        finally:
            write_about_model_value(conn, "Git SHA", git_sha)
