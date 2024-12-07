# Copyright (c) 2024, UChicago Argonne, LLC
# BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
from pathlib import Path

import pandas as pd


def get_csv_table(table_path: Path) -> pd.DataFrame:
    def clear_colum_index_name(df: pd.DataFrame):
        df.columns = [x.replace("index", "_index") for x in df.columns]  # type: ignore
        return df

    schema_path = table_path.parent / (str(table_path.stem) + ".schema")
    if schema_path.exists():
        schema = pd.read_csv(schema_path)
        if schema.pk.sum():
            pk = schema[schema.pk == 1].name.values[0]
            return clear_colum_index_name(pd.read_csv(table_path, index_col=pk.lower(), low_memory=False))
    return clear_colum_index_name(pd.read_csv(table_path))
