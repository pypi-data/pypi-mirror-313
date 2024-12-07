-- Copyright (c) 2024, UChicago Argonne, LLC
-- BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
--@ Firms table have the attributes of the parent  
--@ firm: employment, sector, employees, revenue, 
--@ percent profit, market value
--@

CREATE TABLE Firms (
    "firm_id"           INTEGER NOT NULL PRIMARY KEY, --@ The unique identifier of this firm
    "naics3_firm"       INTEGER NOT NULL DEFAULT 0,   --@ The 3-digit NAICS code of the firm
    "total_estabs"      INTEGER NOT NULL DEFAULT 0,   --@ Total number of member establishments of the firm
    "total_employees"   INTEGER NOT NULL DEFAULT 0,   --@ Total number of employees of the firm
    "rev_mil_usd"       REAL             DEFAULT 0,   --@ The revenue of the firm (units: $USD millions)
    "pct_profit"        REAL             DEFAULT 0,   --@ Percentage profit of the firm
    "market_val"        REAL             DEFAULT 0    --@ Market value of the firm (units: $USD millions)
);
