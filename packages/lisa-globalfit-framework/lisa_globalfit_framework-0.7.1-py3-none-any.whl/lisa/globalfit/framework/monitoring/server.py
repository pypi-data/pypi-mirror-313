import logging
from pathlib import Path

from aiohttp.web import (
    Application,
    GracefulExit,
    _run_app,
    normalize_path_middleware,
    static,
)

from lisa.globalfit.framework.monitoring import api, ui

logger = logging.getLogger(__name__)


class MonitoringServer:
    def __init__(self, api_url: str, s3_bucket_name: str) -> None:
        self.app = Application(middlewares=[normalize_path_middleware()])
        api.register(self.app, "/api", s3_bucket_name)
        ui.register(self.app, "/app", api_url)
        self.app.add_routes([static("/static", Path(__file__).parent / "static")])

    async def run(self, port: int) -> None:
        try:
            await _run_app(self.app, port=port)
        except (GracefulExit, KeyboardInterrupt):
            logger.info("stopping server")
