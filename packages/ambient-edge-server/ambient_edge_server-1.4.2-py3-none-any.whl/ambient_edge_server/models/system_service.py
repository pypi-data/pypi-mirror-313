import pathlib
from typing import Optional

from pydantic import BaseModel


class ServiceConfigBase(BaseModel):
    environment: Optional[dict] = None


def get_exec_start() -> str:
    exec_path = pathlib.Path.home() / ".ambient/.venv/bin/ambient_edge_server"
    return str(exec_path)


class ServiceConfigLinux(ServiceConfigBase):
    description: str = "Ambient Edge Server"
    user: str
    group: str
    exec_start: str = get_exec_start()
