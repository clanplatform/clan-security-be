from fastapi import APIRouter
from app.api.v1.endpoints import router as forensics_router

router = APIRouter()
router.include_router(forensics_router, prefix="/forensics", tags=["forensics"])
