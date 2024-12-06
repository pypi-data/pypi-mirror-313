from typing import Optional

from fastapi import APIRouter, Depends, HTTPException

from ambient_edge_server.models.api import MsgResponse
from ambient_edge_server.services.service_manager import svc_manager
from ambient_edge_server.services.system_daemon_service import SystemDaemonService

router = APIRouter(prefix="/daemon", tags=["daemon"])


@router.post("/install", response_model=None)
async def install_service(
    env_vars: Optional[dict] = None,
    daemon_svc: SystemDaemonService = Depends(svc_manager.get_system_daemon_service),
):
    result = await daemon_svc.install(env_vars)
    if result.is_err():
        raise HTTPException(status_code=500, detail=result.unwrap_err())

    # we shouldn't event get here because this endpoint
    # will stop the server (to install the service)
    return None


@router.post("/start", response_model=MsgResponse)
async def start_service(
    daemon_svc: SystemDaemonService = Depends(svc_manager.get_system_daemon_service),
):
    result = await daemon_svc.start()
    if result.is_err():
        raise HTTPException(status_code=500, detail=result.err())

    return MsgResponse(msg="Service started.")


@router.post("/stop", response_model=MsgResponse)
async def stop_service(
    daemon_svc: SystemDaemonService = Depends(svc_manager.get_system_daemon_service),
):
    result = await daemon_svc.stop()
    if result.is_err():
        return MsgResponse(msg=result.unwrap_err(), status="error")
    return MsgResponse(msg=result.unwrap(), status="success")


@router.post("/restart", response_model=MsgResponse)
async def restart_service(
    daemon_svc: SystemDaemonService = Depends(svc_manager.get_system_daemon_service),
):
    result = await daemon_svc.restart()
    if result.is_err():
        return MsgResponse(msg=result.unwrap_err(), status="error")
    return MsgResponse(msg=result.unwrap(), status="success")


@router.get("/status", response_model=MsgResponse)
async def service_status(
    daemon_svc: SystemDaemonService = Depends(svc_manager.get_system_daemon_service),
):
    status = daemon_svc.status
    if status.is_err():
        raise HTTPException(status_code=500, detail=status.err())

    return MsgResponse(msg=status.unwrap())
