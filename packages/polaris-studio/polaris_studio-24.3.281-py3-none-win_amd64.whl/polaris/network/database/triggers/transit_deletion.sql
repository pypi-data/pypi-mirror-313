-- Copyright (c) 2024, UChicago Argonne, LLC
-- BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
--##
create trigger if not exists transit_delete_patterns_when_deleting_routes before delete on Transit_Routes
  BEGIN
    DELETE FROM Transit_Patterns where route_id == old.route_id;
    DELETE FROM Transit_Fare_Rules where route_id == old.route_id;
  END;

--##
create trigger if not exists transit_delete_trips_when_deleting_patterns before delete on Transit_Patterns
  BEGIN
    DELETE FROM Transit_Pattern_Mapping where pattern_id == old.pattern_id;
    DELETE FROM Transit_Trips where pattern_id == old.pattern_id;
    DELETE FROM Transit_Links where pattern_id == old.pattern_id;
    DELETE FROM Transit_Pattern_Links where pattern_id == old.pattern_id;
  END;
  
--##
create trigger if not exists transit_delete_when_deleting_trips before delete on Transit_Trips
  BEGIN
    DELETE FROM Transit_Trips_Schedule where trip_id == old.trip_id;
  END;

--##
create trigger if not exists transit_delete_connector_when_delete_stop after delete on Transit_Stops
  BEGIN
    DELETE FROM Road_Connectors where to_node == old.stop_id;
  END;