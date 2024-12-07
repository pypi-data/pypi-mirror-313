-- Copyright (c) 2024, UChicago Argonne, LLC
-- BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
--@ All person trips executed during simulation in POLARIS is logged here as a separate record.
--@ Note that only the SOV-related record can be counted as a vehicle trip for person-related travel.
--@ All freight trips can also be counted as a vehicle trip

CREATE TABLE "Trip" (
  "trip_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, --@ Unique identifier of this trip 
  "hhold" INTEGER NOT NULL DEFAULT 0,                   --@ Not used
  "path" INTEGER NOT NULL DEFAULT -1,                   --@ path is not -1 if there exists trajectory-related information in the Path table (in H5) referenced by this value. (foreign key to the Path table)
  "path_multimodal" INTEGER NULL,                       --@ path_multimodal is not NULL if there exists multimodal trajectory-related information in the Path_Multimodal table referenced by this value. (foreign key to the Path_Multimodal table)
  "tour" INTEGER NOT NULL DEFAULT 0,                    --@ Not used
  "trip" INTEGER NOT NULL DEFAULT 0,                    --@ Not used
  "start" REAL NULL DEFAULT 0,                          --@ Simulation time when this trip starts (units: seconds)
  "end" REAL NULL DEFAULT 0,                            --@ Simulation time when this trip ends (units: seconds)
  "duration" REAL NULL DEFAULT 0,                       --@ Not used
  "experienced_gap" REAL NULL DEFAULT 0,                --@ Gap experienced by person based on executed travel time (provided by end minus start) compared to routed travel time.
  "origin" INTEGER NOT NULL DEFAULT 0,                  --@ The location where this trip begins (foreign key to the Location table)
  "destination" INTEGER NOT NULL DEFAULT 0,             --@ The location where this trip ends (foreign key to the Location table)
  "purpose" INTEGER NOT NULL DEFAULT 0,                 --@ Currently used only to distinguish freight trips as E-Commerce or not
  "mode" INTEGER NOT NULL DEFAULT 0,                    --@ The mode used to execute the trip. !Vehicle_Type_Keys!
  "constraint" INTEGER NOT NULL DEFAULT 0,              --@ Not used
  "priority" INTEGER NOT NULL DEFAULT 0,                --@ Not used
  "vehicle" INTEGER NULL,                               --@ Vehicle ID used to complete the travel. Can be NULL for non-motorized trips.
  "passengers" INTEGER NOT NULL DEFAULT 0,              --@ Not used
  "type" INTEGER NOT NULL DEFAULT 0,                    --@ Trip type is logged as either an ABM, External, External_TNC, TNC, Fixed, Transit, or Unsimulated. 
  "partition" INTEGER NOT NULL DEFAULT 0,               --@ Not used
  "person" INTEGER NULL,                                --@ Person who was primarily involved in the trip (foreign key to the Person table)
  "travel_distance" REAL NULL DEFAULT 0,                --@ Distance traveled in executing this trip (units: meters)
  "skim_travel_time" REAL NULL DEFAULT 0,               --@ Travel time from the skim table for comparison with execution (units: seconds)
  "routed_travel_time" REAL NULL DEFAULT 0,             --@ Travel time from the router for comparison with execution (units: seconds)
  "toll" REAL NULL DEFAULT 0,                           --@ Toll paid in executing the trip (units: $USD)
  "has_artificial_trip" INTEGER NOT NULL DEFAULT 0,     --@ Integer to denote the type of artificial trip and can include: All good (0), Not routed (1), congestion removal (2), simulation ended (3), stuck in entry queue (4) 
  "number_of_switches" INTEGER NOT NULL DEFAULT 0,      --@ Integer value indicating the number of times the path was changed to account for downstream congestion or when waiting too long at a link
  "request" INTEGER NOT NULL DEFAULT 0,                 --@ Not used
  "monetary_cost" REAL NULL DEFAULT 0,                  --@ Dollar amount paid when making the trip (units: $USD)

  CONSTRAINT "path_multimodal_fk"
    FOREIGN KEY ("path_multimodal")
    REFERENCES "Path_Multimodal" ("id")
    DEFERRABLE INITIALLY DEFERRED,
  CONSTRAINT "vehicle_fk"
    FOREIGN KEY ("vehicle")
    REFERENCES "Vehicle" ("vehicle_id")
    DEFERRABLE INITIALLY DEFERRED,
  CONSTRAINT "person_fk"
    FOREIGN KEY ("person")
    REFERENCES "Person" ("person")
    DEFERRABLE INITIALLY DEFERRED)