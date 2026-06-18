from fastapi import APIRouter
from app.api.v1.endpoints import router as enc_router

router = APIRouter()
router.include_router(enc_router, prefix="/encryption", tags=["encryption"])
