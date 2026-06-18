import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from app.schemas.dlp import DLPRuleCreate, DLPRuleResponse, DLPViolationResponse, ScanRequest, ScanResult
from app.services.dlp_service import DLPService
from app.api.deps import get_current_user

rules_router = APIRouter()
violations_router = APIRouter()
service = DLPService()


@rules_router.post("/", response_model=DLPRuleResponse, status_code=status.HTTP_201_CREATED)
async def create_rule(payload: DLPRuleCreate, current_user: dict = Depends(get_current_user)):
    return await service.create_rule(payload)


@rules_router.get("/", response_model=List[DLPRuleResponse])
async def list_rules(
    rule_type: Optional[str] = Query(None),
    current_user: dict = Depends(get_current_user),
):
    return await service.list_rules(rule_type=rule_type)


@rules_router.delete("/{rule_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_rule(rule_id: uuid.UUID, current_user: dict = Depends(get_current_user)):
    if not await service.delete_rule(str(rule_id)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rule not found")


@rules_router.post("/scan", response_model=ScanResult)
async def scan_content(payload: ScanRequest, current_user: dict = Depends(get_current_user)):
    return await service.scan(payload)


@violations_router.get("/", response_model=List[DLPViolationResponse])
async def list_violations(
    severity: Optional[str] = Query(None),
    resolved: Optional[bool] = Query(None),
    current_user: dict = Depends(get_current_user),
):
    return await service.list_violations(severity=severity, resolved=resolved)


@violations_router.put("/{violation_id}/resolve", response_model=DLPViolationResponse)
async def resolve_violation(violation_id: uuid.UUID, current_user: dict = Depends(get_current_user)):
    v = await service.resolve_violation(str(violation_id))
    if not v:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Violation not found")
    return v
