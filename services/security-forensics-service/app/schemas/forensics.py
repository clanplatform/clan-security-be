import uuid
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class CaseCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: str = Field(..., min_length=1)
    case_type: str = Field(..., pattern="^(DATA_BREACH|MALWARE|INSIDER_THREAT|FRAUD|UNAUTHORIZED_ACCESS|OTHER)$")
    severity: str = Field(..., pattern="^(LOW|MEDIUM|HIGH|CRITICAL)$")
    incident_id: Optional[str] = None


class CaseResponse(BaseModel):
    id: uuid.UUID
    case_number: str
    title: str
    description: str
    case_type: str
    severity: str
    status: str
    investigator_id: Optional[str]
    incident_id: Optional[str]
    created_at: datetime
    updated_at: datetime
    evidence_count: int = 0

    model_config = {"from_attributes": True}


class EvidenceCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    evidence_type: str = Field(..., pattern="^(LOG_FILE|DISK_IMAGE|MEMORY_DUMP|NETWORK_CAPTURE|SCREENSHOT|DOCUMENT|OTHER)$")
    description: Optional[str] = None
    hash_md5: Optional[str] = None
    hash_sha256: Optional[str] = None
    size_bytes: Optional[int] = None
    source_system: Optional[str] = None


class EvidenceResponse(BaseModel):
    id: uuid.UUID
    case_id: str
    name: str
    evidence_type: str
    description: Optional[str]
    hash_md5: Optional[str]
    hash_sha256: Optional[str]
    size_bytes: Optional[int]
    source_system: Optional[str]
    collected_by: Optional[str]
    collected_at: datetime

    model_config = {"from_attributes": True}


class ChainOfCustodyEntry(BaseModel):
    id: uuid.UUID
    case_id: str
    evidence_id: Optional[str]
    action: str
    actor_id: str
    notes: Optional[str]
    timestamp: datetime
