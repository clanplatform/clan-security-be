import uuid
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class SignatureCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    sid: str = Field(..., description="Snort/Suricata-style SID")
    category: str = Field(..., pattern="^(EXPLOIT|SCAN|MALWARE|BOTNET|POLICY|ANOMALY|DOS|RECON)$")
    severity: str = Field(..., pattern="^(LOW|MEDIUM|HIGH|CRITICAL)$")
    pattern: str = Field(..., min_length=1, description="Detection pattern/regex")
    action: str = Field(default="ALERT", pattern="^(ALERT|DROP|REJECT|LOG)$")
    protocol: Optional[str] = None
    description: Optional[str] = None


class SignatureResponse(BaseModel):
    id: uuid.UUID
    name: str
    sid: str
    category: str
    severity: str
    pattern: str
    action: str
    protocol: Optional[str]
    description: Optional[str]
    is_active: bool
    match_count: int
    created_at: datetime

    model_config = {"from_attributes": True}


class IntrusionEventCreate(BaseModel):
    signature_id: Optional[str] = None
    source_ip: str
    destination_ip: str
    protocol: Optional[str] = None
    source_port: Optional[int] = None
    destination_port: Optional[int] = None
    payload_excerpt: Optional[str] = None
    severity: str = Field(..., pattern="^(LOW|MEDIUM|HIGH|CRITICAL)$")


class IntrusionEventResponse(BaseModel):
    id: uuid.UUID
    signature_id: Optional[str]
    source_ip: str
    destination_ip: str
    protocol: Optional[str]
    source_port: Optional[int]
    destination_port: Optional[int]
    payload_excerpt: Optional[str]
    severity: str
    status: str
    detected_at: datetime

    model_config = {"from_attributes": True}


class AnalyzeRequest(BaseModel):
    source_ip: str
    destination_ip: str
    payload: str
    protocol: Optional[str] = "TCP"


class AnalyzeResponse(BaseModel):
    source_ip: str
    threat_detected: bool
    matched_signatures: List[str]
    severity: Optional[str]
    recommended_action: str
