-- Copyright (c) 2024, UChicago Argonne, LLC
-- BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
--@ This table holds a list of database changes that have been made and that
--@ need to have consequences executed
--@ It will be deprecated, or its relevance greatly reduced, as spatial
--@ relationships between tables get enforced through spatial triggers
--@ leveraging Spatialite's KNN2

CREATE TABLE IF NOT EXISTS "Editing_Table" (
    issue           INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, --@ unique identifier
    table_name      TEXT,    --@ The name of the table that this editing record refers to
    id_field        TEXT,    --@ The field that holds the primary key for the table that this editing record refers to
    id_value        TEXT,    --@ The value of the primary key for the table that this editing record refers to
    field           TEXT,    --@ The field that has been edited
    field_value     TEXT,    --@ The value that the field has been changed to
    "operator"      TEXT,    --@ Whether the editing was an addition, deletion or editing
    checked         INTEGER, --@ 1 if the change has been made consistent, 0 if it is still open
    recorded_change TEXT
    );

create INDEX IF NOT EXISTS editing_table_idx ON editing_table (issue);
create INDEX IF NOT EXISTS editing_table_tname_idx ON editing_table (table_name);
create INDEX IF NOT EXISTS editing_checked_idx ON editing_table (checked);
