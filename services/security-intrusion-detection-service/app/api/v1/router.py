from fastapi import APIRouter
from app.api.v1.endpoints import router as ids_router

router = APIRouter()
router.include_router(ids_router, prefix="/ids", tags=["intrusion-detection"])
