from fastapi import APIRouter
from app.api.v1.endpoints import router as fw_router

router = APIRouter()
router.include_router(fw_router, prefix="/firewall", tags=["firewall"])
