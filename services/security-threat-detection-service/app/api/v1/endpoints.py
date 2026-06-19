import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.threat_detection import (RuleCreate, RuleResponse, IOCCreate, IOCResponse, DetectRequest, DetectResponse)
from app.services.threat_detection_service import ThreatDetectionService
from app.api.deps import get_current_user

router = APIRouter()
service = ThreatDetectionService()


@router.post("/rules", response_model=RuleResponse, status_code=status.HTTP_201_CREATED)
async def create_rule(payload: RuleCreate, current_user: dict = Depends(get_current_user)):
    return await service.create_rule(payload)


@router.get("/rules", response_model=List[RuleResponse])
async def list_rules(current_user: dict = Depends(get_current_user)):
    return await service.list_rules()


@router.post("/iocs", response_model=IOCResponse, status_code=status.HTTP_201_CREATED)
async def add_ioc(payload: IOCCreate, current_user: dict = Depends(get_current_user)):
    return await service.add_ioc(payload)


@router.get("/iocs", response_model=List[IOCResponse])
async def list_iocs(current_user: dict = Depends(get_current_user)):
    return await service.list_iocs()


@router.post("/detect", response_model=DetectResponse)
async def detect(payload: DetectRequest, current_user: dict = Depends(get_current_user)):
    return await service.detect(payload)


@router.get("/stats")
async def stats(current_user: dict = Depends(get_current_user)):
    return await service.get_stats()
