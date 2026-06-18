import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.privilege import EscalationRequestCreate, EscalationRequestResponse, EscalationDecision
from app.services.privilege_service import PrivilegeService
from app.api.deps import get_current_user

router = APIRouter()
service = PrivilegeService()


@router.post("/requests", response_model=EscalationRequestResponse, status_code=status.HTTP_201_CREATED)
async def create_request(payload: EscalationRequestCreate, current_user: dict = Depends(get_current_user)):
    return await service.create_request(payload, current_user)


@router.get("/requests", response_model=List[EscalationRequestResponse])
async def list_requests(current_user: dict = Depends(get_current_user)):
    return await service.list_requests()


@router.get("/requests/{request_id}", response_model=EscalationRequestResponse)
async def get_request(request_id: uuid.UUID, current_user: dict = Depends(get_current_user)):
    r = await service.get_request(str(request_id))
    if not r:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Request not found")
    return r


@router.post("/requests/{request_id}/approve", response_model=EscalationRequestResponse)
async def approve_request(request_id: uuid.UUID, payload: EscalationDecision, current_user: dict = Depends(get_current_user)):
    r = await service.decide(str(request_id), "APPROVED", payload, current_user)
    if not r:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Request not found")
    return r


@router.post("/requests/{request_id}/reject", response_model=EscalationRequestResponse)
async def reject_request(request_id: uuid.UUID, payload: EscalationDecision, current_user: dict = Depends(get_current_user)):
    r = await service.decide(str(request_id), "REJECTED", payload, current_user)
    if not r:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Request not found")
    return r


@router.post("/requests/{request_id}/revoke", response_model=EscalationRequestResponse)
async def revoke_request(request_id: uuid.UUID, current_user: dict = Depends(get_current_user)):
    r = await service.revoke(str(request_id))
    if not r:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Request not found")
    return r
