from fastapi import APIRouter
from app.api.v1.endpoints import router as hsm_router

router = APIRouter()
router.include_router(hsm_router, prefix="/hsm", tags=["hsm"])
