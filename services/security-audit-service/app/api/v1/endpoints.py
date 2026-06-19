import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from app.schemas.audit import AuditEventCreate, AuditEventResponse, AuditReportRequest, AuditReportResponse
from app.services.audit_service import AuditService
from app.api.deps import get_current_user

router = APIRouter()
service = AuditService()


@router.post("/events", response_model=AuditEventResponse, status_code=status.HTTP_201_CREATED)
async def record_event(payload: AuditEventCreate, current_user: dict = Depends(get_current_user)):
    return await service.record_event(payload)


@router.get("/events", response_model=List[AuditEventResponse])
async def list_events(
    actor_id: Optional[str] = Query(None),
    event_type: Optional[str] = Query(None),
    severity: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=500),
    current_user: dict = Depends(get_current_user),
):
    return await service.list_events(actor_id=actor_id, event_type=event_type, severity=severity, limit=limit)


@router.get("/events/{event_id}", response_model=AuditEventResponse)
async def get_event(event_id: uuid.UUID, current_user: dict = Depends(get_current_user)):
    e = await service.get_event(str(event_id))
    if not e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
    return e


@router.post("/reports", response_model=AuditReportResponse)
async def generate_report(payload: AuditReportRequest, current_user: dict = Depends(get_current_user)):
    return await service.generate_report(payload)


@router.get("/summary")
async def get_summary(current_user: dict = Depends(get_current_user)):
    return await service.get_summary()
