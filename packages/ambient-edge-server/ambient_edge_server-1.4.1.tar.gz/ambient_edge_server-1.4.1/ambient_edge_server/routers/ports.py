import base64

from fastapi import APIRouter, Depends

from ambient_client_common.utils import logger
from ambient_edge_server.models.api import MsgResponse
from ambient_edge_server.services.port_service import PortService
from ambient_edge_server.services.service_manager import svc_manager

logger.debug("ports.py - finished imports")

router = APIRouter(prefix="/ports", tags=["ports"])


@router.get("/")
async def get_ports(port_svc: PortService = Depends(svc_manager.get_port_service)):
    return await port_svc.get_ports()


@router.get("/{port_id}")
async def get_port(
    port_id: int, port_svc: PortService = Depends(svc_manager.get_port_service)
):
    return await port_svc.get_port(port_id)


@router.get("/port-forwards")
async def get_port_forwards(
    port_svc: PortService = Depends(svc_manager.get_port_service),
):
    return await port_svc.get_port_forwards()


@router.post("/port-forwards/{port_id}")
async def forward_port(
    port_id: int,
    ws_url: str,
    port_svc: PortService = Depends(svc_manager.get_port_service),
):
    decoded_ws_url = base64.b64decode(ws_url.encode()).decode()
    logger.debug(f"decoded_ws_url: {decoded_ws_url}")
    await port_svc.forward_port(port_id, decoded_ws_url)
    return MsgResponse(msg="Port forwarded", status="success")
