import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.ddos import (RateLimitRuleCreate, RateLimitRuleResponse,
                                BlockedIPCreate, BlockedIPResponse, AttackEventCreate, AttackEventResponse,
                                TrafficAnalysisRequest, TrafficAnalysisResponse)
from app.services.ddos_service import DDoSService
from app.api.deps import get_current_user

router = APIRouter()
service = DDoSService()


@router.post("/rules", response_model=RateLimitRuleResponse, status_code=status.HTTP_201_CREATED)
async def create_rule(payload: RateLimitRuleCreate, current_user: dict = Depends(get_current_user)):
    return await service.create_rule(payload)


@router.get("/rules", response_model=List[RateLimitRuleResponse])
async def list_rules(current_user: dict = Depends(get_current_user)):
    return await service.list_rules()


@router.post("/blocked-ips", response_model=BlockedIPResponse, status_code=status.HTTP_201_CREATED)
async def block_ip(payload: BlockedIPCreate, current_user: dict = Depends(get_current_user)):
    return await service.block_ip(payload)


@router.get("/blocked-ips", response_model=List[BlockedIPResponse])
async def list_blocked(current_user: dict = Depends(get_current_user)):
    return await service.list_blocked()


@router.delete("/blocked-ips/{ip_id}", status_code=status.HTTP_204_NO_CONTENT)
async def unblock_ip(ip_id: uuid.UUID, current_user: dict = Depends(get_current_user)):
    if not await service.unblock_ip(str(ip_id)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="IP not found")


@router.post("/attacks", response_model=AttackEventResponse, status_code=status.HTTP_201_CREATED)
async def record_attack(payload: AttackEventCreate, current_user: dict = Depends(get_current_user)):
    return await service.record_attack(payload)


@router.get("/attacks", response_model=List[AttackEventResponse])
async def list_attacks(current_user: dict = Depends(get_current_user)):
    return await service.list_attacks()


@router.post("/analyze", response_model=TrafficAnalysisResponse)
async def analyze_traffic(payload: TrafficAnalysisRequest, current_user: dict = Depends(get_current_user)):
    return await service.analyze(payload)
