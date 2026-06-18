import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class DSRCreate(BaseModel):
    subject_email: str = Field(..., min_length=1, max_length=255)
    request_type: str = Field(..., pattern="^(access|deletion|portability|rectification)$")
    description: Optional[str] = None
    tenant_id: Optional[str] = None


class DSRStatusUpdate(BaseModel):
    status: str = Field(..., pattern="^(PENDING|IN_PROGRESS|COMPLETED|REJECTED|CANCELLED)$")
    handler_notes: Optional[str] = None


class DSRResponse(BaseModel):
    id: uuid.UUID
    subject_email: str
    request_type: str
    status: str
    description: Optional[str]
    handler_notes: Optional[str]
    due_date: Optional[datetime]
    completed_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    tenant_id: Optional[str]

    model_config = {"from_attributes": True}


class ConsentCreate(BaseModel):
    subject_email: str = Field(..., min_length=1, max_length=255)
    purpose: str = Field(..., min_length=1, max_length=255)
    granted: bool = True
    legal_basis: Optional[str] = None
    source: Optional[str] = None
    tenant_id: Optional[str] = None


class ConsentResponse(BaseModel):
    id: uuid.UUID
    subject_email: str
    purpose: str
    granted: bool
    legal_basis: Optional[str]
    source: Optional[str]
    revoked_at: Optional[datetime]
    created_at: datetime
    tenant_id: Optional[str]

    model_config = {"from_attributes": True}
