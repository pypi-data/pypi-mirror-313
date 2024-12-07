-- Copyright (c) 2024, UChicago Argonne, LLC
-- BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
--@ Aggregated trajectory information for multimodal trips are logged in this table.
--@ None of these records are related to an auto-only trip.
--@
--@ Columns starting with `Est_` are values as estimated by the router, while columns starting with `Act_`
--@ represent the actual experienced value during simulation.

CREATE TABLE "Path_Multimodal" (
  "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,            --@ Unique identifier for this multimodal path
  "traveler_id" INTEGER NOT NULL DEFAULT 0,                   --@ Traveler ID related to the multimodal path (foreign key to Person table)
  "origin_activity_location" INTEGER NOT NULL DEFAULT 0,      --@ Origin location from which this path started (foreign key to Location table)
  "destination_activity_location" INTEGER NOT NULL DEFAULT 0, --@ Destination location at which this path ended (foreign key to Location table)
  "origin_link" INTEGER NOT NULL DEFAULT 0,                   --@ The id of the first link in the path sequence (foreign key to Link table)
  "destination_link" INTEGER NOT NULL DEFAULT 0,              --@ The id of the last link in the path sequence (foreign key to Link table)
  "num_links" INTEGER NOT NULL DEFAULT 0,                     --@ Number of links traversed when executing this multimodal path
  "departure_time" INTEGER NOT NULL DEFAULT 0,                --@ The time at which this path started (units: seconds)
  "Mode" INTEGER NOT NULL DEFAULT 0,                          --@ Mode identifier for trips !Vehicle_Type_Keys!
  "Est_Arrival_Time" REAL NULL DEFAULT 0,                     --@ The time at which this path finished traversing the last link (units: seconds) 
  "Act_Arrival_Time" REAL NULL DEFAULT 0,                     --@ 
  "Est_Gen_Cost" REAL NULL DEFAULT 0,                         --@ Generalized cost for this path
  "Act_Gen_Cost" REAL NULL DEFAULT 0,                         --@ 
  "Est_Duration" REAL NULL DEFAULT 0,                         --@ Time taken to traverse this multimodal link (units: seconds)
  "Act_Duration" REAL NULL DEFAULT 0,                         --@
  "Est_Wait_Count" INTEGER NOT NULL DEFAULT 0,                --@ Number of transfers
  "Act_Wait_Count" INTEGER NOT NULL DEFAULT 0,                --@ 
  "Est_TNC_Wait_Count" INTEGER NOT NULL DEFAULT 0,            --@ Number of transfers to and from a TNC mode
  "Est_Bus_Wait_Time" REAL NULL DEFAULT 0,                    --@ Wait time to board a bus. Can be 0 if bus is not the next transfer. (units: seconds)
  "Act_Bus_Wait_Time" REAL NULL DEFAULT 0,                    --@ 
  "Est_Rail_Wait_Time" REAL NULL DEFAULT 0,                   --@ Wait time to board a rail. Can be 0 if rail is not the next transfer. (units: seconds)
  "Act_Rail_Wait_Time" REAL NULL DEFAULT 0,                   --@ 
  "Est_Comm_Rail_Wait_Time" REAL NULL DEFAULT 0,              --@ Wait time to board a commuter rail. Can be 0 if commuter rail is not the next transfer. (units: seconds)
  "Act_Comm_Rail_Wait_Time" REAL NULL DEFAULT 0,              --@ 
  "Est_Walk_Time" REAL NULL DEFAULT 0,                        --@ Walk time along this link (units: seconds)
  "Act_Walk_Time" REAL NULL DEFAULT 0,                        --@ 
  "Est_Bike_Time" REAL NULL DEFAULT 0,                        --@ Bike time along this link (units: seconds)
  "Act_Bike_Time" REAL NULL DEFAULT 0,                        --@ 
  "Est_Bus_IVTT" REAL NULL DEFAULT 0,                         --@ Bus in-vehicle travel time along this link (units: seconds)
  "Act_Bus_IVTT" REAL NULL DEFAULT 0,                         --@ 
  "Est_Rail_IVTT" REAL NULL DEFAULT 0,                        --@ Rail in-vehicle travel time along this link (units: seconds)
  "Act_Rail_IVTT" REAL NULL DEFAULT 0,                        --@ 
  "Est_Comm_Rail_IVTT" REAL NULL DEFAULT 0,                   --@ Commuter rail in-vehicle travel time along this link (units: seconds)
  "Act_Comm_Rail_IVTT" REAL NULL DEFAULT 0,                   --@ 
  "Est_Car_Time" REAL NULL DEFAULT 0,                         --@ Auto in-vehicle travel time along this link (units: seconds)
  "Act_Car_Time" REAL NULL DEFAULT 0,                         --@ 
  "Est_Transfer_Pen" REAL NULL DEFAULT 0,                     --@ Total transfer penalty incurred in traversing the path (units: seconds)
  "Act_Transfer_Pen" REAL NULL DEFAULT 0,                     --@ 
  "Est_Standing_Pen" REAL NULL DEFAULT 0,                     --@ Total penalty for standing in a crowded transit mode incurred in traversing the path (units: seconds)
  "Act_Standing_Pen" REAL NULL DEFAULT 0,                     --@ 
  "Est_Capacity_Pen" REAL NULL DEFAULT 0,                     --@ Estimated capacity penalty (using CapacityAlpha from MultimodalRouting.json) when load exceeds a threshold (obtained from inflating transit vehicle capacity by CapacityBeta in MultimodalRouting.json) (units: seconds)
  "Act_Capacity_Pen" REAL NULL DEFAULT 0,                     --@
  "Est_Monetary_Cost" REAL NULL DEFAULT 0,                    --@ Monetary cost that is incurred in traversing the path (units: $USD)
  "Act_Monetary_Cost" REAL NULL DEFAULT 0,                    --@ 
  "Number_of_Switches" INTEGER NOT NULL DEFAULT 0)            --@ Total number of reroutes/detours that occured during path execution