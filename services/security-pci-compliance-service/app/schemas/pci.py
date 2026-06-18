import uuid
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class PCIControlCreate(BaseModel):
    requirement_id: str = Field(..., min_length=1, max_length=50)
    title: str = Field(..., min_length=1, max_length=500)
    description: Optional[str] = None
    category: str = Field(..., min_length=1)


class PCIControlResponse(BaseModel):
    id: uuid.UUID
    requirement_id: str
    title: str
    description: Optional[str]
    category: str
    status: str
    last_assessed: Optional[datetime]
    created_at: datetime

    model_config = {"from_attributes": True}


class ComplianceCheckCreate(BaseModel):
    control_id: uuid.UUID
    result: str = Field(..., pattern="^(PASS|FAIL|NOT_APPLICABLE)$")
    evidence: Optional[str] = None
    assessor: Optional[str] = None
    notes: Optional[str] = None
    score: Optional[float] = Field(None, ge=0.0, le=100.0)


class ComplianceCheckResponse(BaseModel):
    id: uuid.UUID
    control_id: uuid.UUID
    result: str
    evidence: Optional[str]
    assessor: Optional[str]
    notes: Optional[str]
    score: Optional[float]
    assessed_at: datetime
    next_review: Optional[datetime]

    model_config = {"from_attributes": True}
