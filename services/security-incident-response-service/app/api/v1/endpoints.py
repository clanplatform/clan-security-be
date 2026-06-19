import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from app.schemas.incident import (IncidentCreate, IncidentResponse, IncidentUpdate,
                                   TimelineEntryCreate, TimelineEntryResponse)
from app.services.incident_service import IncidentService
from app.api.deps import get_current_user

router = APIRouter()
service = IncidentService()


@router.post("/", response_model=IncidentResponse, status_code=status.HTTP_201_CREATED)
async def create_incident(payload: IncidentCreate, current_user: dict = Depends(get_current_user)):
    return await service.create_incident(payload, current_user)


@router.get("/", response_model=List[IncidentResponse])
async def list_incidents(status_filter: Optional[str] = Query(None, alias="status"),
                         severity: Optional[str] = Query(None),
                         current_user: dict = Depends(get_current_user)):
    return await service.list_incidents(status_filter=status_filter, severity=severity)


@router.get("/{incident_id}", response_model=IncidentResponse)
async def get_incident(incident_id: uuid.UUID, current_user: dict = Depends(get_current_user)):
    inc = await service.get_incident(str(incident_id))
    if not inc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incident not found")
    return inc


@router.patch("/{incident_id}", response_model=IncidentResponse)
async def update_incident(incident_id: uuid.UUID, payload: IncidentUpdate, current_user: dict = Depends(get_current_user)):
    inc = await service.update_incident(str(incident_id), payload)
    if not inc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incident not found")
    return inc


@router.post("/{incident_id}/timeline", response_model=TimelineEntryResponse, status_code=status.HTTP_201_CREATED)
async def add_timeline(incident_id: uuid.UUID, payload: TimelineEntryCreate, current_user: dict = Depends(get_current_user)):
    entry = await service.add_timeline(str(incident_id), payload, current_user)
    if not entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incident not found")
    return entry


@router.get("/{incident_id}/timeline", response_model=List[TimelineEntryResponse])
async def get_timeline(incident_id: uuid.UUID, current_user: dict = Depends(get_current_user)):
    return await service.get_timeline(str(incident_id))
