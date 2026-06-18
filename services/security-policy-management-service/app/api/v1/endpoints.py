import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from app.schemas.policy import PolicyCreate, PolicyResponse, PolicyUpdate, PolicyViolationCreate, PolicyViolationResponse
from app.services.policy_service import PolicyService
from app.api.deps import get_current_user

policies_router = APIRouter()
service = PolicyService()


@policies_router.post("/", response_model=PolicyResponse, status_code=status.HTTP_201_CREATED)
async def create_policy(payload: PolicyCreate, current_user: dict = Depends(get_current_user)):
    return await service.create_policy(payload)


@policies_router.get("/", response_model=List[PolicyResponse])
async def list_policies(
    category: Optional[str] = Query(None),
    policy_status: Optional[str] = Query(None, alias="status"),
    current_user: dict = Depends(get_current_user),
):
    return await service.list_policies(category=category, policy_status=policy_status)


@policies_router.get("/{policy_id}", response_model=PolicyResponse)
async def get_policy(policy_id: uuid.UUID, current_user: dict = Depends(get_current_user)):
    policy = await service.get_policy(str(policy_id))
    if not policy:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Policy not found")
    return policy


@policies_router.put("/{policy_id}", response_model=PolicyResponse)
async def update_policy(policy_id: uuid.UUID, payload: PolicyUpdate, current_user: dict = Depends(get_current_user)):
    policy = await service.update_policy(str(policy_id), payload)
    if not policy:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Policy not found")
    return policy


@policies_router.post("/{policy_id}/activate", response_model=PolicyResponse)
async def activate_policy(policy_id: uuid.UUID, current_user: dict = Depends(get_current_user)):
    policy = await service.set_policy_status(str(policy_id), "ACTIVE")
    if not policy:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Policy not found")
    return policy


@policies_router.post("/{policy_id}/deactivate", response_model=PolicyResponse)
async def deactivate_policy(policy_id: uuid.UUID, current_user: dict = Depends(get_current_user)):
    policy = await service.set_policy_status(str(policy_id), "INACTIVE")
    if not policy:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Policy not found")
    return policy


@policies_router.delete("/{policy_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_policy(policy_id: uuid.UUID, current_user: dict = Depends(get_current_user)):
    deleted = await service.delete_policy(str(policy_id))
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Policy not found")


@policies_router.post("/{policy_id}/violations", response_model=PolicyViolationResponse, status_code=status.HTTP_201_CREATED)
async def report_violation(policy_id: uuid.UUID, payload: PolicyViolationCreate, current_user: dict = Depends(get_current_user)):
    return await service.report_violation(str(policy_id), payload)


@policies_router.get("/{policy_id}/violations", response_model=List[PolicyViolationResponse])
async def get_violations(policy_id: uuid.UUID, current_user: dict = Depends(get_current_user)):
    return await service.get_violations(str(policy_id))
