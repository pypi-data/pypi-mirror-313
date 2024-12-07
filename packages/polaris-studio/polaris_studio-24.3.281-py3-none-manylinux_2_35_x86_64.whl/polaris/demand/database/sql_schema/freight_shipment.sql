-- Copyright (c) 2024, UChicago Argonne, LLC
-- BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
--@ An output table for the freight shipment attributes,
--@ and mode choice results, including: supplier, receiver
--@ commodity type, mode used, shipment size, total trade volume and cost 
--@ between buyers and suppliers, and if that particular 
--@ shipment is simulated that day or no

CREATE TABLE Freight_Shipment (
    "shipment_id"       INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, --@ The unique identifier of this shipment 
    "supplier_estab_id" INTEGER NOT NULL DEFAULT 0,                 --@ The supplier of this shipment (foreign key to establishment table)
    "receiver_estab_id" INTEGER NOT NULL DEFAULT 0,                 --@ The receiver of this shipment (foreign key to establishment table)
    "commodity"         INTEGER NOT NULL DEFAULT 0,                 --@ The commodity type of the shipment (none, bulk, intermediate, finished) - TODO: corresponds to the FreightCommodityType enum
    "mode"              INTEGER NOT NULL DEFAULT 0,                 --@ The freight mode used for the shipment (truck, rail, air, courier) - TODO: corresponds to the FreightModeType enum
    "total_cost"        INTEGER NOT NULL DEFAULT 0,                 --@ Total shipping cost of annual shipments (units: $USD)
    "demand_tons"       REAL             DEFAULT 0,                 --@ Total annual shipments (units: tons)
    "shipment_size_lbs" INTEGER NOT NULL DEFAULT 0,                 --@ Shipment size (units: lbs.)
    "days_btw_orders"   INTEGER NOT NULL DEFAULT 0,                 --@ Time interval between two subsequent orders (units: days)
    "is_simulated"      INTEGER NOT NULL DEFAULT 0                  --@ boolean flag - is the movement of this shipment simulated this day?
);
