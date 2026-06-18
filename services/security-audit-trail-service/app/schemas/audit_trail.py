import uuid
from datetime import datetime
from typing import Optional, Any, Dict
from pydantic import BaseModel, Field


class AuditEntryCreate(BaseModel):
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    action: str = Field(..., min_length=1, max_length=255)
    resource: str = Field(..., min_length=1, max_length=500)
    resource_id: Optional[str] = None
    result: str = Field(default="SUCCESS", pattern="^(SUCCESS|FAILURE|ERROR|DENIED)$")
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    service: str = Field(..., min_length=1, max_length=255)
    severity: str = Field(default="INFO", pattern="^(DEBUG|INFO|WARNING|ERROR|CRITICAL)$")
    details: Optional[Dict[str, Any]] = None
    tenant_id: Optional[str] = None
    correlation_id: Optional[str] = None


class AuditEntryResponse(BaseModel):
    id: uuid.UUID
    timestamp: datetime
    user_id: Optional[str]
    session_id: Optional[str]
    action: str
    resource: str
    resource_id: Optional[str]
    result: str
    ip_address: Optional[str]
    service: str
    severity: str
    details: Optional[Dict[str, Any]]
    tenant_id: Optional[str]
    correlation_id: Optional[str]

    model_config = {"from_attributes": True}


class AuditSearchParams(BaseModel):
    user_id: Optional[str] = None
    action: Optional[str] = None
    resource: Optional[str] = None
    from_date: Optional[datetime] = None
    to_date: Optional[datetime] = None
    page: int = 1
    page_size: int = 50
