# Copyright (c) 2024, UChicago Argonne, LLC
# BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
import dataclasses
from pathlib import Path

import pandas as pd


@dataclasses.dataclass
class NHTSDataset:
    households: pd.DataFrame
    persons: pd.DataFrame
    trips: pd.DataFrame
    vehicles: pd.DataFrame

    def filter_to_state(self, statecode: str):
        hh = self.households[self.households["HHSTATE"] == statecode].copy()
        per = self.persons[self.persons["HOUSEID"].isin(hh.HOUSEID)].copy()
        trip = self.trips[self.trips["HOUSEID"].isin(hh.HOUSEID)].copy()
        veh = self.vehicles[self.vehicles["HOUSEID"].isin(hh.HOUSEID)].copy()
        return NHTSDataset(hh, per, trip, veh)

    def save_nhts(self, dir: Path):
        dir.mkdir(exist_ok=True, parents=True)
        for f in ["hh", "per", "trip", "veh"]:
            f = dir / f"{f}pub.parquet"
            if f.exists():
                raise RuntimeError(f"File {f} already exists")

        self.households.to_parquet(dir / "hhpub.parquet")
        self.persons.to_parquet(dir / "perpub.parquet")
        self.trips.to_parquet(dir / "trippub.parquet")
        self.vehicles.to_parquet(dir / "vehpub.parquet")

    @staticmethod
    def from_dir(dir: Path):
        if (dir / "hhpub.csv").exists():
            return NHTSDataset.from_csv_dir(dir)
        elif (dir / "hhpub.parquet").exists():
            return NHTSDataset.from_parquet_dir(dir)
        else:
            raise FileNotFoundError(f"Couldn't find a hhold file in directory: {dir}")

    @staticmethod
    def from_csv_dir(dir: Path):
        hh = pd.read_csv(dir / "hhpub.csv")
        per = pd.read_csv(dir / "perpub.csv")
        trip = pd.read_csv(dir / "trippub.csv")
        veh = pd.read_csv(dir / "vehpub.csv")
        return NHTSDataset(hh, per, trip, veh)

    @staticmethod
    def from_parquet_dir(dir: Path):
        hh = pd.read_parquet(dir / "hhpub.parquet")
        per = pd.read_parquet(dir / "perpub.parquet")
        trip = pd.read_parquet(dir / "trippub.parquet")
        veh = pd.read_parquet(dir / "vehpub.parquet")
        return NHTSDataset(hh, per, trip, veh)
