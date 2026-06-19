import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.forensics import CaseCreate, CaseResponse, EvidenceCreate, EvidenceResponse, ChainOfCustodyEntry
from app.services.forensics_service import ForensicsService
from app.api.deps import get_current_user

router = APIRouter()
service = ForensicsService()


@router.post("/cases", response_model=CaseResponse, status_code=status.HTTP_201_CREATED)
async def create_case(payload: CaseCreate, current_user: dict = Depends(get_current_user)):
    return await service.create_case(payload, current_user)


@router.get("/cases", response_model=List[CaseResponse])
async def list_cases(current_user: dict = Depends(get_current_user)):
    return await service.list_cases()


@router.get("/cases/{case_id}", response_model=CaseResponse)
async def get_case(case_id: uuid.UUID, current_user: dict = Depends(get_current_user)):
    c = await service.get_case(str(case_id))
    if not c:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Case not found")
    return c


@router.post("/cases/{case_id}/evidence", response_model=EvidenceResponse, status_code=status.HTTP_201_CREATED)
async def add_evidence(case_id: uuid.UUID, payload: EvidenceCreate, current_user: dict = Depends(get_current_user)):
    ev = await service.add_evidence(str(case_id), payload, current_user)
    if not ev:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Case not found")
    return ev


@router.get("/cases/{case_id}/evidence", response_model=List[EvidenceResponse])
async def list_evidence(case_id: uuid.UUID, current_user: dict = Depends(get_current_user)):
    return await service.list_evidence(str(case_id))


@router.get("/cases/{case_id}/chain-of-custody", response_model=List[ChainOfCustodyEntry])
async def get_chain(case_id: uuid.UUID, current_user: dict = Depends(get_current_user)):
    return await service.get_chain(str(case_id))
