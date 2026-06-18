import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.backup import BackupKeyCreate, BackupKeyResponse, BackupJobCreate, BackupJobResponse, VerifyRequest
from app.services.backup_service import BackupService
from app.api.deps import get_current_user

router = APIRouter()
service = BackupService()


@router.post("/keys", response_model=BackupKeyResponse, status_code=status.HTTP_201_CREATED)
async def create_backup_key(payload: BackupKeyCreate, current_user: dict = Depends(get_current_user)):
    return await service.create_key(payload)


@router.get("/keys", response_model=List[BackupKeyResponse])
async def list_backup_keys(current_user: dict = Depends(get_current_user)):
    return await service.list_keys()


@router.get("/keys/{key_id}", response_model=BackupKeyResponse)
async def get_backup_key(key_id: uuid.UUID, current_user: dict = Depends(get_current_user)):
    key = await service.get_key(str(key_id))
    if not key:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Backup key not found")
    return key


@router.post("/keys/{key_id}/rotate", response_model=BackupKeyResponse)
async def rotate_backup_key(key_id: uuid.UUID, current_user: dict = Depends(get_current_user)):
    key = await service.rotate_key(str(key_id))
    if not key:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Backup key not found")
    return key


@router.post("/jobs", response_model=BackupJobResponse, status_code=status.HTTP_201_CREATED)
async def create_backup_job(payload: BackupJobCreate, current_user: dict = Depends(get_current_user)):
    return await service.create_job(payload)


@router.get("/jobs", response_model=List[BackupJobResponse])
async def list_backup_jobs(current_user: dict = Depends(get_current_user)):
    return await service.list_jobs()


@router.post("/verify", )
async def verify_backup(payload: VerifyRequest, current_user: dict = Depends(get_current_user)):
    return await service.verify_backup(payload)
