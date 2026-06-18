from typing import List
from fastapi import APIRouter, Depends, status
from app.schemas.encryption import EncryptRequest, EncryptResponse, DecryptRequest, DecryptResponse, GenerateKeyResponse
from app.services.encryption_service import EncryptionService
from app.api.deps import get_current_user

router = APIRouter()
service = EncryptionService()


@router.post("/encrypt", response_model=EncryptResponse)
async def encrypt(payload: EncryptRequest, current_user: dict = Depends(get_current_user)):
    return await service.encrypt(payload)


@router.post("/decrypt", response_model=DecryptResponse)
async def decrypt(payload: DecryptRequest, current_user: dict = Depends(get_current_user)):
    return await service.decrypt(payload)


@router.post("/generate-key", response_model=GenerateKeyResponse, status_code=status.HTTP_201_CREATED)
async def generate_key(algorithm: str = "AES-256", current_user: dict = Depends(get_current_user)):
    return await service.generate_key(algorithm)


@router.get("/algorithms")
async def list_algorithms(current_user: dict = Depends(get_current_user)):
    return {"algorithms": ["AES-128", "AES-256", "AES-256-GCM", "ChaCha20-Poly1305", "RSA-2048", "RSA-4096", "ECDSA-P256", "ECDSA-P384"]}
