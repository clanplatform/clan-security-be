from fastapi import APIRouter
from app.api.v1.endpoints import router as mask_router

router = APIRouter()
router.include_router(mask_router, prefix="/masking", tags=["data-masking"])
