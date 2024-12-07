-- Copyright (c) 2024, UChicago Argonne, LLC
-- BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md

--##
create trigger if not exists location_populates_fields_on_new_record after insert on Location
begin
    update Location
    set
        x = round(ST_X(new.geo), 8),
        y = round(ST_Y(new.geo), 8),
        area_type = coalesce((select area_type from Zone where zone=new.zone), -1),
        setback = round(coalesce(st_distance(new.geo, (select geo from Link where link= new.link)), 0), 8)
    where
        Location.rowid = new.rowid;
    insert into editing_table Values(NULL, 'Location', 'location', new.location, 'geo', NULL, 'ADD', 0, '');
end;

--##
create trigger if not exists location_enforces_x_field_Location after update of "x" on Location
begin
    update Location
    set x = round(ST_X(new.geo), 8)
    where Location.rowid = new.rowid;
end;

--##
create trigger if not exists location_enforces_setback_field_Location after update of setback on Location
begin
    update Location
    set setback = round(coalesce(st_distance(new.geo, (select geo from Link where link= new.link)), old.setback), 2)
    where Location.rowid = new.rowid;
end;

--##
create trigger if not exists location_enforces_link_field_Location after update of link on Location
begin
    update Location
    set setback = round(coalesce(st_distance(new.geo, (select geo from Link where link= new.link)), old.setback), 2)
    where Location.rowid = new.rowid;
end;

--##
create trigger if not exists location_enforces_y_field_Location after update of "y" on Location
begin
    update Location
    set "y" = round(ST_Y(new.geo), 8)
    where Location.rowid = new.rowid;
end;

--##
-- create trigger if not exists location_enforces_z_field_Location after update of "z" on Location
-- begin
--     update Location
--     set "z" = COALESCE(ST_Z(new.geo), 0)
--     where Location.rowid = new.rowid;
-- end;

--##
create trigger if not exists location_updates_xyz_fields_on_geo_change after update of geo on Location
begin
    update Location
    set "x" = round(ST_X(new.geo), 8),
        "y" = round(ST_Y(new.geo), 8),
        setback = coalesce(round(st_distance(new.geo, (select geo from Link where link= new.link)), 2), old.setback)
    where Location.rowid = new.rowid;
    insert into editing_table Values(NULL, 'Location', 'location', new.location, 'geo', NULL, 'EDIT', 0, '');
end;

--##
create trigger if not exists location_updates_area_type_on_zone_change after update of zone on Location
begin
    update Location
    set area_type = coalesce((select area_type from Zone where zone=new.zone), old.area_type)
    where Location.rowid = new.rowid;
    insert into editing_table Values(NULL, 'Location', 'location', new.location, 'zone', NULL, 'EDIT', 0, '');
end;

--##
create trigger if not exists location_enforces_area_type_on_area_type_change after update of area_type on Location
begin
    update Location
    set area_type = coalesce((select area_type from Zone where zone=new.zone), old.area_type)
    where Location.rowid = new.rowid;
end;


--##
create trigger if not exists location_on_link_change after update of link on Location
begin
    insert into editing_table Values(NULL, 'Location', 'location', new.location, 'link', NULL, 'EDIT', 0, '');
end;


--##
create trigger if not exists location_on_walk_link_change after update of walk_link on Location
begin
    update Location
    set "walk_offset" = coalesce(round((select ST_Line_Locate_Point(geo, new.geo) * "length" from Transit_Walk where walk_link=new.walk_link), 2), old.walk_offset)
    where Location.rowid = new.rowid;
    insert into editing_table Values(NULL, 'Location', 'location', new.location, 'walk_link', NULL, 'EDIT', 0, '');
end;


--##
create trigger if not exists location_on_bike_link_change after update of bike_link on Location
begin
    update Location
    set "bike_offset" = coalesce(round((select ST_Line_Locate_Point(geo, new.geo) * "length" from Transit_Bike where bike_offset=new.bike_offset), 2), old.bike_offset)
    where Location.rowid = new.rowid;
    insert into editing_table Values(NULL, 'Location', 'location', new.location, 'bike_link', NULL, 'EDIT', 0, '');
end;


--##
create trigger if not exists location_on_walk_offset_change after update of walk_offset on Location
begin
    update Location
    set "walk_offset" = coalesce(round((select ST_Line_Locate_Point(geo, new.geo) * "length" from Transit_Walk where walk_link=new.walk_link), 2), old.walk_offset)
    where Location.rowid = new.rowid;
end;

--##
create trigger if not exists location_on_bike_offset_change after update of bike_offset on Location
begin
    update Location
    set "bike_offset" = coalesce(round((select ST_Line_Locate_Point(geo, new.geo) * "length" from Transit_Bike where bike_link=new.bike_link), 2), old.bike_offset)
    where Location.rowid = new.rowid;
end;

--##
create trigger if not exists location_deleted_location after delete on Location
begin
    DELETE FROM Location_Links where location=old.location;
    DELETE FROM Location_Parking where location=old.location;
    insert into editing_table Values(NULL, 'Location', 'location', old.location, NULL, NULL, 'DELETE', 0, '');
end;
