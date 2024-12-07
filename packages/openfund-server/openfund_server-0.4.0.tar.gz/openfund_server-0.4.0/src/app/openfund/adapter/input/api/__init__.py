from fastapi import APIRouter

from app.openfund.adapter.input.api.v1.collect_api import (
    collect_router as collect_v1_router,
)

router = APIRouter()
router.include_router(collect_v1_router, prefix="/api/v1/collcet", tags=["Collect"])


__all__ = ["router"]
