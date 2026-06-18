from fastapi import APIRouter
from app.api.v1.endpoints import router as acl_router

router = APIRouter()
router.include_router(acl_router, prefix="/access-control", tags=["access-control"])
