-- Copyright (c) 2024, UChicago Argonne, LLC
-- BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
pragma foreign_keys = off;

-- Delete multi-modal paths
delete from path_multimodal;
delete from path_multimodal_links;

-- Delete all trips which we don't care about ( we care only about - SOV, TNC, Trucks)
delete from trip where mode not in (0, 9, 17, 18, 19, 20);

-- Delete all paths except those from modes (SOV/Truck) - TNC paths are always dynamic
delete from path where id not in (select path from trip where mode != 9);

pragma foreign_keys = on;
