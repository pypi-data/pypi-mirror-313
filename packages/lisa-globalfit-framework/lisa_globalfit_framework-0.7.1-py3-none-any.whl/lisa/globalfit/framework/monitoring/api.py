from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from aiobotocore.session import AioSession, get_session
from aiohttp.web import (
    AppKey,
    Application,
    Request,
    Response,
    RouteTableDef,
    json_response,
)
from types_aiobotocore_s3.client import S3Client

from lisa.globalfit.framework.io import CustomJSONEncoder
from lisa.globalfit.framework.monitoring import service
from lisa.globalfit.framework.monitoring.types import MonitoringStorage

# Use typed application-level variables.
# See https://docs.aiohttp.org/en/stable/web_advanced.html#application-s-config
s3_session = AppKey("s3_session", AioSession)
s3_bucket = AppKey("s3_bucket", str)


routes = RouteTableDef()


@asynccontextmanager
async def get_s3_client(request: Request) -> AsyncIterator[S3Client]:
    # Use AWS_ENDPOINT_URL, AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment
    # variables for client authentication.
    async with request.app[s3_session].create_client(
        "s3",
    ) as client:
        yield client


@asynccontextmanager
async def get_monitoring_storage(request: Request) -> AsyncIterator[MonitoringStorage]:
    async with get_s3_client(request) as s3:
        yield MonitoringStorage(s3, request.app[s3_bucket])


@routes.get("/runs")
async def get_runs(request: Request) -> Response:
    async with get_monitoring_storage(request) as storage:
        response = await service.get_runs(storage)
    return json_response(response, dumps=CustomJSONEncoder.dumps)


@routes.get("/runs/{run}/groups")
async def get_run_groups(request: Request) -> Response:
    async with get_monitoring_storage(request) as storage:
        response = await service.get_run_groups(storage, request.match_info["run"])
    return json_response(response, dumps=CustomJSONEncoder.dumps)


@routes.get("/runs/{run}/groups/{group}/modules")
async def get_run_group_modules(request: Request) -> Response:
    async with get_monitoring_storage(request) as storage:
        response = await service.get_run_group_modules(
            storage, request.match_info["run"], request.match_info["group"]
        )
    return json_response(response, dumps=CustomJSONEncoder.dumps)


@routes.get("/runs/{run}/groups/{group}/modules/{module}")
async def get_run_group_module(request: Request) -> Response:
    async with get_monitoring_storage(request) as storage:
        response = await service.get_run_group_module(
            storage,
            request.match_info["run"],
            request.match_info["group"],
            request.match_info["module"],
        )
    return json_response(response, dumps=CustomJSONEncoder.dumps)


def register(app: Application, prefix: str, s3_bucket_name: str):
    subapp = Application()
    subapp.add_routes(routes)

    # Configure S3 client.
    subapp[s3_session] = get_session()
    subapp[s3_bucket] = s3_bucket_name
    app.add_subapp(prefix, subapp)
