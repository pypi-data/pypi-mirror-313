-- Copyright (c) 2024, UChicago Argonne, LLC
-- BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
--@ An output table for the establishments trade partners
--@ and their assets, including: heavy and medium duty trucks,
--@ total tonnage produced and attracted, their suppliers, 
--@ and carriers

CREATE TABLE Establishments_Attributes (
    "estab_id"              INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, --@ The establishment identifier
    "location_id"           INTEGER NOT NULL DEFAULT 0, --@ The selected location of the establishment (foreign key to the Location table)
    "medium_duty_trucks"    INTEGER NOT NULL DEFAULT 0, --@ Number of medium duty trucks owned by the establishment
    "heavy_duty_trucks"     INTEGER NOT NULL DEFAULT 0, --@ Number of heavy duty trucks owned by the establishment
    "freight_produced_ton"  REAL             DEFAULT 0, --@ Total outbound tonnage by the establishment (units: tons)
    "freight_attracted_ton" REAL             DEFAULT 0, --@ Total inbound tonnage by the establishment (units: tons)
    "supplier1_estab_id"    INTEGER NOT NULL DEFAULT 0, --@ First supplier establishment identifier (foreign key to the Establishment table)
    "supplier2_estab_id"    INTEGER NOT NULL DEFAULT 0, --@ Second supplier establishment identifier (foreign key to the Establishment table)
    "carrier_estab_id"      INTEGER NOT NULL DEFAULT 0, --@ Carrier establishment identifier (foreign key to the Establishment table)
    "firm_dc_location"      INTEGER NOT NULL DEFAULT 0  --@ The selected location of the parent firm in the region (foreign key to the Location table)
);
