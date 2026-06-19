from fastapi import APIRouter
from app.api.v1.endpoints import router as log_router

router = APIRouter()
router.include_router(log_router, prefix="/logs", tags=["log-analysis"])
