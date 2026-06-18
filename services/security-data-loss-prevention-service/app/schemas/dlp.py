import uuid
from datetime import datetime
from typing import Optional, List, Any, Dict
from pydantic import BaseModel, Field


class DLPRuleCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    rule_type: str = Field(..., pattern="^(REGEX|KEYWORD|ML_MODEL)$")
    pattern: str = Field(..., min_length=1)
    severity: str = Field(default="MEDIUM", pattern="^(LOW|MEDIUM|HIGH|CRITICAL)$")
    action: str = Field(default="ALERT", pattern="^(ALERT|BLOCK|ENCRYPT)$")
    description: Optional[str] = None


class DLPRuleResponse(BaseModel):
    id: uuid.UUID
    name: str
    rule_type: str
    pattern: str
    severity: str
    action: str
    description: Optional[str]
    is_active: bool
    match_count: int
    created_at: datetime

    model_config = {"from_attributes": True}


class DLPViolationResponse(BaseModel):
    id: uuid.UUID
    rule_id: uuid.UUID
    rule_name: str
    content_snippet: Optional[str]
    source: Optional[str]
    severity: str
    action_taken: str
    user_id: Optional[str]
    is_resolved: bool
    resolution_notes: Optional[str]
    detected_at: datetime
    resolved_at: Optional[datetime]

    model_config = {"from_attributes": True}


class ScanRequest(BaseModel):
    content: str = Field(..., min_length=1)
    source: Optional[str] = None
    user_id: Optional[str] = None


class ScanResult(BaseModel):
    violations_found: int
    violations: List[Dict[str, Any]]
    blocked: bool
    scan_duration_ms: float
