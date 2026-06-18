import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class SOXControlCreate(BaseModel):
    control_id: str = Field(..., min_length=1, max_length=50)
    objective: str = Field(..., min_length=1)
    control_type: str = Field(..., pattern="^(PREVENTIVE|DETECTIVE|CORRECTIVE)$")
    frequency: str = Field(..., pattern="^(DAILY|WEEKLY|MONTHLY|QUARTERLY|ANNUAL)$")
    owner: str = Field(..., min_length=1)
    process: Optional[str] = None
    risk_level: str = Field(default="MEDIUM", pattern="^(LOW|MEDIUM|HIGH|CRITICAL)$")


class SOXControlResponse(BaseModel):
    id: uuid.UUID
    control_id: str
    objective: str
    control_type: str
    frequency: str
    owner: str
    process: Optional[str]
    risk_level: str
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class SOXAssessmentCreate(BaseModel):
    control_id: uuid.UUID
    period: str = Field(..., pattern=r"^\d{4}-Q[1-4]$")
    result: str = Field(..., pattern="^(EFFECTIVE|INEFFECTIVE|NOT_TESTED)$")
    evidence: Optional[str] = None
    assessor: Optional[str] = None
    deficiencies: Optional[str] = None
    remediation_plan: Optional[str] = None


class SOXAssessmentResponse(BaseModel):
    id: uuid.UUID
    control_id: uuid.UUID
    period: str
    result: str
    evidence: Optional[str]
    assessor: Optional[str]
    deficiencies: Optional[str]
    remediation_plan: Optional[str]
    assessed_at: datetime
    next_assessment: Optional[datetime]

    model_config = {"from_attributes": True}
