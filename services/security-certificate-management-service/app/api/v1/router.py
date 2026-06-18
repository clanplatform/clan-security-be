from fastapi import APIRouter
from app.api.v1.endpoints import router as cert_router

router = APIRouter()
router.include_router(cert_router, prefix="/certificates", tags=["certificates"])
