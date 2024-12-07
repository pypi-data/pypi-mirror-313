-- Copyright (c) 2024, UChicago Argonne, LLC
-- BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
--@ Industry make use table contains a susbset of
--@ the input-output tables of the Bureau of Economic Analysis that defines
--@ the purchased values between sectors
--@

CREATE TABLE Industry_Make_Use (
    "naics3_make"   INTEGER NOT NULL DEFAULT 0, --@ The 3-digit NAICS code of the sender industry sector
    "naics3_use"    INTEGER NOT NULL DEFAULT 0, --@ The 3-digit NAICS code of the recipient industry sector
    "purchase_valM" REAL             DEFAULT 0  --@ The purchase value (units: $USD millions)
);
