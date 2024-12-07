-- Copyright (c) 2024, UChicago Argonne, LLC
-- BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md

--##
create trigger if not exists location_links_creates_distance_field_on_insert after insert on Location_Links
begin
    update Location_Links
    set "distance" = round(st_distance((select geo from Location where location = new.location),
                                 (select geo from Link where link = new.link)), 2)
    where Location_Links.rowid = new.rowid;
end;

--##
create trigger if not exists location_links_updates_distance_field_on_change after update on Location_Links
begin
    update Location_Links
    set "distance" = round(st_distance((select geo from Location where location = new.location),
                                 (select geo from Link where link = new.link)), 2)
    where Location_Links.rowid = new.rowid;
end;

--##
create trigger if not exists location_links_deletes after delete on Location_Links
begin
    INSERT INTO editing_table Values(NULL, 'Location_Links', 'location', old.location, NULL, NULL, 'DELETE', 0, '');
end;
