import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class CryptoKeyCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    algorithm: str = Field(..., pattern="^(AES-128|AES-256|RSA-2048|RSA-4096|ECDSA-P256|ECDSA-P384|HMAC-SHA256|ChaCha20)$")
    key_size: int = Field(default=256)
    purpose: str = Field(..., pattern="^(ENCRYPT|SIGN|AUTHENTICATE|WRAP)$")
    description: Optional[str] = None
    rotation_period_days: int = Field(default=90, ge=1, le=730)
    tenant_id: Optional[str] = None


class CryptoKeyResponse(BaseModel):
    id: uuid.UUID
    name: str
    algorithm: str
    key_size: int
    purpose: str
    status: str
    version: int
    description: Optional[str]
    rotation_period_days: Optional[int]
    last_rotated_at: Optional[datetime]
    expires_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    tenant_id: Optional[str]

    model_config = {"from_attributes": True}


class KeyRotateResponse(BaseModel):
    old_key_id: str
    new_key_id: str
    algorithm: str
    new_version: int
    rotated_at: datetime
