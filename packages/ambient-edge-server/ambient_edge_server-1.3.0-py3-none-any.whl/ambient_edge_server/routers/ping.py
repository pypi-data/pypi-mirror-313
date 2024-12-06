import aiohttp
from fastapi import APIRouter

from ambient_client_common.utils import logger
from ambient_edge_server.config import settings
from ambient_edge_server.models.api import MsgResponse

logger.debug("ping.py - finished imports")

router = APIRouter()


@router.get("/ping", response_model=MsgResponse)
async def pong(endpoint: str) -> MsgResponse:
    if endpoint == "server":
        return MsgResponse(msg="pong", status="success")
    elif endpoint == "backend":
        async with aiohttp.ClientSession() as session:
            url = f"{settings.backend_api_url}/ping/"
            logger.debug("url: {}", url)
            async with session.get(url) as resp:
                resp.raise_for_status()
                return MsgResponse(msg="pong", status="success")
