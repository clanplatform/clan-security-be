from typing import Optional
from pydantic import BaseModel, Field


class EncryptRequest(BaseModel):
    plaintext: str = Field(..., min_length=1)
    key_id: Optional[str] = None
    algorithm: str = Field(default="AES-256-GCM")
    context: Optional[str] = None


class EncryptResponse(BaseModel):
    ciphertext: str
    key_id: str
    algorithm: str
    iv: Optional[str] = None


class DecryptRequest(BaseModel):
    ciphertext: str = Field(..., min_length=1)
    key_id: str
    algorithm: str = Field(default="AES-256-GCM")
    iv: Optional[str] = None


class DecryptResponse(BaseModel):
    plaintext: str
    key_id: str
    algorithm: str


class GenerateKeyResponse(BaseModel):
    key_id: str
    algorithm: str
    key_material: str
    key_size: int
