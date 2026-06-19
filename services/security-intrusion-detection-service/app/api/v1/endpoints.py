import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.ids import SignatureCreate, SignatureResponse, IntrusionEventCreate, IntrusionEventResponse, AnalyzeRequest, AnalyzeResponse
from app.services.ids_service import IDSService
from app.api.deps import get_current_user

router = APIRouter()
service = IDSService()


@router.post("/signatures", response_model=SignatureResponse, status_code=status.HTTP_201_CREATED)
async def create_signature(payload: SignatureCreate, current_user: dict = Depends(get_current_user)):
    return await service.create_signature(payload)


@router.get("/signatures", response_model=List[SignatureResponse])
async def list_signatures(current_user: dict = Depends(get_current_user)):
    return await service.list_signatures()


@router.post("/events", response_model=IntrusionEventResponse, status_code=status.HTTP_201_CREATED)
async def record_event(payload: IntrusionEventCreate, current_user: dict = Depends(get_current_user)):
    return await service.record_event(payload)


@router.get("/events", response_model=List[IntrusionEventResponse])
async def list_events(current_user: dict = Depends(get_current_user)):
    return await service.list_events()


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze(payload: AnalyzeRequest, current_user: dict = Depends(get_current_user)):
    return await service.analyze(payload)


@router.get("/stats")
async def get_stats(current_user: dict = Depends(get_current_user)):
    return await service.get_stats()
