import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class EscalationRequestCreate(BaseModel):
    target_role: str = Field(..., min_length=1, max_length=100)
    target_resource: Optional[str] = None
    justification: str = Field(..., min_length=10, max_length=2000)
    duration_hours: int = Field(default=1, ge=1, le=8)
    ticket_id: Optional[str] = None


class EscalationRequestResponse(BaseModel):
    id: uuid.UUID
    requester_id: str
    requester_email: Optional[str]
    target_role: str
    target_resource: Optional[str]
    justification: str
    duration_hours: int
    status: str
    approved_by: Optional[str]
    approval_notes: Optional[str]
    requested_at: datetime
    decided_at: Optional[datetime]
    expires_at: Optional[datetime]
    revoked_at: Optional[datetime]
    ticket_id: Optional[str]

    model_config = {"from_attributes": True}


class EscalationDecision(BaseModel):
    notes: Optional[str] = None
