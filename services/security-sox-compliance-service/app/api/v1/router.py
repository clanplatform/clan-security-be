from fastapi import APIRouter
from app.api.v1.endpoints import controls_router, assessments_router

router = APIRouter()
router.include_router(controls_router, prefix="/sox-controls", tags=["sox-controls"])
router.include_router(assessments_router, prefix="/sox-assessments", tags=["sox-assessments"])
