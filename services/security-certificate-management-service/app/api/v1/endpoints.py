import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from app.schemas.certificate import CertificateCreate, CertificateResponse, CertificateRenewRequest
from app.services.certificate_service import CertificateService
from app.api.deps import get_current_user

router = APIRouter()
service = CertificateService()


@router.post("/", response_model=CertificateResponse, status_code=status.HTTP_201_CREATED)
async def create_certificate(payload: CertificateCreate, current_user: dict = Depends(get_current_user)):
    return await service.create_certificate(payload)


@router.get("/", response_model=List[CertificateResponse])
async def list_certificates(
    cert_type: Optional[str] = Query(None),
    status_filter: Optional[str] = Query(None, alias="status"),
    expiring_soon: bool = Query(False),
    current_user: dict = Depends(get_current_user),
):
    return await service.list_certificates(cert_type=cert_type, status_filter=status_filter, expiring_soon=expiring_soon)


@router.get("/{cert_id}", response_model=CertificateResponse)
async def get_certificate(cert_id: uuid.UUID, current_user: dict = Depends(get_current_user)):
    cert = await service.get_certificate(str(cert_id))
    if not cert:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Certificate not found")
    return cert


@router.post("/{cert_id}/renew", response_model=CertificateResponse)
async def renew_certificate(cert_id: uuid.UUID, payload: CertificateRenewRequest, current_user: dict = Depends(get_current_user)):
    cert = await service.renew_certificate(str(cert_id), payload)
    if not cert:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Certificate not found")
    return cert


@router.post("/{cert_id}/revoke", response_model=CertificateResponse)
async def revoke_certificate(cert_id: uuid.UUID, current_user: dict = Depends(get_current_user)):
    cert = await service.revoke_certificate(str(cert_id))
    if not cert:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Certificate not found")
    return cert


@router.get("/summary/expiring")
async def get_expiring_certificates(days: int = Query(30, ge=1, le=365), current_user: dict = Depends(get_current_user)):
    return await service.get_expiring(days)
