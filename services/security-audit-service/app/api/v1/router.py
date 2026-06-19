from fastapi import APIRouter
from app.api.v1.endpoints import router as audit_router

router = APIRouter()
router.include_router(audit_router, prefix="/audit", tags=["audit"])
