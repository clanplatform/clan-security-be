from fastapi import APIRouter
from app.api.v1.endpoints import controls_router, checks_router

router = APIRouter()
router.include_router(controls_router, prefix="/controls", tags=["pci-controls"])
router.include_router(checks_router, prefix="/compliance-checks", tags=["compliance-checks"])
