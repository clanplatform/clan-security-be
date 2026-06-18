from fastapi import APIRouter
from app.api.v1.endpoints import router as key_router

router = APIRouter()
router.include_router(key_router, prefix="/keys", tags=["key-management"])
