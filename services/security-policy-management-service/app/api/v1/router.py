from fastapi import APIRouter
from app.api.v1.endpoints import policies_router

router = APIRouter()
router.include_router(policies_router, prefix="/policies", tags=["policies"])
