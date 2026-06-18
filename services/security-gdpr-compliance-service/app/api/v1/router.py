from fastapi import APIRouter
from app.api.v1.endpoints import dsr_router, consent_router

router = APIRouter()
router.include_router(dsr_router, prefix="/data-subject-requests", tags=["data-subject-requests"])
router.include_router(consent_router, prefix="/consent-records", tags=["consent"])
