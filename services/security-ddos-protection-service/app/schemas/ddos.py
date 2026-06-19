import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class RateLimitRuleCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    target: str = Field(..., description="IP, CIDR, or endpoint path")
    requests_per_second: int = Field(..., ge=1)
    burst_size: int = Field(default=100, ge=1)
    action: str = Field(default="THROTTLE", pattern="^(THROTTLE|BLOCK|CHALLENGE)$")


class RateLimitRuleResponse(BaseModel):
    id: uuid.UUID
    name: str
    target: str
    requests_per_second: int
    burst_size: int
    action: str
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class BlockedIPCreate(BaseModel):
    ip_address: str = Field(..., min_length=7)
    reason: str = Field(..., min_length=1)
    block_type: str = Field(default="MANUAL", pattern="^(MANUAL|AUTO|GEOFENCE)$")
    expires_at: Optional[datetime] = None


class BlockedIPResponse(BaseModel):
    id: uuid.UUID
    ip_address: str
    reason: str
    block_type: str
    is_active: bool
    expires_at: Optional[datetime]
    created_at: datetime

    model_config = {"from_attributes": True}


class AttackEventCreate(BaseModel):
    attack_type: str = Field(..., pattern="^(VOLUMETRIC|PROTOCOL|APPLICATION|AMPLIFICATION|SLOWLORIS)$")
    source_ip: Optional[str] = None
    target: str
    peak_rps: int = Field(..., ge=0)
    duration_seconds: Optional[int] = None
    mitigated: bool = False


class AttackEventResponse(BaseModel):
    id: uuid.UUID
    attack_type: str
    source_ip: Optional[str]
    target: str
    peak_rps: int
    duration_seconds: Optional[int]
    mitigated: bool
    detected_at: datetime

    model_config = {"from_attributes": True}


class TrafficAnalysisRequest(BaseModel):
    source_ip: str
    requests_per_second: float
    bytes_per_second: Optional[float] = None
    destination: Optional[str] = None


class TrafficAnalysisResponse(BaseModel):
    source_ip: str
    is_suspicious: bool
    is_blocked: bool
    risk_score: int
    recommended_action: str
    reason: str
