import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class FirewallRuleCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    direction: str = Field(..., pattern="^(INBOUND|OUTBOUND|BOTH)$")
    action: str = Field(..., pattern="^(ALLOW|DENY|DROP|LOG)$")
    protocol: str = Field(..., pattern="^(TCP|UDP|ICMP|ANY)$")
    source_ip: Optional[str] = None
    source_port: Optional[str] = None
    destination_ip: Optional[str] = None
    destination_port: Optional[str] = None
    priority: int = Field(default=100, ge=1, le=65535)
    description: Optional[str] = None


class FirewallRuleResponse(BaseModel):
    id: uuid.UUID
    name: str
    direction: str
    action: str
    protocol: str
    source_ip: Optional[str]
    source_port: Optional[str]
    destination_ip: Optional[str]
    destination_port: Optional[str]
    priority: int
    description: Optional[str]
    is_active: bool
    hit_count: int
    created_at: datetime

    model_config = {"from_attributes": True}


class PacketCheckRequest(BaseModel):
    source_ip: str
    destination_ip: str
    protocol: str = Field(..., pattern="^(TCP|UDP|ICMP|ANY)$")
    source_port: Optional[int] = None
    destination_port: Optional[int] = None
    direction: str = Field(default="INBOUND", pattern="^(INBOUND|OUTBOUND)$")


class PacketCheckResponse(BaseModel):
    allowed: bool
    action: str
    matched_rule_id: Optional[str]
    matched_rule_name: Optional[str]
    reason: str
