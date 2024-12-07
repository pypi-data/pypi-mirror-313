-- Copyright (c) 2024, UChicago Argonne, LLC
-- BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
--@ An output table for the freight tours synthesized by CRISTAL,
--@ including their mode, volume, trip type,
--@ origin and destination

CREATE TABLE Freight_Delivery (
    "trip_id"               INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, --@ unique identifier of this freight trip 
    "tour_id"               INTEGER NOT NULL DEFAULT 0, --@ Freight tour identifier
    "carrier_estab_id"      INTEGER NOT NULL DEFAULT 0, --@ Carrier establishment identifier (foreign key to the Establishment table)
    "supplier_estab_id"     INTEGER NOT NULL DEFAULT 0, --@ Supplier establishment identifier (foreign key to the Establishment table)
    "receiver_estab_id"     INTEGER NOT NULL DEFAULT 0, --@ Receiver establishment identifier (foreign key to the Establishment table)
    "origin_loc_id"         INTEGER NOT NULL DEFAULT 0, --@ The trip's origin location (foreign key to the Location table)
    "destination_loc_id"    INTEGER NOT NULL DEFAULT 0, --@ The trip's destination location (foreign key to the Location table)
    "volume"                INTEGER NOT NULL DEFAULT 0, --@ Shipment volume (units: lbs.)
    "good_type"             INTEGER NOT NULL DEFAULT 0, --@ Type of good being shipped (TODO: Add the enum)
    "mode_type"             INTEGER NOT NULL DEFAULT 0, --@ Mode used to make the deliver !Vehicle_Type_Keys!
    "pickup_trip"           INTEGER NOT NULL DEFAULT 0, --@ boolean flag - is this a pick up trip?
    "OHD"                   INTEGER NOT NULL DEFAULT 0  --@ boolean flag - is this delivery performed in off hours?
);
