from fastapi import APIRouter
from app.api.v1.endpoints import router as class_router

router = APIRouter()
router.include_router(class_router, prefix="/classifications", tags=["data-classification"])
