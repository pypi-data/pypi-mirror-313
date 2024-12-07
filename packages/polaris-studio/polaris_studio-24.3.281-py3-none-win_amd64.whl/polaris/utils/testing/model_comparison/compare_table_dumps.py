# Copyright (c) 2024, UChicago Argonne, LLC
# BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
from pathlib import Path
from typing import List

from polaris.utils.testing.model_comparison.compare_tables import compare_tables
from polaris.utils.testing.model_comparison.get_csv_table import get_csv_table


def compare_table_dumps(old_path: Path, new_path: Path) -> List[str]:
    new_files = [x.name for x in Path(new_path).glob("*.csv")]
    old_files = [x.name for x in Path(old_path).glob("*.csv")]
    report = []

    dropped_files = [x for x in old_files if x not in new_files]
    if dropped_files:
        report.extend(["**Dropped tables**:\n", f"{', '.join(dropped_files)}\n"])
    else:
        report.append("**No dropped tables**\n")

    added_files = [x for x in new_files if x not in old_files]
    if added_files:
        report.extend(["**New tables**:\n", f"{', '.join(added_files)}\n"])
    else:
        report.append("**No new tables**\n")

    # Compares one table at a time
    no_change = []
    table_changes = []
    for table in new_files:
        if table not in old_files:
            continue
        print(f"Comparing: {table}")
        table_report = compare_tables(get_csv_table(Path(old_path) / table), get_csv_table(Path(new_path) / table))
        if len(table_report):
            table_changes.append(f"\n * {table}:\n")
            table_changes.extend(table_report)
        else:
            no_change.append(table)

    if no_change:
        report.extend(["**Tables with no changes**:\n", f"{', '.join(no_change)}\n"])

    if table_changes:
        report.append("\n\n**Tables with changes**:")
        report.extend(table_changes)

    return report
