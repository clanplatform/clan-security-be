from fastapi import APIRouter
from app.api.v1.endpoints import router as ir_router

router = APIRouter()
router.include_router(ir_router, prefix="/incidents", tags=["incident-response"])
