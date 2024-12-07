-- Copyright (c) 2024, UChicago Argonne, LLC
-- BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
--##
create trigger if not exists parking_enforces_setback_field_setback after update of setback on Parking
begin
    update Parking
    set setback = round(coalesce(st_distance(new.geo, (select geo from Link where link= new.link)), old.setback), 2)
    where Parking.rowid = new.rowid;
end;

--##
create trigger if not exists parking_enforces_link_field_link after update of link on Parking
when old.link!= new.link
begin
    update Parking
    set setback = round(coalesce(st_distance(new.geo, (select geo from Link where link= new.link)), old.setback), 2)
    where Parking.rowid = new.rowid;
    insert into editing_table Values(NULL, 'Parking', 'parking', new.parking, 'link', NULL, 'EDIT', 0, '');
end;

--##
create trigger if not exists parking_updates_fields_on_geo_change after update of geo on Parking
begin
    update Parking
    set setback = round(coalesce(st_distance(new.geo, (select geo from Link where link= new.link)), old.setback), 2)
    where Parking.rowid = new.rowid;
    insert into editing_table Values(NULL, 'Parking', 'parking', new.parking, 'geo', NULL, 'EDIT', 0, '');
end;

--##
create trigger if not exists parking_on_walk_link_change after update of walk_link on Parking
begin
    update Parking
    set "walk_offset" = round((select ST_Line_Locate_Point(geo, new.geo) * "length" from Transit_Walk where walk_link=new.walk_link), 2)
    where Parking.rowid = new.rowid;
    insert into editing_table Values(NULL, 'Parking', 'parking', new.parking, 'walk_link', NULL, 'EDIT', 0, '');
end;

--##
create trigger if not exists parking_on_walk_offset_change after update of walk_offset on Parking
begin
    update Parking
    set "walk_offset" = round((select ST_Line_Locate_Point(geo, new.geo) * "length" from Transit_Walk where walk_link=new.walk_link), 2)
    where Parking.rowid = new.rowid;
end;

--##
create trigger if not exists parking_on_bike_link_change after update of bike_link on Parking
begin
    update Parking
    set "bike_offset" = round((select ST_Line_Locate_Point(geo, new.geo) * "length" from Transit_Bike where bike_link=new.bike_link), 2)
    where Parking.rowid = new.rowid;
    insert into editing_table Values(NULL, 'Parking', 'parking', new.parking, 'bike_link', NULL, 'EDIT', 0, '');
end;

--##
create trigger if not exists parking_on_bike_offset_change after update of bike_offset on Parking
begin
    update Parking
    set "bike_offset" = round((select ST_Line_Locate_Point(geo, new.geo) * "length" from Transit_Bike where bike_link=new.bike_link), 2)
    where Parking.rowid = new.rowid;
end;

--##
create trigger if not exists parking_deleted_parking after delete on Parking
begin
    insert into editing_table Values(NULL, 'Parking', 'parking', old.parking, NULL, NULL, 'DELETE', 0, '');
end;

--##
create trigger if not exists parking_updates_zone_field after update of zone on Parking
when old.zone!= new.zone
begin
    insert into editing_table Values(NULL, 'Parking', 'parking', new.parking, 'zone', NULL, 'EDIT', 0, '');
end;