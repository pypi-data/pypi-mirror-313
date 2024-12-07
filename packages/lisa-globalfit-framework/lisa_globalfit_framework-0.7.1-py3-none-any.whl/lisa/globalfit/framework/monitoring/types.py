import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import Self

from aiobotocore.session import get_session
from types_aiobotocore_s3 import S3Client


@dataclass
class MonitoringStorage:
    client: S3Client
    bucket: str

    @classmethod
    @asynccontextmanager
    async def from_env(cls) -> AsyncIterator[Self]:
        async with get_session().create_client("s3") as s3:
            yield cls(s3, os.environ["S3_BUCKET"])
