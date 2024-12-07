-- Copyright (c) 2024, UChicago Argonne, LLC
-- BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
--##
create trigger if not exists transit_pattern_mapping_rounds_offset_on_change after update of "offset" on transit_pattern_mapping
begin
    update transit_pattern_mapping
    set "offset" = round(new.offset, 8)
    where transit_pattern_mapping.rowid = new.rowid;
end;

--##
create trigger if not exists transit_pattern_mapping_rounds_offset_on_insert after insert on transit_pattern_mapping
begin
    update transit_pattern_mapping
    set "offset" = round(new.offset, 8)
    where transit_pattern_mapping.rowid = new.rowid;
end;