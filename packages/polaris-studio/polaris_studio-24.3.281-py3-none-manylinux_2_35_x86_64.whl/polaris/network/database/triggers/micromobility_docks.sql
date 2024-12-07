-- Copyright (c) 2024, UChicago Argonne, LLC
-- BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md

--##
create trigger if not exists micromobility_docks_populates_xyz_fields_on_new_record after insert on Micromobility_Docks
begin
    update Micromobility_Docks
    set "x" = round(ST_X(new.geo), 8),  "y" = round(ST_Y(new.geo), 8)
    where Micromobility_Docks.rowid = new.rowid;

    INSERT INTO editing_table VALUES(NULL, 'Micromobility_Docks', 'dock',new.dock_id, NULL, NULL, 'ADD', 0, '');
end;

--##
create trigger if not exists micromobility_docks_enforces_x_field after update of "x" on Micromobility_Docks
begin
    update Micromobility_Docks
    set "x" = round(ST_X(new.geo), 8)
    where Micromobility_Docks.rowid = new.rowid;
end;

--##
create trigger if not exists micromobility_docks_enforces_y_field after update of "y" on Micromobility_Docks
begin
    update Micromobility_Docks
    set "y" = round(ST_Y(new.geo), 8)
    where Micromobility_Docks.rowid = new.rowid;
end;

--##
create trigger if not exists micromobility_docks_enforces_zone_field after update of "zone" on Micromobility_Docks
begin
    INSERT INTO editing_table VALUES(NULL, 'Micromobility_Docks', 'dock', new.dock_id, 'zone', NULL, 'EDIT', 0, '');
end;

--##
create trigger if not exists micromobility_docks_enforces_link_field after update of "link" on Micromobility_Docks
begin
    INSERT INTO editing_table VALUES(NULL, 'Micromobility_Docks', 'dock', new.dock_id, 'link', NULL, 'EDIT', 0, '');
end;

--##
create trigger if not exists micromobility_docks_on_geo_change after update of geo on Micromobility_Docks
begin
    update Micromobility_Docks
    set "x" = round(ST_X(new.geo), 8), "y" = round(ST_Y(new.geo), 8)
    where Micromobility_Docks.rowid = new.rowid;

    update Transit_Walk
    set geo = SetStartPoint(geo,new.geo)
    where from_node = new.dock_id
    and StartPoint(geo) != new.geo;

    update Transit_Walk
    set geo = SetEndPoint(geo,new.geo)
    where to_node = new.dock_id
    and EndPoint(geo) != new.geo;

    update Transit_Bike
    set geo = SetStartPoint(geo,new.geo)
    where from_node = new.dock_id
    and StartPoint(geo) != new.geo;

    update Transit_Bike
    set geo = SetEndPoint(geo,new.geo)
    where to_node = new.dock_id
    and EndPoint(geo) != new.geo;

    INSERT INTO editing_table VALUES(NULL, 'Micromobility_Docks', 'dock',new.dock_id, 'geo', NULL, 'EDIT', 0, '');
end;

--##
create trigger if not exists micromobility_unique_tag before insert on Micromobility_Agencies
when (select count(*) from Transit_Agencies where agency_id=new.agency_id)>0
begin
    SELECT raise(ABORT, 'Operator ID already used for transit agencies');
end;

--##
create trigger if not exists transit_agencies_unique_tag before insert on Transit_Agencies
when (select count(*) from Micromobility_Agencies where agency_id=new.agency_id)>0
begin
    SELECT raise(ABORT, 'Operator ID already used for Micro-mobility agency');
end;