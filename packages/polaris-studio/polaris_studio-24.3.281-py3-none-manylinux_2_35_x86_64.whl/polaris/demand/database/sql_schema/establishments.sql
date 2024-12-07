-- Copyright (c) 2024, UChicago Argonne, LLC
-- BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
--@ The establishments table include endogenous establishments
--@ and a subset of the exogenous establishments and their
--@ attributes: parent firm, sector, county, employees,
--@ revenue, endogenous/exogenous, type of goods, freight rates,
--@ points of entry, possible land uses
--@

CREATE TABLE Establishments (
    "estab_id"        INTEGER NOT NULL  PRIMARY KEY AUTOINCREMENT, --@ The unique identifier of this establishment 
    "firm_id"         INTEGER NOT NULL,            --@ The parent firm identifier (foreign key to the Firm table)
    "naics3"          INTEGER NOT NULL,            --@ The 3-digit NAICS code of the establishment
    "fips_cnty"       INTEGER NOT NULL,            --@ The county FIPS code of the establishment 
    "employees"       INTEGER NOT NULL  DEFAULT 0, --@ Number of employees
    "rev_1000_usd"    REAL              DEFAULT 0, --@ Establishment revenue (units: $USD thousands)
    "is_external"     INTEGER NOT NULL  DEFAULT 0, --@ 1, if an exogenous establishment, 0 if an endogenous establishment
    "fp_rate"         REAL              DEFAULT 0, --@ Freight production rate per empolyee (units: tons/employee)
    "fa_rate"         REAL              DEFAULT 0, --@ Freight attraction rate per empolyee (units: tons/employee)
    "good_prod"       INTEGER NOT NULL  DEFAULT 0, --@ Type of good produced by the establishment (none, bulk, intermediate, finished)
    "good_cons"       INTEGER NOT NULL  DEFAULT 0, --@ Type of good consumed by the establishment (none, bulk, intermediate, finished)
    "poe_truck"       INTEGER NOT NULL  DEFAULT 0, --@ Location of the highway point of entry/exit closest to the establishment (foreign key to the Location table)
    "poe_rail"        INTEGER NOT NULL  DEFAULT 0, --@ Location of the Railyard point of entry/exit closest to the establishment (foreign key to the Location table)
    "poe_air"         INTEGER NOT NULL  DEFAULT 0, --@ Location of the Airport point of entry/exit closest to the establishment (foreign key to the Location table)
    "ohd_accept"      INTEGER NOT NULL  DEFAULT 0, --@ boolean flag - can this establishment accept off-hour deliveries?
    "land_use"        INTEGER NOT NULL  DEFAULT 0, --@ Which types of land use can be used by the establishment (TODO: Add FreightLandUse enum when freight branch is merged)

    CONSTRAINT firm_fk FOREIGN KEY (firm_id)
    REFERENCES Firms (firm_id) DEFERRABLE INITIALLY DEFERRED
);
