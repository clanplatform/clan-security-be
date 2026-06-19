from fastapi import APIRouter
from app.api.v1.endpoints import router as netmon_router

router = APIRouter()
router.include_router(netmon_router, prefix="/network", tags=["network-monitoring"])
