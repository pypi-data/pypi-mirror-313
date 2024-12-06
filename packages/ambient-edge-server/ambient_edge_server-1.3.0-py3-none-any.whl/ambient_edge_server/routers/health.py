from fastapi import APIRouter, Depends

from ambient_client_common.utils import logger
from ambient_edge_server.models.api import MsgResponse
from ambient_edge_server.services.health_service import HealthService
from ambient_edge_server.services.service_manager import svc_manager

logger.debug("health.py - finished imports")

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/check-in", response_model=MsgResponse)
async def check_in(
    health_svc: HealthService = Depends(svc_manager.get_health_service),
):
    """Check in with the backend API

    Args:
        health_svc (HealthService, optional): Defaults to
            Depends(svc_manager.get_health_service).

    Returns:
        dict: Response
    """

    await health_svc.trigger_check_in()
    return MsgResponse(
        msg="Triggered Check-In",
        status="success",
    )
