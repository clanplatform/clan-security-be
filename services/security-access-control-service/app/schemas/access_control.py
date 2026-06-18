import uuid
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class RoleCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    is_system_role: bool = False
    tenant_id: Optional[str] = None


class RoleResponse(BaseModel):
    id: uuid.UUID
    name: str
    description: Optional[str]
    is_system_role: bool
    is_active: bool
    permissions: List[str] = []
    created_at: datetime
    tenant_id: Optional[str]

    model_config = {"from_attributes": True}


class PermissionCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    resource: str = Field(..., min_length=1, max_length=100)
    action: str = Field(..., pattern="^(CREATE|READ|UPDATE|DELETE|EXECUTE|ADMIN)$")
    description: Optional[str] = None


class PermissionResponse(BaseModel):
    id: uuid.UUID
    name: str
    resource: str
    action: str
    description: Optional[str]
    created_at: datetime

    model_config = {"from_attributes": True}


class RolePermissionAssign(BaseModel):
    permission_id: uuid.UUID


class AccessCheckRequest(BaseModel):
    subject: str = Field(..., description="User or service ID")
    roles: List[str] = []
    resource: str
    action: str


class AccessCheckResponse(BaseModel):
    allowed: bool
    subject: str
    resource: str
    action: str
    matched_permission: Optional[str] = None
    reason: str
