from aiohttp import ClientSession
from aiohttp.web import (
    AppKey,
    Application,
    Request,
    Response,
    RouteTableDef,
)
from jinja2 import Environment, PackageLoader, select_autoescape

jinja_env = AppKey("jinja_env", Environment)
api_session = AppKey("api_session", ClientSession)


def render_template(request: Request, filename: str, **kwargs) -> Response:
    template = request.app[jinja_env].get_template(filename)
    return Response(
        text=template.render(**kwargs),
        content_type="text/html",
    )


async def api_get_json(request: Request, path: str) -> dict:
    res = await request.app[api_session].get(f"/api{path}")
    return await res.json()


routes = RouteTableDef()


@routes.get("/")
async def get_root(request: Request) -> Response:
    return render_template(
        request,
        "index.html",
        navigation=[{"caption": "Pipeline runs", "href": "runs"}],
    )


@routes.get("/runs/")
async def get_runs(request: Request) -> Response:
    return render_template(
        request,
        "runs.html",
        **await api_get_json(request, "/runs"),
    )


@routes.get("/runs/{run}/")
async def get_run_details(request: Request) -> Response:
    groups = await api_get_json(request, f"/runs/{request.match_info['run']}/groups")
    return render_template(
        request,
        "run_details.html",
        **groups,
    )


@routes.get("/runs/{run}/groups/{group}/modules/{module}")
async def get_module_details(request: Request) -> Response:
    details = await api_get_json(
        request,
        "/".join(
            (
                "/runs",
                request.match_info["run"],
                "groups",
                request.match_info["group"],
                "modules",
                request.match_info["module"],
            )
        ),
    )
    return render_template(
        request,
        "module_details.html",
        **details,
    )


def register(app: Application, prefix: str, api_url: str):
    subapp = Application()
    subapp.add_routes(routes)

    # Configure Jinja.
    subapp[jinja_env] = Environment(
        loader=PackageLoader(__name__, "templates"),
        autoescape=select_autoescape(),
    )
    subapp[api_session] = ClientSession(base_url=api_url)

    app.add_subapp(prefix, subapp)
