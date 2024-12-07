-- Copyright (c) 2024, UChicago Argonne, LLC
-- BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md

--##
create trigger if not exists connection_populates_node_todir_geo_new_record after insert on Connection
begin
    update Connection
    set "node" = (SELECT CASE
                         WHEN dir =1 THEN (SELECT NODE_A FROM LINK WHERE LINK.link=new.link)
                         ELSE (SELECT NODE_B FROM LINK WHERE LINK.link=new.link)
                         END as 'NODE')
    where Connection.rowid = new.rowid;
    update Connection
    set "to_dir" = (SELECT CASE
                         WHEN (SELECT NODE_A FROM LINK WHERE LINK.link=new.to_link) = new.node THEN 0
                         ELSE 1
                         END as 'todir')
    where Connection.rowid = new.rowid;
--     update Connection set geo= (select CastToSingle(LineMerge(ST_Union(
--                             case new.dir
--                                 when 1
--                                     then st_reverse(ST_Line_Substring((select geo from Link where link=new.link),
--                                                                       0,
--                                                                       min(1.0, 100/ (select "length" from Link where link=new.link))))
--                                 when 0
--                                     then ST_Line_Substring((select geo from Link where link=new.link),
--                                                            1.0 - min(1.0, 100/ (select "length" from Link where link=new.link)),
--                                                            1.0)
--                              END,
--                              case new.to_dir
--                                  when 0
--                                      then ST_Line_Substring((select geo from Link where link=new.to_link),
--                                                             0,
--                                                             min(1.0, 100/ (select "length" from Link where link=new.to_link)))
--                                  when 1
--                                      then st_reverse(ST_Line_Substring((select geo from Link where link=new.to_link),
--                                                                        1.0 - min(1.0, 100/ (select "length" from Link where link=new.to_link)),
--                                                                        1.0))
--                             END))))
--     where Connection.rowid = new.rowid;
end;

--##
create trigger if not exists connection_enforce_node_on_table_change after update on Connection
begin
    update Connection
    set "node" = (SELECT CASE
                         WHEN dir =1 THEN (SELECT NODE_A FROM LINK WHERE LINK.link=new.link)
                         ELSE (SELECT NODE_B FROM LINK WHERE LINK.link=new.link)
                         END as 'NODE')
    where Connection.rowid = new.rowid;
end;

--##
create trigger if not exists connection_enforce_todir_on_table_change after update of node on Connection
begin
    update Connection
    set "to_dir" = (SELECT CASE
                         WHEN (SELECT NODE_A FROM LINK WHERE LINK.link=new.to_link) = new.node THEN 0
                         ELSE 1
                         END as 'todir')
    where Connection.rowid = new.rowid;
end;

--##
-- create trigger if not exists connection_enforce_geo_on_table_change after update of todir on Connection
-- begin
--     update Connection set geo= (select CastToSingle(LineMerge(ST_Union(
--                             case new.dir
--                                 when 1
--                                     then st_reverse(ST_Line_Substring((select geo from Link where link=new.link),
--                                                                       0,
--                                                                       min(1.0, 100/ (select "length" from Link where link=new.link))))
--                                 when 0
--                                     then ST_Line_Substring((select geo from Link where link=new.link),
--                                                            1.0 - min(1.0, 100/ (select "length" from Link where link=new.link)),
--                                                            1.0)
--                              END,
--                              case new.to_dir
--                                  when 0
--                                      then ST_Line_Substring((select geo from Link where link=new.to_link),
--                                                             0,
--                                                             min(1.0, 100/ (select "length" from Link where link=new.to_link)))
--                                  when 1
--                                      then st_reverse(ST_Line_Substring((select geo from Link where link=new.to_link),
--                                                                        1.0 - min(1.0, 100/ (select "length" from Link where link=new.to_link)),
--                                                                        1.0))
--                             END))))
--     where Connection.rowid = new.rowid;
-- end;
