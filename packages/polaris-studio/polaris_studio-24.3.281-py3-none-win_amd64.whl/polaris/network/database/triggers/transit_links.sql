-- Copyright (c) 2024, UChicago Argonne, LLC
-- BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
--##
create trigger if not exists transit_links_populates_length_on_new_record after insert on Transit_Links
begin
    update Transit_Links
    set "length" = round(coalesce(ST_Length(new.geo), 0), 8)
    where Transit_Links.rowid = new.rowid;
end;

--##
create trigger if not exists transit_links_populates_length_on_new_geometry after update of "geo" on Transit_Links
begin
    update Transit_Links
    set "length" = round(coalesce(ST_Length(new.geo), 0), 8)
    where Transit_Links.rowid = new.rowid;
end;

--##
create trigger if not exists transit_links_enforces_length_field after update of "length" on Transit_Links
begin
    update Transit_Links
    set "length" = round(coalesce(ST_Length(new.geo), 0), 8)
    where Transit_Links.rowid = new.rowid;
end;

--##
-- We can uncomment from here downwards if and only if we are looking for editing capabilities for the transit layers
-- create trigger if not exists transit_links_fixes_geo_on_stop_change after update of geo on Transit_Stops
-- begin
-- update Transit_Links
--     set geo = SetStartPoint(geo,new.geo)
--     where from_node = new.stop
--     and StartPoint(geo) != new.geo;
--
-- update Transit_Links
--     set geo = SetEndPoint(geo,new.geo)
--     where to_node = new.stop
--     and EndPoint(geo) != new.geo;
--
-- update Transit_Links
--     set "length" = round(ST_Length(new.geo), 8)
--     where Transit_Links.rowid = new.rowid;
-- end;
--
-- --##
-- create trigger if not exists transit_links_dont_delete_stop before delete on Transit_Stops
--   when (SELECT count(*) FROM Transit_Stops WHERE from_node = old.stop OR to_node = old.stop) > 0
--   BEGIN
--     SELECT raise(ABORT, 'Stop cannot be deleted, it still has transit links attached to it.');
--   END;