import uuid
from datetime import datetime
from typing import Optional, Dict
from pydantic import BaseModel, Field


class DeviceCreate(BaseModel):
    hostname: str = Field(..., min_length=1, max_length=255)
    ip_address: str = Field(..., min_length=7)
    device_type: str = Field(..., pattern="^(ROUTER|SWITCH|FIREWALL|SERVER|WORKSTATION|IOT|OTHER)$")
    os_type: Optional[str] = None
    location: Optional[str] = None
    tags: Optional[Dict[str, str]] = None


class DeviceResponse(BaseModel):
    id: uuid.UUID
    hostname: str
    ip_address: str
    device_type: str
    os_type: Optional[str]
    location: Optional[str]
    status: str
    tags: Optional[Dict[str, str]]
    last_seen: Optional[datetime]
    registered_at: datetime

    model_config = {"from_attributes": True}


class FlowCreate(BaseModel):
    source_ip: str
    destination_ip: str
    source_port: Optional[int] = None
    destination_port: Optional[int] = None
    protocol: str = Field(default="TCP", pattern="^(TCP|UDP|ICMP|OTHER)$")
    bytes_sent: int = Field(default=0, ge=0)
    bytes_received: int = Field(default=0, ge=0)
    packets: int = Field(default=1, ge=0)
    duration_ms: Optional[int] = None


class FlowResponse(BaseModel):
    id: uuid.UUID
    source_ip: str
    destination_ip: str
    source_port: Optional[int]
    destination_port: Optional[int]
    protocol: str
    bytes_sent: int
    bytes_received: int
    packets: int
    duration_ms: Optional[int]
    recorded_at: datetime

    model_config = {"from_attributes": True}


class NetworkStatsResponse(BaseModel):
    total_devices: int
    online_devices: int
    total_flows: int
    total_bytes_in: int
    total_bytes_out: int
    top_talkers: list
    generated_at: datetime
