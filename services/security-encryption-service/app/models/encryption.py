import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class EncryptionOperation(Base):
    __tablename__ = "encryption_operations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    operation = Column(String(20), nullable=False)  # ENCRYPT, DECRYPT
    algorithm = Column(String(50), nullable=False)
    key_id = Column(String(255), nullable=True)
    user_id = Column(String(255), nullable=True)
    status = Column(String(20), nullable=False, default="SUCCESS")
    created_at = Column(DateTime, default=datetime.utcnow)
