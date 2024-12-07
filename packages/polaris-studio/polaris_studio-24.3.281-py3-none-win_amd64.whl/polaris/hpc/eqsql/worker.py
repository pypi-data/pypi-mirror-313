# Copyright (c) 2024, UChicago Argonne, LLC
# BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
from datetime import datetime
from typing import NamedTuple

from polaris.hpc.eq_utils import git_pull
from polaris.hpc.eqsql.eq import insert_task
from polaris.hpc.eqsql.eq_db import workers_table
from polaris.hpc.eqsql.utils import from_id, update_from_db, update_to_db


class Worker(NamedTuple):
    worker_id: str
    status: str
    message: str
    task_id: int
    updated_at: datetime

    @classmethod
    def from_id(cls, engine, worker_id):
        return from_id(cls, engine, worker_id)

    def mark_dead(self, engine):
        """Useful if a worker has gone offline without informing the database"""
        updated_message = f"DEAD: {self.message}" if not self.message.startswith("DEAD") else self.message
        return update_to_db(self, engine, status="dead", message=updated_message)

    def terminate(self, engine):
        """Tell the worker to shutdown and update the db appropriately"""
        eq_abort_task = {"task-type": "control-task", "control-type": "EQ_ABORT"}
        with engine.connect() as conn:
            insert_task(conn=conn, worker_id=f"^{self.worker_id}$", definition=eq_abort_task, input={})

    abort = terminate  # type:ignore

    def restart(self, engine):
        """Tell the worker to restart and reload code"""
        eq_task = {"task-type": "control-task", "control-type": "EQ_RESTART"}
        with engine.connect() as conn:
            insert_task(conn=conn, worker_id=f"^{self.worker_id}$", definition=eq_task, input={})

    def git_pull(self, engine):
        return git_pull(engine, self.worker_id)

    @property
    def machine_id(self):
        return "-".join(self.worker_id.split("-")[0:-1])

    @property
    def primary_key(self):
        return self.worker_id

    def update_from_db(self, engine):
        return update_from_db(self, engine)

    def update_to_db(self, engine, **kwargs):
        return update_to_db(self, engine, **kwargs)

    @classmethod
    def table(cls):
        return workers_table

    @classmethod
    def key_col(cls):
        return workers_table.c.worker_id
