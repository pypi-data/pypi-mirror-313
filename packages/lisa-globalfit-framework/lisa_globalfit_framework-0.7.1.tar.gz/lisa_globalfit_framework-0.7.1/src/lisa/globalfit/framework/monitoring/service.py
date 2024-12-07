from operator import itemgetter
from pathlib import Path
from tempfile import NamedTemporaryFile

from lisa.globalfit.framework.monitoring.types import MonitoringStorage
from lisa.globalfit.framework.msg.subjects import (
    SUBJECT_GLOBALFIT,
    channel_get_group,
    channel_get_module,
    channel_get_pipeline,
)
from lisa.globalfit.framework.plot import ModuleExecutionDrawer


async def get_runs(storage: MonitoringStorage):
    runs = {}
    paginator = storage.client.get_paginator("list_objects_v2")
    async for result in paginator.paginate(
        Bucket=storage.bucket,
        Prefix="lisa-checkpoint",
    ):
        for item in result.get("Contents", []):
            run_id = channel_get_pipeline(item["Key"])
            last_modified = item["LastModified"]
            if run_id not in runs:
                runs[run_id] = {"run_id": run_id, "date": last_modified}
            else:
                runs[run_id]["date"] = max(runs[run_id]["date"], last_modified)

    return {"runs": sorted(runs.values(), key=itemgetter("date"), reverse=True)}


async def get_run_groups(storage: MonitoringStorage, run_id: str):
    groups = {}
    paginator = storage.client.get_paginator("list_objects_v2")
    async for result in paginator.paginate(
        Bucket=storage.bucket,
        Prefix=f"lisa-checkpoint-{SUBJECT_GLOBALFIT}.{run_id}",
    ):
        for item in result.get("Contents", []):
            group = channel_get_group(item["Key"])
            module = channel_get_module(item["Key"])
            if group not in groups:
                groups[group] = {"group_id": group, "modules": {module}}
            else:
                # mypy does not understand the in-place assignment,
                # so we split it in three steps
                group_modules = set(groups[group]["modules"])
                group_modules.add(module)
                groups[group]["modules"] = group_modules

    # Sort module names within each group.
    for group_id, item in groups.items():
        groups[group_id]["modules"] = sorted(item["modules"])

    return {"groups": sorted(groups.values(), key=itemgetter("group_id"))}


async def get_run_group_modules(storage: MonitoringStorage, run_id: str, group_id: str):
    paginator = storage.client.get_paginator("list_objects_v2")
    return sorted(
        {
            channel_get_module(item["Key"])
            async for result in paginator.paginate(
                Bucket=storage.bucket,
                Prefix=f"lisa-checkpoint-{SUBJECT_GLOBALFIT}.{run_id}.{group_id}",
            )
            for item in result.get("Contents", [])
        }
    )


async def get_run_group_module(
    storage: MonitoringStorage, run_id: str, group_id: str, module_id: str
):
    response = await storage.client.get_object(
        Bucket=storage.bucket,
        Key=f"lisa-checkpoint-{SUBJECT_GLOBALFIT}.{run_id}.{group_id}.{module_id}",
    )

    # TODO Refactor into self-contained functions.
    with (
        NamedTemporaryFile() as input_data,
        NamedTemporaryFile(suffix=".svg") as output_img,
    ):
        async for chunk in response["Body"].iter_chunks():
            input_data.write(chunk)
        input_data.flush()

        ModuleExecutionDrawer().plot_corner(
            Path(input_data.name), "mcmc/chain", Path(output_img.name)
        )
        return {"plots": [{"src": output_img.read().decode()}]}
