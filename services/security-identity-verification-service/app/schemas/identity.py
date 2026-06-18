import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class VerificationCreate(BaseModel):
    user_id: str = Field(..., min_length=1)
    verification_type: str = Field(..., pattern="^(EMAIL|PHONE|DOCUMENT|BIOMETRIC|KYC)$")
    provider: Optional[str] = None


class VerificationResponse(BaseModel):
    id: uuid.UUID
    user_id: str
    verification_type: str
    status: str
    provider: Optional[str]
    verified_at: Optional[datetime]
    created_at: datetime
    expires_at: Optional[datetime]

    model_config = {"from_attributes": True}


class OTPRequest(BaseModel):
    user_id: str
    channel: str = Field(..., pattern="^(EMAIL|SMS)$")
    destination: str = Field(..., min_length=3)


class OTPVerifyRequest(BaseModel):
    user_id: str
    otp_code: str = Field(..., min_length=6, max_length=8)
    channel: str = Field(..., pattern="^(EMAIL|SMS)$")


class OTPVerifyResponse(BaseModel):
    user_id: str
    valid: bool
    message: str


class MFASetupResponse(BaseModel):
    user_id: str
    secret: str
    qr_uri: str
    backup_codes: list
