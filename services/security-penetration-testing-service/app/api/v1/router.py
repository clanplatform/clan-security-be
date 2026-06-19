from fastapi import APIRouter
from app.api.v1.endpoints import router as pentest_router

router = APIRouter()
router.include_router(pentest_router, prefix="/pentest", tags=["penetration-testing"])
