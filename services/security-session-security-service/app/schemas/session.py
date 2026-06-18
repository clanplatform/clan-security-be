import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class SessionCreate(BaseModel):
    user_id: str = Field(..., min_length=1)
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    device_fingerprint: Optional[str] = None
    geo_country: Optional[str] = None


class SessionResponse(BaseModel):
    id: uuid.UUID
    user_id: str
    ip_address: Optional[str]
    user_agent: Optional[str]
    status: str
    risk_score: int
    last_activity_at: Optional[datetime]
    created_at: datetime
    expires_at: datetime
    revoked_at: Optional[datetime]
    device_fingerprint: Optional[str]
    geo_country: Optional[str]

    model_config = {"from_attributes": True}


class SessionActivityUpdate(BaseModel):
    ip_address: Optional[str] = None
    geo_country: Optional[str] = None
