from typing import Optional

import fastapi

from ambient_client_common.utils import logger
from ambient_edge_server.services.event_service import EventService
from ambient_edge_server.services.service_manager import svc_manager

logger.debug("plugins.py - finished imports")

router = fastapi.APIRouter(tags=["plugins"])
logger.debug("plugins.py - created router")


@router.post("/plugins/{plugin_name}/{custom_endpoint}")
async def handle_custom_plugin_endpoint_post(
    plugin_name: str,
    custom_endpoint: str,
    request: fastapi.Request,
    body: Optional[dict] = None,
    event_service: EventService = fastapi.Depends(svc_manager.get_event_service),
):
    return await event_service.handle_plugin_api_request("post", request.url.path, body)


@router.get("/plugins/{plugin_name}/{custom_endpoint}")
async def handle_custom_plugin_endpoint_get(
    plugin_name: str,
    custom_endpoint: str,
    request: fastapi.Request,
    event_service: EventService = fastapi.Depends(svc_manager.get_event_service),
):
    return await event_service.handle_plugin_api_request("get", request.url.path)


@router.put("/plugins/{plugin_name}/{custom_endpoint}")
async def handle_custom_plugin_endpoint_put(
    plugin_name: str,
    custom_endpoint: str,
    request: fastapi.Request,
    body: Optional[dict] = None,
    event_service: EventService = fastapi.Depends(svc_manager.get_event_service),
):
    return await event_service.handle_plugin_api_request("put", request.url.path, body)


@router.delete("/plugins/{plugin_name}/{custom_endpoint}")
async def handle_custom_plugin_endpoint_delete(
    plugin_name: str,
    custom_endpoint: str,
    request: fastapi.Request,
    event_service: EventService = fastapi.Depends(svc_manager.get_event_service),
):
    return await event_service.handle_plugin_api_request("delete", request.url.path)


logger.debug("plugins.py - created routes")
