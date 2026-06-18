from fastapi import APIRouter
from app.api.v1.endpoints import rules_router, violations_router

router = APIRouter()
router.include_router(rules_router, prefix="/dlp-rules", tags=["dlp-rules"])
router.include_router(violations_router, prefix="/violations", tags=["violations"])
