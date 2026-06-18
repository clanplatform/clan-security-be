import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.hsm import (HSMKeyGenRequest, HSMKeyResponse, HSMSignRequest, HSMSignResponse,
                               HSMVerifyRequest, HSMVerifyResponse)
from app.services.hsm_service import HSMService
from app.api.deps import get_current_user

router = APIRouter()
service = HSMService()


@router.get("/status")
async def get_status(current_user: dict = Depends(get_current_user)):
    return await service.get_status()


@router.post("/keys/generate", response_model=HSMKeyResponse, status_code=status.HTTP_201_CREATED)
async def generate_key(payload: HSMKeyGenRequest, current_user: dict = Depends(get_current_user)):
    return await service.generate_key(payload)


@router.get("/keys", response_model=List[HSMKeyResponse])
async def list_keys(current_user: dict = Depends(get_current_user)):
    return await service.list_keys()


@router.get("/keys/{key_id}", response_model=HSMKeyResponse)
async def get_key(key_id: uuid.UUID, current_user: dict = Depends(get_current_user)):
    key = await service.get_key(str(key_id))
    if not key:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Key not found")
    return key


@router.post("/sign", response_model=HSMSignResponse)
async def sign_data(payload: HSMSignRequest, current_user: dict = Depends(get_current_user)):
    return await service.sign(payload)


@router.post("/verify", response_model=HSMVerifyResponse)
async def verify_signature(payload: HSMVerifyRequest, current_user: dict = Depends(get_current_user)):
    return await service.verify(payload)


@router.delete("/keys/{key_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_key(key_id: uuid.UUID, current_user: dict = Depends(get_current_user)):
    deleted = await service.delete_key(str(key_id))
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Key not found")
