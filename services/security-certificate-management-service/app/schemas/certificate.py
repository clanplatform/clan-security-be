import uuid
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class CertificateCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    domain: str = Field(..., min_length=1, max_length=255)
    cert_type: str = Field(..., pattern="^(DV|OV|EV|WILDCARD|SAN)$")
    key_algorithm: str = Field(default="RSA", pattern="^(RSA|ECDSA|ED25519)$")
    key_size: int = Field(default=2048)
    san_domains: Optional[List[str]] = None
    auto_renew: bool = True
    tenant_id: Optional[str] = None


class CertificateRenewRequest(BaseModel):
    validity_days: int = Field(default=365, ge=1, le=825)


class CertificateResponse(BaseModel):
    id: uuid.UUID
    name: str
    domain: str
    cert_type: str
    status: str
    issuer: Optional[str]
    subject: Optional[str]
    fingerprint: Optional[str]
    serial_number: Optional[str]
    key_algorithm: str
    key_size: int
    valid_from: Optional[datetime]
    valid_to: Optional[datetime]
    auto_renew: str
    san_domains: Optional[str]
    created_at: datetime
    updated_at: datetime
    tenant_id: Optional[str]

    model_config = {"from_attributes": True}
