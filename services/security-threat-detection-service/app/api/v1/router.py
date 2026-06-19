from fastapi import APIRouter
from app.api.v1.endpoints import router as threat_router

router = APIRouter()
router.include_router(threat_router, prefix="/threats", tags=["threat-detection"])
