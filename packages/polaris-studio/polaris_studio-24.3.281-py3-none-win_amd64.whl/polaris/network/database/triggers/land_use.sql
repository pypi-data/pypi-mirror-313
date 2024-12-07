-- Copyright (c) 2024, UChicago Argonne, LLC
-- BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
-- Guarantees that flags on the land_use table are always binary

create trigger if not exists land_use_is_work_update before update of is_work on land_use
when new.is_work != 0 AND new.is_work != 1
begin
  select RAISE(ABORT,'is_work flag needs to be 0 or 1');
end;

--##
create trigger if not exists land_use_is_work_insert before insert on land_use
when new.is_work != 0 AND new.is_work != 1
begin
  select RAISE(ABORT,'is_work flag needs to be 0 or 1');
end;

--##
create trigger if not exists land_use_is_home_update before update of is_home on land_use
when new.is_home != 0 AND new.is_home != 1
begin
  select RAISE(ABORT,'is_home flag needs to be 0 or 1');
end;

--##
create trigger if not exists land_use_is_home_insert before insert on land_use
when new.is_home != 0 AND new.is_home != 1
begin
  select RAISE(ABORT,'is_home flag needs to be 0 or 1');
end;

--##
create trigger if not exists land_use_is_discretionary_update before update of is_discretionary on land_use
when new.is_discretionary != 0 AND new.is_discretionary != 1
begin
  select RAISE(ABORT,'is_discretionary flag needs to be 0 or 1');
end;

--##
create trigger if not exists land_use_is_discretionary_insert before insert on land_use
when new.is_discretionary != 0 AND new.is_discretionary != 1
begin
  select RAISE(ABORT,'is_discretionary flag needs to be 0 or 1');
end;

--##
create trigger if not exists land_use_is_school_update before update of is_school on land_use
when new.is_school != 0 AND new.is_school != 1
begin
  select RAISE(ABORT,'is_school flag needs to be 0 or 1');
end;

--##
create trigger if not exists land_use_is_school_insert before insert on land_use
when new.is_school != 0 AND new.is_school != 1
begin
  select RAISE(ABORT,'is_school flag needs to be 0 or 1');
end;