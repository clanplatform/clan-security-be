import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class PolicyCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    category: str = Field(..., min_length=1, max_length=100)
    content: str = Field(..., min_length=1)
    owner: Optional[str] = None
    effective_date: Optional[datetime] = None
    expiry_date: Optional[datetime] = None
    tenant_id: Optional[str] = None


class PolicyUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    category: Optional[str] = None
    content: Optional[str] = None
    owner: Optional[str] = None
    effective_date: Optional[datetime] = None
    expiry_date: Optional[datetime] = None
    review_date: Optional[datetime] = None


class PolicyResponse(BaseModel):
    id: uuid.UUID
    name: str
    category: str
    content: str
    version: int
    status: str
    owner: Optional[str]
    effective_date: Optional[datetime]
    expiry_date: Optional[datetime]
    review_date: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    tenant_id: Optional[str]

    model_config = {"from_attributes": True}


class PolicyViolationCreate(BaseModel):
    description: str = Field(..., min_length=1)
    severity: str = Field(default="MEDIUM", pattern="^(LOW|MEDIUM|HIGH|CRITICAL)$")
    reporter: Optional[str] = None


class PolicyViolationResponse(BaseModel):
    id: uuid.UUID
    policy_id: uuid.UUID
    description: str
    severity: str
    reporter: Optional[str]
    status: str
    resolution: Optional[str]
    created_at: datetime
    resolved_at: Optional[datetime]

    model_config = {"from_attributes": True}
