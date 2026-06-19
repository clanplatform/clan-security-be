import uuid
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class FeedCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    feed_type: str = Field(..., pattern="^(OSINT|COMMERCIAL|ISAC|GOVERNMENT|INTERNAL)$")
    url: Optional[str] = None
    description: Optional[str] = None
    confidence: int = Field(default=50, ge=0, le=100)


class FeedResponse(BaseModel):
    id: uuid.UUID
    name: str
    feed_type: str
    url: Optional[str]
    description: Optional[str]
    confidence: int
    is_active: bool
    last_updated: Optional[datetime]
    created_at: datetime

    model_config = {"from_attributes": True}


class ActorCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    aliases: Optional[str] = None
    origin_country: Optional[str] = None
    motivation: str = Field(..., pattern="^(FINANCIAL|ESPIONAGE|HACKTIVISM|SABOTAGE|UNKNOWN)$")
    sophistication: str = Field(..., pattern="^(MINIMAL|INTERMEDIATE|ADVANCED|EXPERT)$")
    description: Optional[str] = None


class ActorResponse(BaseModel):
    id: uuid.UUID
    name: str
    aliases: Optional[str]
    origin_country: Optional[str]
    motivation: str
    sophistication: str
    description: Optional[str]
    created_at: datetime

    model_config = {"from_attributes": True}


class TTPCreate(BaseModel):
    mitre_id: str = Field(..., pattern=r"^T\d{4}(\.\d{3})?$", description="MITRE ATT&CK ID e.g. T1059 or T1059.001")
    name: str
    tactic: str = Field(..., pattern="^(RECONNAISSANCE|RESOURCE_DEV|INITIAL_ACCESS|EXECUTION|PERSISTENCE|PRIV_ESC|DEFENSE_EVASION|CREDENTIAL_ACCESS|DISCOVERY|LATERAL_MOVEMENT|COLLECTION|C2|EXFILTRATION|IMPACT)$")
    description: Optional[str] = None
    actor_id: Optional[str] = None


class TTPResponse(BaseModel):
    id: uuid.UUID
    mitre_id: str
    name: str
    tactic: str
    description: Optional[str]
    actor_id: Optional[str]
    created_at: datetime

    model_config = {"from_attributes": True}
