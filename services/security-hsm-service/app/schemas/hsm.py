import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class HSMKeyGenRequest(BaseModel):
    label: str = Field(..., min_length=1, max_length=255)
    key_type: str = Field(..., pattern="^(RSA|ECDSA|AES|HMAC)$")
    key_size: int = Field(default=2048)
    tenant_id: Optional[str] = None


class HSMKeyResponse(BaseModel):
    id: uuid.UUID
    label: str
    key_type: str
    key_size: int
    status: str
    slot_id: int
    created_at: datetime
    tenant_id: Optional[str]

    model_config = {"from_attributes": True}


class HSMSignRequest(BaseModel):
    key_id: str
    data: str = Field(..., description="Base64-encoded data to sign")
    algorithm: str = Field(default="SHA256withRSA")


class HSMSignResponse(BaseModel):
    key_id: str
    signature: str
    algorithm: str


class HSMVerifyRequest(BaseModel):
    key_id: str
    data: str
    signature: str
    algorithm: str = Field(default="SHA256withRSA")


class HSMVerifyResponse(BaseModel):
    key_id: str
    valid: bool
    algorithm: str
