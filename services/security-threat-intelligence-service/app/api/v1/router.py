from fastapi import APIRouter
from app.api.v1.endpoints import router as intel_router

router = APIRouter()
router.include_router(intel_router, prefix="/intel", tags=["threat-intelligence"])
