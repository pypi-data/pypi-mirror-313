-- Copyright (c) 2024, UChicago Argonne, LLC
-- BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
--##
create trigger if not exists prevent_delete_version before delete on About_Model
when
old.infoname in ("network_model_version", "hand_of_driving")
begin
    select raise(ROLLBACK, "You cannot delete this record");
end;

--##
create trigger if not exists prevent_change_version before update on About_Model
when
    old.infoname = "network_model_version"
begin
    select raise(ROLLBACK, "You cannot make changes to this record outside the API");
end;