import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class BackupKeyCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    algorithm: str = Field(default="AES-256-GCM")
    description: Optional[str] = None
    expires_at: Optional[datetime] = None
    tenant_id: Optional[str] = None


class BackupKeyResponse(BaseModel):
    id: uuid.UUID
    name: str
    algorithm: str
    key_version: int
    status: str
    description: Optional[str]
    expires_at: Optional[datetime]
    created_at: datetime
    rotated_at: Optional[datetime]
    tenant_id: Optional[str]

    model_config = {"from_attributes": True}


class BackupJobCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    key_id: uuid.UUID
    source: str = Field(..., min_length=1)
    destination: str = Field(..., min_length=1)
    schedule: Optional[str] = None


class BackupJobResponse(BaseModel):
    id: uuid.UUID
    name: str
    key_id: uuid.UUID
    source: str
    destination: str
    status: str
    schedule: Optional[str]
    last_run: Optional[datetime]
    next_run: Optional[datetime]
    size_bytes: Optional[int]
    checksum: Optional[str]
    created_at: datetime
    is_verified: bool

    model_config = {"from_attributes": True}


class VerifyRequest(BaseModel):
    job_id: uuid.UUID
    checksum: str
