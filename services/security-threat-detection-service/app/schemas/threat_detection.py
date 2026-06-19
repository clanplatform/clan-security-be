import uuid
from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class RuleCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    rule_type: str = Field(..., pattern="^(SIGMA|YARA|SNORT|CUSTOM)$")
    severity: str = Field(..., pattern="^(LOW|MEDIUM|HIGH|CRITICAL)$")
    rule_content: str = Field(..., min_length=1)
    mitre_attack: Optional[str] = None


class RuleResponse(BaseModel):
    id: uuid.UUID
    name: str
    description: Optional[str]
    rule_type: str
    severity: str
    rule_content: str
    mitre_attack: Optional[str]
    is_active: bool
    hit_count: int
    created_at: datetime

    model_config = {"from_attributes": True}


class IOCCreate(BaseModel):
    ioc_type: str = Field(..., pattern="^(IP|DOMAIN|URL|HASH_MD5|HASH_SHA1|HASH_SHA256|EMAIL)$")
    value: str = Field(..., min_length=1)
    confidence: int = Field(default=50, ge=0, le=100)
    severity: str = Field(..., pattern="^(LOW|MEDIUM|HIGH|CRITICAL)$")
    source: Optional[str] = None
    description: Optional[str] = None


class IOCResponse(BaseModel):
    id: uuid.UUID
    ioc_type: str
    value: str
    confidence: int
    severity: str
    source: Optional[str]
    description: Optional[str]
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class DetectRequest(BaseModel):
    event_data: Dict[str, Any]
    source_ip: Optional[str] = None
    domain: Optional[str] = None
    file_hash: Optional[str] = None
    url: Optional[str] = None


class DetectResponse(BaseModel):
    threat_detected: bool
    matched_rules: List[str]
    matched_iocs: List[str]
    overall_severity: Optional[str]
    recommended_action: str
    analyzed_at: datetime
