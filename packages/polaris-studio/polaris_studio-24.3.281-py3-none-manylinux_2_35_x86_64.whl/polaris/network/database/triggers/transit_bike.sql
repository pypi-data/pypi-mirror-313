-- Copyright (c) 2024, UChicago Argonne, LLC
-- BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md

create trigger if not exists transit_bike_queue_edit_delete_link after delete on Transit_Bike
  begin
    Delete from Transit_Stops
    where stop_id = old.from_node and
    (select sum(n) from
           (
           SELECT count(*) n FROM Transit_Walk WHERE from_node = old.from_node OR to_node = old.from_node UNION ALL
           SELECT count(*) n FROM Transit_Bike WHERE from_node = old.from_node OR to_node = old.from_node UNION ALL
           SELECT count(*) c FROM Transit_Links WHERE from_node = old.from_node OR to_node = old.from_node UNION ALL
           SELECT count(*) c FROM Transit_Pattern_Mapping WHERE stop_id = old.from_node
           )
    ) < 1;

    Delete from Transit_Stops
    where stop_id = old.to_node and
    (select sum(n) from
           (
           SELECT count(*) n FROM Transit_Walk WHERE from_node = old.to_node OR to_node = old.to_node UNION ALL
           SELECT count(*) n FROM Transit_Bike WHERE from_node = old.to_node OR to_node = old.to_node UNION ALL
           SELECT count(*) c FROM Transit_Links WHERE from_node = old.to_node OR to_node = old.to_node UNION ALL
           SELECT count(*) c FROM Transit_Pattern_Mapping WHERE stop_id = old.to_node
           )
    ) < 1;

    insert into editing_table Values(NULL, 'Transit_Bike', 'bike_link', old.bike_link, NULL, NULL, 'DELETE', 0, '');
  end;

--##
create trigger if not exists transit_bike_queue_edit_add_link after INSERT on Transit_Bike
  begin
    update Transit_Bike
    set "bearing_a" =  coalesce(round(Degrees(ST_Azimuth(StartPoint(new.geo), ST_PointN(SanitizeGeometry(new.geo), 2))),0),0),
        "bearing_b" = coalesce(round(Degrees(ST_Azimuth(ST_PointN(SanitizeGeometry(new.geo), ST_NumPoints(SanitizeGeometry(new.geo))-1), EndPoint(new.geo))),0),0),
        "length" = round(ST_Length(new.geo), 4)
    where Transit_Bike.rowid = new.rowid;
    insert into editing_table Values(NULL, 'Transit_Bike', 'bike_link', new.bike_link, NULL, NULL, 'ADD', 0, '');
  end;

--##
create trigger if not exists transit_bike_queue_edit_change_geo_link after UPDATE of geo on Transit_Bike
  begin
    update Transit_Bike
    set "bearing_a" =  coalesce(round(Degrees(ST_Azimuth(StartPoint(new.geo), ST_PointN(SanitizeGeometry(new.geo), 2))),0),0),
        "bearing_b" = coalesce(round(Degrees(ST_Azimuth(ST_PointN(SanitizeGeometry(new.geo), ST_NumPoints(SanitizeGeometry(new.geo))-1), EndPoint(new.geo))),0),0),
        "length" = round(ST_Length(new.geo), 4)
    where Transit_Bike.rowid = new.rowid;
    insert into editing_table Values(NULL, 'Transit_Bike', 'bike_link', new.bike_link, 'geo', NULL, 'EDIT', 0, '');
  end;

--##
create trigger if not exists transit_bike_change_bike_link_id after UPDATE of bike_link on Transit_Bike
  begin
    Update Location
    set bike_link = new.bike_link
    where bike_link = old.bike_link;
  end;


--##
create trigger if not exists transit_bike_enforces_link_bearing_a_update after update of "bearing_a" on Transit_Bike
begin
    update Transit_Bike
    set "bearing_a" =  coalesce(round(Degrees(ST_Azimuth(StartPoint(geo), ST_PointN(SanitizeGeometry(geo), 2))),0),0)
    where Transit_Bike.rowid = new.rowid;
end;


--##
create trigger if not exists transit_bike_enforces_link_bearing_b_update after update of "bearing_b" on Transit_Bike
begin
    update Transit_Bike
    set "bearing_b" = coalesce(round(Degrees(ST_Azimuth(ST_PointN(SanitizeGeometry(new.geo), ST_NumPoints(SanitizeGeometry(new.geo))-1), EndPoint(new.geo))),0),0)
    where Transit_Bike.rowid = new.rowid;
end;
