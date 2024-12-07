import json
import logging
import sqlite3
from asyncio import gather
from collections import ChainMap
from datetime import UTC, datetime
from itertools import groupby
from pathlib import Path
from textwrap import dedent

import numpy as np
from aiosqlite import Connection, connect

from lisa.globalfit.framework.catalog import SourceCatalog
from lisa.globalfit.framework.io import CustomJSONEncoder
from lisa.globalfit.framework.model import ParametricModel
from lisa.globalfit.framework.msg.data import ModuleState
from lisa.globalfit.framework.msg.subjects import Subject

sqlite3.register_adapter(np.float64, float)
sqlite3.register_adapter(np.float32, float)
sqlite3.register_adapter(np.int64, int)
sqlite3.register_adapter(np.int32, int)

logger = logging.getLogger(__name__)


class SqliteSourceCatalog(SourceCatalog):
    def __init__(self, db_file: Path) -> None:
        super().__init__()
        self.db_file = db_file

    async def get_source_parameters(self) -> dict[Subject, ParametricModel]:
        async with connect(self.db_file) as db:
            tables = await self.get_model_tables(db)
            source_parameters = await gather(
                *(self.select_latest_model(db, table) for table in tables)
            )
            return dict(ChainMap(*source_parameters))

    async def update(self, subject: Subject, state: ModuleState) -> None:
        # TODO Should the detection catalog be updated if the best sample from the
        # chain in the current iteration has a lower posterior probability than the
        # best sample from all previous iterations ?
        # The posterior should probably be passed along the waveform parameters, so
        # that its evolution can be monitored during execution.
        async with connect(self.db_file) as db:
            await db.set_trace_callback(logger.debug)
            # TODO Ideally, we should only do this once, but we need to figure out
            # corner cases.
            # Maybe we should try/except the insert directly, and only create the table
            # on error.
            await self.ensure_table(db, state.chain.waveforms)
            await self.insert_values(db, subject, state.chain.waveforms)

    async def write(self, filename: Path) -> None:
        params = await self.get_source_parameters()
        with open(filename, "w") as f:  #  noqa: ASYNC230
            json.dump(params, f, cls=CustomJSONEncoder)
        logger.info(f"wrote {len(params)} source parameters to {filename}")

    def safe_table_name(self, model_name: str) -> str:
        if not model_name.isidentifier():
            raise ValueError("")
        return model_name

    async def ensure_table(self, db: Connection, model: ParametricModel) -> None:
        # We cannot use prepared statements to parametrize table name, so we use
        # string interpolation on a safe version of the model name to prevent SQL
        # injection.
        table = self.safe_table_name(model.name)
        n_params = model.parameters.shape[-1]
        dtype = model.parameters.dtype
        params = ", ".join(f"p{i} {dtype} NOT NULL" for i in range(n_params))
        stmt = dedent(
            f"""
            CREATE TABLE IF NOT EXISTS
            {table} (
                subject TEXT NOT NULL,
                timestamp TIMESTAMP NOT NULL,
                {params}
            )
            """
        ).strip()
        await db.execute(stmt)

    async def insert_values(
        self, db: Connection, subject: Subject, model: ParametricModel
    ) -> None:
        # Here also, static prepared statements cannot be used to insert a dynamic
        # number of columns, so we dynamically create the prepared statement.
        table = self.safe_table_name(model.name)
        timestamp = datetime.now(UTC)
        params_placeholder = ", ".join(["?"] * model.parameters.shape[-1])
        stmt = dedent(
            f"""
            INSERT INTO {table}
            VALUES (
                ?,
                ?,
                {params_placeholder}
            )
            """  # noqa: S608
        ).strip()
        args = [(subject, timestamp, *params) for params in model.parameters]
        await db.executemany(stmt, args)
        await db.commit()

    async def get_model_tables(self, db: Connection) -> list[str]:
        async with db.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        ) as cursor:
            results = await cursor.fetchall()
            return [row[0] for row in results]

    async def select_latest_model(
        self, db: Connection, table: str
    ) -> dict[Subject, ParametricModel]:
        stmt = dedent(
            f"""
            SELECT
                *
            FROM
                {table}
            WHERE
                (subject, timestamp) IN (
                    SELECT
                        subject,
                        MAX(timestamp)
                    FROM
                        {table}
                    GROUP BY
                        subject
                )
            ORDER BY subject
            """  # noqa: S608
        ).strip()
        async with db.execute(stmt) as cursor:
            # TODO This could be more memory-efficient by returning an asynchronous
            # iterator instead.
            rows = await cursor.fetchall()
            return {
                subject: ParametricModel(
                    name=table,
                    # TODO Is the row order guaranteed to be the same as the insertion
                    # order ?
                    parameters=np.array([row[2:] for row in subject_rows]),
                )
                for subject, subject_rows in groupby(rows, key=lambda x: x[0])
            }
