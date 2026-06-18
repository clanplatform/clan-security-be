import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from app.schemas.sox import SOXControlCreate, SOXControlResponse, SOXAssessmentCreate, SOXAssessmentResponse
from app.services.sox_service import SOXService
from app.api.deps import get_current_user

controls_router = APIRouter()
assessments_router = APIRouter()
service = SOXService()


@controls_router.post("/", response_model=SOXControlResponse, status_code=status.HTTP_201_CREATED)
async def create_control(payload: SOXControlCreate, current_user: dict = Depends(get_current_user)):
    return await service.create_control(payload)


@controls_router.get("/", response_model=List[SOXControlResponse])
async def list_controls(
    control_type: Optional[str] = Query(None),
    owner: Optional[str] = Query(None),
    current_user: dict = Depends(get_current_user),
):
    return await service.list_controls(control_type=control_type, owner=owner)


@controls_router.get("/{control_id}", response_model=SOXControlResponse)
async def get_control(control_id: uuid.UUID, current_user: dict = Depends(get_current_user)):
    ctrl = await service.get_control(str(control_id))
    if not ctrl:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="SOX control not found")
    return ctrl


@assessments_router.post("/", response_model=SOXAssessmentResponse, status_code=status.HTTP_201_CREATED)
async def create_assessment(payload: SOXAssessmentCreate, current_user: dict = Depends(get_current_user)):
    return await service.create_assessment(payload)


@assessments_router.get("/", response_model=List[SOXAssessmentResponse])
async def list_assessments(
    period: Optional[str] = Query(None),
    result: Optional[str] = Query(None),
    current_user: dict = Depends(get_current_user),
):
    return await service.list_assessments(period=period, result=result)


@assessments_router.get("/report/{period}")
async def get_period_report(period: str, current_user: dict = Depends(get_current_user)):
    return await service.get_period_report(period)
