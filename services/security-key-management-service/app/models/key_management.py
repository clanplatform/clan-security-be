import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Integer, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class CryptoKey(Base):
    __tablename__ = "crypto_keys"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    algorithm = Column(String(50), nullable=False)
    key_size = Column(Integer, nullable=False, default=256)
    purpose = Column(String(100), nullable=False)  # ENCRYPT, SIGN, AUTHENTICATE, WRAP
    status = Column(String(30), nullable=False, default="ACTIVE")
    version = Column(Integer, nullable=False, default=1)
    key_material_hash = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    rotation_period_days = Column(Integer, nullable=True, default=90)
    last_rotated_at = Column(DateTime, nullable=True)
    expires_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    tenant_id = Column(String(255), nullable=True)
