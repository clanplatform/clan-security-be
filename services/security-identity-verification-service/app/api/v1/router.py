from fastapi import APIRouter
from app.api.v1.endpoints import router as idv_router

router = APIRouter()
router.include_router(idv_router, prefix="/identity", tags=["identity-verification"])
