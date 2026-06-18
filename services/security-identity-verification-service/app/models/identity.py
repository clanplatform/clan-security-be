import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class IdentityVerification(Base):
    __tablename__ = "identity_verifications"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(String(255), nullable=False, index=True)
    verification_type = Column(String(50), nullable=False)  # EMAIL, PHONE, DOCUMENT, BIOMETRIC, KYC
    status = Column(String(30), nullable=False, default="PENDING")
    provider = Column(String(100), nullable=True)
    verified_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)


class OTPRecord(Base):
    __tablename__ = "otp_records"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(String(255), nullable=False)
    otp_hash = Column(String(255), nullable=False)
    channel = Column(String(20), nullable=False)  # EMAIL, SMS
    is_used = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)
