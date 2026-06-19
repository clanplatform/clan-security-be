from fastapi import APIRouter
from app.api.v1.endpoints import router as mon_router

router = APIRouter()
router.include_router(mon_router, prefix="/monitoring", tags=["monitoring"])
