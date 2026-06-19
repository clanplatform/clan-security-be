import uuid
from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field


class AuditEventCreate(BaseModel):
    event_type: str = Field(..., min_length=1, max_length=100)
    severity: str = Field(..., pattern="^(INFO|LOW|MEDIUM|HIGH|CRITICAL)$")
    actor_id: Optional[str] = None
    actor_type: Optional[str] = None  # USER, SERVICE, SYSTEM
    resource_type: Optional[str] = None
    resource_id: Optional[str] = None
    action: str = Field(..., min_length=1)
    outcome: str = Field(..., pattern="^(SUCCESS|FAILURE|DENIED|ERROR)$")
    ip_address: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class AuditEventResponse(BaseModel):
    id: uuid.UUID
    event_type: str
    severity: str
    actor_id: Optional[str]
    actor_type: Optional[str]
    resource_type: Optional[str]
    resource_id: Optional[str]
    action: str
    outcome: str
    ip_address: Optional[str]
    metadata: Optional[Dict[str, Any]]
    occurred_at: datetime

    model_config = {"from_attributes": True}


class AuditReportRequest(BaseModel):
    start_date: datetime
    end_date: datetime
    event_types: Optional[List[str]] = None
    severity_filter: Optional[str] = None
    report_title: str = "Security Audit Report"


class AuditReportResponse(BaseModel):
    report_id: str
    title: str
    period_start: datetime
    period_end: datetime
    total_events: int
    events_by_severity: Dict[str, int]
    events_by_outcome: Dict[str, int]
    top_actors: List[Dict[str, Any]]
    generated_at: datetime
