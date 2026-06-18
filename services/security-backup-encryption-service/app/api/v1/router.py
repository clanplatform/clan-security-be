from fastapi import APIRouter
from app.api.v1.endpoints import router as backup_router

router = APIRouter()
router.include_router(backup_router, prefix="/backups", tags=["backup-encryption"])
