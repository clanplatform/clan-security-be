import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from app.schemas.gdpr import (
    DSRCreate, DSRResponse, DSRStatusUpdate,
    ConsentCreate, ConsentResponse,
)
from app.services.gdpr_service import GDPRService
from app.api.deps import get_current_user

dsr_router = APIRouter()
consent_router = APIRouter()
service = GDPRService()


@dsr_router.post("/", response_model=DSRResponse, status_code=status.HTTP_201_CREATED)
async def create_dsr(payload: DSRCreate, current_user: dict = Depends(get_current_user)):
    return await service.create_dsr(payload)


@dsr_router.get("/", response_model=List[DSRResponse])
async def list_dsrs(
    status_filter: Optional[str] = Query(None, alias="status"),
    request_type: Optional[str] = Query(None),
    current_user: dict = Depends(get_current_user),
):
    return await service.list_dsrs(status_filter=status_filter, request_type=request_type)


@dsr_router.get("/{dsr_id}", response_model=DSRResponse)
async def get_dsr(dsr_id: uuid.UUID, current_user: dict = Depends(get_current_user)):
    dsr = await service.get_dsr(str(dsr_id))
    if not dsr:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="DSR not found")
    return dsr


@dsr_router.put("/{dsr_id}/status", response_model=DSRResponse)
async def update_dsr_status(
    dsr_id: uuid.UUID,
    payload: DSRStatusUpdate,
    current_user: dict = Depends(get_current_user),
):
    dsr = await service.update_dsr_status(str(dsr_id), payload)
    if not dsr:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="DSR not found")
    return dsr


@consent_router.post("/", response_model=ConsentResponse, status_code=status.HTTP_201_CREATED)
async def record_consent(payload: ConsentCreate, current_user: dict = Depends(get_current_user)):
    return await service.record_consent(payload)


@consent_router.get("/", response_model=List[ConsentResponse])
async def list_consents(
    subject_email: Optional[str] = Query(None),
    purpose: Optional[str] = Query(None),
    current_user: dict = Depends(get_current_user),
):
    return await service.list_consents(subject_email=subject_email, purpose=purpose)


@consent_router.delete("/{consent_id}", status_code=status.HTTP_204_NO_CONTENT)
async def revoke_consent(consent_id: uuid.UUID, current_user: dict = Depends(get_current_user)):
    revoked = await service.revoke_consent(str(consent_id))
    if not revoked:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Consent record not found")
