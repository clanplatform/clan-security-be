import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Boolean, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class MaskingConfig(Base):
    __tablename__ = "masking_configs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False, unique=True)
    field_type = Column(String(100), nullable=False)  # EMAIL, PHONE, CC_NUMBER, SSN, NAME, ADDRESS, CUSTOM
    mask_type = Column(String(50), nullable=False)    # REDACT, PARTIAL, TOKENIZE, HASH
    pattern = Column(Text, nullable=True)
    replacement = Column(String(255), nullable=True, default="***")
    preserve_length = Column(Boolean, default=False)
    preserve_format = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class MaskingToken(Base):
    __tablename__ = "masking_tokens"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    token = Column(String(255), nullable=False, unique=True, index=True)
    encrypted_value = Column(Text, nullable=False)
    field_type = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)
