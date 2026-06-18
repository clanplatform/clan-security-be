import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.access_control import (RoleCreate, RoleResponse, PermissionCreate, PermissionResponse,
                                         AccessCheckRequest, AccessCheckResponse, RolePermissionAssign)
from app.services.access_control_service import AccessControlService
from app.api.deps import get_current_user

router = APIRouter()
service = AccessControlService()


@router.post("/roles", response_model=RoleResponse, status_code=status.HTTP_201_CREATED)
async def create_role(payload: RoleCreate, current_user: dict = Depends(get_current_user)):
    return await service.create_role(payload)


@router.get("/roles", response_model=List[RoleResponse])
async def list_roles(current_user: dict = Depends(get_current_user)):
    return await service.list_roles()


@router.post("/permissions", response_model=PermissionResponse, status_code=status.HTTP_201_CREATED)
async def create_permission(payload: PermissionCreate, current_user: dict = Depends(get_current_user)):
    return await service.create_permission(payload)


@router.get("/permissions", response_model=List[PermissionResponse])
async def list_permissions(current_user: dict = Depends(get_current_user)):
    return await service.list_permissions()


@router.post("/roles/{role_id}/permissions", response_model=RoleResponse)
async def assign_permission(role_id: uuid.UUID, payload: RolePermissionAssign, current_user: dict = Depends(get_current_user)):
    role = await service.assign_permission(str(role_id), payload)
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
    return role


@router.post("/check", response_model=AccessCheckResponse)
async def check_access(payload: AccessCheckRequest, current_user: dict = Depends(get_current_user)):
    return await service.check_access(payload)
