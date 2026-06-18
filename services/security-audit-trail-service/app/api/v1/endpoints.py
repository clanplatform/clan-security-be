import uuid
from typing import Optional, List
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query, status
from app.schemas.audit_trail import AuditEntryCreate, AuditEntryResponse, AuditSearchParams
from app.services.audit_trail_service import AuditTrailService
from app.api.deps import get_current_user

router = APIRouter()
service = AuditTrailService()


@router.post("/", response_model=AuditEntryResponse, status_code=status.HTTP_201_CREATED)
async def create_audit_entry(
    payload: AuditEntryCreate,
    current_user: dict = Depends(get_current_user),
):
    return await service.create_entry(payload)


@router.get("/", response_model=List[AuditEntryResponse])
async def list_audit_entries(
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=500),
    user_id: Optional[str] = Query(None),
    action: Optional[str] = Query(None),
    resource: Optional[str] = Query(None),
    from_date: Optional[datetime] = Query(None),
    to_date: Optional[datetime] = Query(None),
    current_user: dict = Depends(get_current_user),
):
    params = AuditSearchParams(
        user_id=user_id, action=action, resource=resource,
        from_date=from_date, to_date=to_date,
        page=page, page_size=page_size,
    )
    return await service.search_entries(params)


@router.get("/{entry_id}", response_model=AuditEntryResponse)
async def get_audit_entry(
    entry_id: uuid.UUID,
    current_user: dict = Depends(get_current_user),
):
    entry = await service.get_entry(str(entry_id))
    if not entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Audit entry not found")
    return entry


@router.get("/summary/stats")
async def get_audit_stats(
    from_date: Optional[datetime] = Query(None),
    to_date: Optional[datetime] = Query(None),
    current_user: dict = Depends(get_current_user),
):
    return await service.get_stats(from_date, to_date)
