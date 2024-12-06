from typing import Optional

from fastapi import APIRouter, HTTPException

from ambient_edge_server.services.upgrade_service import UpgradeService

router = APIRouter(prefix="/software", tags=["software"])


@router.post("/upgrade")
async def upgrade_to_latest(version: Optional[str] = None):
    upgrade_service = UpgradeService()
    try:
        if version:
            return upgrade_service.upgrade_software(version)
        return await upgrade_service.upgrade_to_latest()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
