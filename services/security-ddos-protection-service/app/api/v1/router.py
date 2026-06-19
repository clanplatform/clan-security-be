from fastapi import APIRouter
from app.api.v1.endpoints import router as ddos_router

router = APIRouter()
router.include_router(ddos_router, prefix="/ddos", tags=["ddos-protection"])
