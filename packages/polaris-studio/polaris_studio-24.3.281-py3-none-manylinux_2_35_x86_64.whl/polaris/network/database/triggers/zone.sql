-- Copyright (c) 2024, UChicago Argonne, LLC
-- BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
create trigger if not exists zone_queue_change_deletion after delete on Zone
begin
    INSERT INTO editing_table VALUES(NULL, 'Zone', 'zone', old.zone, NULL, NULL, 'DELETE', 0, '');
end;

--##
create trigger if not exists zone_populates_geo_enabled_fields_on_new_record after insert on Zone
begin
    update Zone
    set "x" = round(COALESCE(ST_X(ST_Centroid(new.geo)), 0), 8),
        "y" = round(COALESCE(ST_Y(ST_Centroid(new.geo)), 0), 8),
        "area" = round(COALESCE(ST_Area(new.geo), 0), 8)
    where Zone.rowid = new.rowid;

    INSERT INTO editing_table VALUES(NULL, 'Zone', 'zone', new.zone, 'geo', NULL, 'ADD', 0, '');
end;

--##
create trigger if not exists zone_enforces_x_field_Zone after update of "x" on Zone
begin
    update Zone
    set "x" = round(COALESCE(ST_X(ST_Centroid(new.geo)), new.x), 8)
    where Zone.rowid = new.rowid;
end;

--##
create trigger if not exists zone_enforces_area_field_Zone after update of "area" on Zone
begin
    update Zone
    set "area" = round(COALESCE(ST_Area(new.geo), new.area), 8)
    where Zone.rowid = new.rowid;
end;

--##
create trigger if not exists zone_enforces_y_field_Zone after update of "y" on Zone
begin
    update Zone
    set "y" = round(COALESCE(ST_Y(ST_Centroid(new.geo)), new.y), 8)
    where Zone.rowid = new.rowid;
end;

--##
create trigger if not exists zone_updates_xyz_fields_on_geo_change after update of geo on Zone
begin
        update Zone
    set "x" = round(COALESCE(ST_X(ST_Centroid(new.geo)), old.x), 8),
        "y" = round(COALESCE(ST_Y(ST_Centroid(new.geo)), old.y), 8),
        "area" = round(COALESCE(ST_Area(new.geo), old.area), 8)
    where Zone.rowid = new.rowid;

    INSERT INTO editing_table VALUES(NULL, 'Zone', 'zone', new.zone, 'geo', NULL, 'EDIT', 0, '');
end;

--##
create trigger if not exists zone_renumbering after update of "zone" on Zone
begin
    update EV_Charging_Stations set zone=new.zone where zone=old.zone;
    update Location set zone=new.zone where zone=old.zone;
    update Node set zone=new.zone where zone=old.zone;
    update Parking set zone=new.zone where zone=old.zone;
    update Transit_Stops set zone=new.zone where zone=old.zone;
    update Micromobility_Docks set zone=new.zone where zone=old.zone;
end;

--##
create trigger if not exists zone_change_area_type after update of area_type on Zone
begin
    update Location set area_type=new.area_type where zone=new.zone;
    INSERT INTO editing_table VALUES(NULL, 'Zone', 'zone', new.zone, 'area_type', NULL, 'EDIT', 0, '');
end;