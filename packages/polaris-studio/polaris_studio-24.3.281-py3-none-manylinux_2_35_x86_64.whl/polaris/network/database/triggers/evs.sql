-- Copyright (c) 2024, UChicago Argonne, LLC
-- BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md

--##
create trigger if not exists evs_populates_fields_on_new_record after insert on EV_Charging_Stations
begin
    update EV_Charging_Stations
    set
        Longitude = round(ST_X(new.geo), 8),
        Latitude = round(ST_Y(new.geo), 8)
    where
        EV_Charging_Stations.rowid = new.rowid;
    insert into editing_table Values(NULL, 'EV_Charging_Stations', 'EV_Charging_Stations', new.ID, 'geo', NULL, 'ADD', 0, '');
end;

--##
create trigger if not exists evs_enforces_longitude_field after update of "Longitude" on EV_Charging_Stations
begin
    update 
        EV_Charging_Stations set Longitude = round(ST_X(new.geo), 8)
    where
        EV_Charging_Stations.rowid = new.rowid;
end;

--##
create trigger if not exists evs_enforces_latitude_field after update of "Latitude" on EV_Charging_Stations
begin
    update 
        EV_Charging_Stations set Latitude = round(ST_Y(new.geo), 8)
    where
        EV_Charging_Stations.rowid = new.rowid;
end;

--##
create trigger if not exists evs_updates_lat_lon_fields_on_geo_change after update of geo on EV_Charging_Stations
begin
    update EV_Charging_Stations
    set
        Longitude = round(ST_X(new.geo), 8),
        Latitude = round(ST_Y(new.geo), 8)
    where
        EV_Charging_Stations.rowid = new.rowid;
    insert into editing_table Values(NULL, 'EV_Charging_Stations', 'EV_Charging_Stations', new.ID, 'geo', NULL, 'EDIT', 0, '');
end;

--##
create trigger if not exists evs_delete_all_data_for_deleted_stations before delete on EV_Charging_Stations
begin
  delete from EV_Charging_Station_Plugs where station_id = old.ID;
  delete from EV_Charging_Station_Service_Bays where Station_id = old.ID;
end;

--##
create trigger if not exists evs_updates_zone_field after update of zone on EV_Charging_Stations
when old.zone!= new.zone
begin
    insert into editing_table Values(NULL, 'EV_Charging_Stations', 'EV_Charging_Stations', new.ID, 'zone', NULL, 'EDIT', 0, '');
end;


--##
create trigger if not exists evs_updates_location_field after update of location on EV_Charging_Stations
when old.location!= new.location
begin
    insert into editing_table Values(NULL, 'EV_Charging_Stations', 'EV_Charging_Stations', new.ID, 'location', NULL, 'EDIT', 0, '');
end;

