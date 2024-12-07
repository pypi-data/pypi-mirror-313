import json
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

from lisa.globalfit.framework.msg.base import MessageBase


@dataclass
class WorkflowSpec(MessageBase):
    resource: str
    labels: list[str] = field(default_factory=list)
    parameters: dict[str, str] = field(default_factory=dict)


@dataclass
class WorkflowResult(MessageBase):
    name: str
    status: str
    labels: list[str] = field(default_factory=list)

    def get_workflow_info(self) -> dict:
        args = ["argo", "get", self.name, "-o", "json"]
        proc = subprocess.run(args, capture_output=True)
        if proc.returncode != 0:
            raise ValueError(
                f"could not get workflow information: {proc.stderr.decode().strip()}"
            )
        return json.loads(proc.stdout)

    def get_workdir(self) -> Path:
        workflow_info = self.get_workflow_info()
        params = [
            p["value"]
            for p in workflow_info["spec"]["arguments"]["parameters"]
            if p["name"] == "workdir"
        ]
        if not params:
            raise ValueError(f"could not find workdir for workflow {workflow_info}")
        return Path(params[0])
