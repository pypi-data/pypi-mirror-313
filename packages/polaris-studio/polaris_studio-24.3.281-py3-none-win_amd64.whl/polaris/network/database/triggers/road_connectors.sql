-- Copyright (c) 2024, UChicago Argonne, LLC
-- BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
--##
create trigger if not exists Road_Connector_populates_length_on_new_record after insert on Road_Connectors
begin
    update  Road_Connectors
    set "length" = round(coalesce(ST_Length(new.geo), 0), 8)
    where Road_Connectors.rowid = new.rowid;
end;

--##
create trigger if not exists Road_Connector_populates_length_on_new_geometry after update of "geo" on Road_Connectors
begin
    update  Road_Connectors
    set "length" = round(coalesce(ST_Length(new.geo), 0), 8)
    where Road_Connectors.rowid = new.rowid;
end;

--##
create trigger if not exists Road_Connectorenforces_length_field after update of "length" on Road_Connectors
begin
    update  Road_Connectors
    set "length" = round(coalesce(ST_Length(new.geo), 0), 8)
    where Road_Connectors.rowid = new.rowid;
end;

--##
create trigger if not exists Road_Connectorenforces_bearing after INSERT on Road_Connectors
  begin
    update Road_Connectors
    set "bearing_a" =  coalesce(round(Degrees(ST_Azimuth(StartPoint(new.geo), ST_PointN(SanitizeGeometry(new.geo), 2))),0),0),
        "bearing_b" = coalesce(round(Degrees(ST_Azimuth(ST_PointN(SanitizeGeometry(new.geo), ST_NumPoints(SanitizeGeometry(new.geo))-1), EndPoint(new.geo))),0),0)
    where Road_Connectors.rowid = new.rowid;
    insert into editing_table Values(NULL, 'Road_Connectors', 'road_connector', new.road_connector, NULL, NULL, 'ADD', 0, '');
end;