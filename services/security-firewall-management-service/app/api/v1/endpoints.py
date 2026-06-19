import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.firewall import FirewallRuleCreate, FirewallRuleResponse, PacketCheckRequest, PacketCheckResponse
from app.services.firewall_service import FirewallService
from app.api.deps import get_current_user

router = APIRouter()
service = FirewallService()


@router.post("/rules", response_model=FirewallRuleResponse, status_code=status.HTTP_201_CREATED)
async def create_rule(payload: FirewallRuleCreate, current_user: dict = Depends(get_current_user)):
    return await service.create_rule(payload)


@router.get("/rules", response_model=List[FirewallRuleResponse])
async def list_rules(current_user: dict = Depends(get_current_user)):
    return await service.list_rules()


@router.get("/rules/{rule_id}", response_model=FirewallRuleResponse)
async def get_rule(rule_id: uuid.UUID, current_user: dict = Depends(get_current_user)):
    r = await service.get_rule(str(rule_id))
    if not r:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rule not found")
    return r


@router.put("/rules/{rule_id}/toggle", response_model=FirewallRuleResponse)
async def toggle_rule(rule_id: uuid.UUID, current_user: dict = Depends(get_current_user)):
    r = await service.toggle(str(rule_id))
    if not r:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rule not found")
    return r


@router.delete("/rules/{rule_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_rule(rule_id: uuid.UUID, current_user: dict = Depends(get_current_user)):
    if not await service.delete_rule(str(rule_id)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rule not found")


@router.post("/check", response_model=PacketCheckResponse)
async def check_packet(payload: PacketCheckRequest, current_user: dict = Depends(get_current_user)):
    return await service.check_packet(payload)
