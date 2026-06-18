import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class HSMKey(Base):
    __tablename__ = "hsm_keys"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    label = Column(String(255), nullable=False)
    key_type = Column(String(50), nullable=False)  # RSA, ECDSA, AES, HMAC
    key_size = Column(Integer, nullable=False)
    status = Column(String(30), nullable=False, default="ACTIVE")  # ACTIVE, INACTIVE, DESTROYED
    slot_id = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    tenant_id = Column(String(255), nullable=True)
