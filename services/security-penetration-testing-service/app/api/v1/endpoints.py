import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.pentest import (EngagementCreate, EngagementResponse, FindingCreate, FindingResponse, ReportResponse)
from app.services.pentest_service import PentestService
from app.api.deps import get_current_user

router = APIRouter()
service = PentestService()


@router.post("/engagements", response_model=EngagementResponse, status_code=status.HTTP_201_CREATED)
async def create_engagement(payload: EngagementCreate, current_user: dict = Depends(get_current_user)):
    return await service.create_engagement(payload, current_user)


@router.get("/engagements", response_model=List[EngagementResponse])
async def list_engagements(current_user: dict = Depends(get_current_user)):
    return await service.list_engagements()


@router.get("/engagements/{engagement_id}", response_model=EngagementResponse)
async def get_engagement(engagement_id: uuid.UUID, current_user: dict = Depends(get_current_user)):
    e = await service.get_engagement(str(engagement_id))
    if not e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Engagement not found")
    return e


@router.post("/engagements/{engagement_id}/findings", response_model=FindingResponse, status_code=status.HTTP_201_CREATED)
async def add_finding(engagement_id: uuid.UUID, payload: FindingCreate, current_user: dict = Depends(get_current_user)):
    f = await service.add_finding(str(engagement_id), payload)
    if not f:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Engagement not found")
    return f


@router.get("/engagements/{engagement_id}/findings", response_model=List[FindingResponse])
async def list_findings(engagement_id: uuid.UUID, current_user: dict = Depends(get_current_user)):
    return await service.list_findings(str(engagement_id))


@router.get("/engagements/{engagement_id}/report", response_model=ReportResponse)
async def get_report(engagement_id: uuid.UUID, current_user: dict = Depends(get_current_user)):
    r = await service.generate_report(str(engagement_id))
    if not r:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Engagement not found")
    return r
