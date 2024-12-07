-- Copyright (c) 2024, UChicago Argonne, LLC
-- BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
--@ Path_multimodal_links table shows the trajectory in detail for each multimodal path logged in the Path_Multimodal table.
--@ Each record in the Path_multimodal_links table is a link that was traversed by the traveler using various modes.
--@
--@ Link-specific router-estimates and experienced values are logged in this table. Definitions for the variable in columns known as 'value_{variable}'
--@ can be found in the Path_Multimodal table description. Unique column descriptions are logged below.

CREATE TABLE "Path_Multimodal_links" (
  "object_id" INTEGER NOT NULL,                 --@ The multimodal path that this link is a part of (foreign key to Path_Multimodal table)
  "index" INTEGER NOT NULL,                     --@ Sequence number for this link within the overall path
  "value_link" INTEGER NOT NULL DEFAULT 0,      --@ The link which makes up this part of the overall path (foreign key to Link table)
  "value_dir" INTEGER NOT NULL,                 --@ The direction of travel on the link {0: a->b, 1: b->a}
  "value_link_type" INTEGER NOT NULL DEFAULT 0, --@ Integer refering to the type of link. !Link_Type_Keys!
  "value_transit_vehicle_trip" INTEGER NOT NULL DEFAULT 0, --@ If this path utilised transit to traverse this link, the id of the corresponding transit trip (foreign key to Transit_Trips table)
  "value_transit_vehicle_stop_sequence" INTEGER NOT NULL DEFAULT 0, --@ Non-zero integer represents a valid transit stop sequence used to distinguish transit stop or transfers. Zero when transit stop sequence is not used.
  "value_Est_Arrival_Time" REAL NULL DEFAULT 0,
  "value_Act_Arrival_Time" REAL NULL DEFAULT 0,
  "value_Est_Gen_Cost" REAL NULL DEFAULT 0,
  "value_Act_Gen_Cost" REAL NULL DEFAULT 0,
  "value_Est_Duration" REAL NULL DEFAULT 0,
  "value_Act_Duration" REAL NULL DEFAULT 0,
  "value_Est_Wait_Count" INTEGER NOT NULL DEFAULT 0,
  "value_Act_Wait_Count" INTEGER NOT NULL DEFAULT 0,
  "value_Est_TNC_Wait_Count" INTEGER NOT NULL DEFAULT 0,
  "value_Est_Bus_Wait_Time" REAL NULL DEFAULT 0,
  "value_Act_Bus_Wait_Time" REAL NULL DEFAULT 0,
  "value_Est_Rail_Wait_Time" REAL NULL DEFAULT 0,
  "value_Act_Rail_Wait_Time" REAL NULL DEFAULT 0,
  "value_Est_Comm_Rail_Wait_Time" REAL NULL DEFAULT 0,
  "value_Act_Comm_Rail_Wait_Time" REAL NULL DEFAULT 0,
  "value_Est_Walk_Time" REAL NULL DEFAULT 0,
  "value_Act_Walk_Time" REAL NULL DEFAULT 0,
  "value_Est_Bike_Time" REAL NULL DEFAULT 0,
  "value_Act_Bike_Time" REAL NULL DEFAULT 0,
  "value_Est_Bus_IVTT" REAL NULL DEFAULT 0,
  "value_Act_Bus_IVTT" REAL NULL DEFAULT 0,
  "value_Est_Rail_IVTT" REAL NULL DEFAULT 0,
  "value_Act_Rail_IVTT" REAL NULL DEFAULT 0,
  "value_Est_Comm_Rail_IVTT" REAL NULL DEFAULT 0,
  "value_Act_Comm_Rail_IVTT" REAL NULL DEFAULT 0,
  "value_Est_Car_Time" REAL NULL DEFAULT 0,
  "value_Act_Car_Time" REAL NULL DEFAULT 0,
  "value_Est_Transfer_Pen" REAL NULL DEFAULT 0,
  "value_Act_Transfer_Pen" REAL NULL DEFAULT 0,
  "value_Est_Standing_Pen" REAL NULL DEFAULT 0,
  "value_Act_Standing_Pen" REAL NULL DEFAULT 0,
  "value_Est_Capacity_Pen" REAL NULL DEFAULT 0,
  "value_Act_Capacity_Pen" REAL NULL DEFAULT 0,
  "value_exit_position" REAL NULL DEFAULT 0,
  "value_Number_of_Switches" INTEGER NOT NULL DEFAULT 0,
  "value_Est_Monetary_Cost" REAL NULL DEFAULT 0,
  "value_Act_Monetary_Cost" REAL NULL DEFAULT 0,
  "value_Est_Status" INTEGER NOT NULL DEFAULT 0, --@ The expected person status when traversing this link at the routing stage. !Movement_Status_Keys!
  "value_Act_Status" INTEGER NOT NULL DEFAULT 0, --@ The actual experienced person status when traversing this link. !Movement_Status_Keys!
  "value_Switch_Cause" INTEGER NOT NULL DEFAULT 0,
  CONSTRAINT "object_id_fk"
    FOREIGN KEY ("object_id")
    REFERENCES "Path_Multimodal" ("id")
    ON DELETE CASCADE)