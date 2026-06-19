import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class IncidentCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: str = Field(..., min_length=1)
    severity: str = Field(..., pattern="^(LOW|MEDIUM|HIGH|CRITICAL)$")
    incident_type: str = Field(..., pattern="^(DATA_BREACH|MALWARE|PHISHING|INSIDER|RANSOMWARE|DDoS|OTHER)$")
    source: Optional[str] = None
    affected_systems: Optional[str] = None


class IncidentUpdate(BaseModel):
    status: Optional[str] = Field(None, pattern="^(OPEN|IN_PROGRESS|CONTAINED|RESOLVED|CLOSED)$")
    assignee_id: Optional[str] = None
    resolution_notes: Optional[str] = None
    severity: Optional[str] = Field(None, pattern="^(LOW|MEDIUM|HIGH|CRITICAL)$")


class IncidentResponse(BaseModel):
    id: uuid.UUID
    incident_number: str
    title: str
    description: str
    severity: str
    incident_type: str
    status: str
    source: Optional[str]
    affected_systems: Optional[str]
    reporter_id: Optional[str]
    assignee_id: Optional[str]
    resolution_notes: Optional[str]
    created_at: datetime
    updated_at: datetime
    resolved_at: Optional[datetime]

    model_config = {"from_attributes": True}


class TimelineEntryCreate(BaseModel):
    action: str = Field(..., min_length=1, max_length=500)
    details: Optional[str] = None
    entry_type: str = Field(default="NOTE", pattern="^(NOTE|ACTION|ESCALATION|CONTAINMENT|EVIDENCE|RESOLUTION)$")


class TimelineEntryResponse(BaseModel):
    id: uuid.UUID
    incident_id: str
    action: str
    details: Optional[str]
    entry_type: str
    actor_id: str
    occurred_at: datetime
