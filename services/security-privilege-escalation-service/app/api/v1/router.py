from fastapi import APIRouter
from app.api.v1.endpoints import router as priv_router

router = APIRouter()
router.include_router(priv_router, prefix="/privilege", tags=["privilege-escalation"])
