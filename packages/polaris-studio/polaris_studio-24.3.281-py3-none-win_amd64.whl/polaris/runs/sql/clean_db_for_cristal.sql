-- Copyright (c) 2024, UChicago Argonne, LLC
-- BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
pragma foreign_keys = off;

delete from activity;
delete from path_multimodal_links;
delete from path_multimodal;


delete from trip where type <> 22; -- DELETE NON-EXTERNAL TRIPS

update trip set vehicle = NULL, person = NULL, path = -1, path_multimodal = NULL, experienced_gap = 1.0;

pragma foreign_keys = on;
