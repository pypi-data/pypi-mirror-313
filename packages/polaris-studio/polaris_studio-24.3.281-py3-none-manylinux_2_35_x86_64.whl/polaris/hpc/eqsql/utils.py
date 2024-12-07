# Copyright (c) 2024, UChicago Argonne, LLC
# BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
import inspect
import json
import logging
from functools import wraps

from sqlalchemy import func, text


def clear_idle_pg_connection():
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            args_dict = inspect.getcallargs(function, *args, **kwargs)
            if "engine" in args_dict:
                try:
                    with args_dict["engine"].connect() as conn:
                        conn.execute(text("SELECT 1"))
                except Exception:
                    pass
            elif "conn" in args_dict:
                try:
                    args_dict["conn"].execute(text("SELECT 1"))
                except Exception as err:
                    logging.warning(
                        "Your database conn seems to have become idle - you can likely get around this problem by "
                        "re-running the cell of your notebook."
                    )
                    raise RuntimeError("Idle conn Object") from err

            return function(*args, **kwargs)

        return wrapper

    return decorator


def from_id(cls, engine, id):
    with engine.connect() as conn:
        return from_cursor_result(cls, conn.execute(cls.table().select().filter(cls.key_col() == id)))


def from_cursor_result(cls, result):
    row = result.fetchone()
    if row is None:
        return None
    return from_row(cls, row)


def from_row(cls, row):
    return cls(**dictify_dict_fields(row._asdict()))


def dictify_dict_fields(dct):
    if "input" in dct:
        dct["input"] = json.loads(dct["input"])
    if "definition" in dct:
        dct["definition"] = json.loads(dct["definition"])
    return dct


def update_from_db(obj, engine):
    with engine.connect() as conn:
        cursor_result = conn.execute(type(obj).table().select().filter(type(obj).key_col() == obj.primary_key))
        data = dict(cursor_result.fetchone()._asdict().items())
        return obj._replace(**dictify_dict_fields(data))


def update_to_db(obj, engine, **kwargs):
    if "updated_at" not in kwargs:
        kwargs["updated_at"] = func.now()
    for k, v in kwargs.items():
        if isinstance(v, dict):
            kwargs[k] = json.dumps(v)
    with engine.connect() as conn:
        update_stmt = type(obj).table().update().filter(type(obj).key_col() == obj.primary_key)
        stmt = update_stmt.values(**kwargs).returning(type(obj).table().c)
        return from_cursor_result(type(obj), conn.execute(stmt))
