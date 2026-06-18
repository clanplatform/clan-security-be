from fastapi import APIRouter
from app.api.v1.endpoints import router as session_router

router = APIRouter()
router.include_router(session_router, prefix="/sessions", tags=["session-security"])
