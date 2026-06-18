import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from app.schemas.key_management import CryptoKeyCreate, CryptoKeyResponse, KeyRotateResponse
from app.services.key_management_service import KeyManagementService
from app.api.deps import get_current_user

router = APIRouter()
service = KeyManagementService()


@router.post("/", response_model=CryptoKeyResponse, status_code=status.HTTP_201_CREATED)
async def create_key(payload: CryptoKeyCreate, current_user: dict = Depends(get_current_user)):
    return await service.create_key(payload)


@router.get("/", response_model=List[CryptoKeyResponse])
async def list_keys(
    purpose: Optional[str] = Query(None),
    status_filter: Optional[str] = Query(None, alias="status"),
    current_user: dict = Depends(get_current_user),
):
    return await service.list_keys(purpose=purpose, status_filter=status_filter)


@router.get("/{key_id}", response_model=CryptoKeyResponse)
async def get_key(key_id: uuid.UUID, current_user: dict = Depends(get_current_user)):
    key = await service.get_key(str(key_id))
    if not key:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Key not found")
    return key


@router.post("/{key_id}/rotate", response_model=KeyRotateResponse)
async def rotate_key(key_id: uuid.UUID, current_user: dict = Depends(get_current_user)):
    result = await service.rotate_key(str(key_id))
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Key not found")
    return result


@router.post("/{key_id}/activate", response_model=CryptoKeyResponse)
async def activate_key(key_id: uuid.UUID, current_user: dict = Depends(get_current_user)):
    key = await service.set_status(str(key_id), "ACTIVE")
    if not key:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Key not found")
    return key


@router.post("/{key_id}/expire", response_model=CryptoKeyResponse)
async def expire_key(key_id: uuid.UUID, current_user: dict = Depends(get_current_user)):
    key = await service.set_status(str(key_id), "EXPIRED")
    if not key:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Key not found")
    return key


@router.delete("/{key_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_key(key_id: uuid.UUID, current_user: dict = Depends(get_current_user)):
    deleted = await service.delete_key(str(key_id))
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Key not found")


@router.get("/summary/rotation-due")
async def get_rotation_due(current_user: dict = Depends(get_current_user)):
    return await service.get_rotation_due()
