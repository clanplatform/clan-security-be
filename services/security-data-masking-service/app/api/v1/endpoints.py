import uuid
from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.masking import MaskingConfigCreate, MaskingConfigResponse, MaskRequest, MaskResponse, UnmaskRequest
from app.services.masking_service import MaskingService
from app.api.deps import get_current_user

router = APIRouter()
service = MaskingService()


@router.post("/configs", response_model=MaskingConfigResponse, status_code=status.HTTP_201_CREATED)
async def create_config(payload: MaskingConfigCreate, current_user: dict = Depends(get_current_user)):
    return await service.create_config(payload)


@router.get("/configs", response_model=List[MaskingConfigResponse])
async def list_configs(current_user: dict = Depends(get_current_user)):
    return await service.list_configs()


@router.get("/configs/{config_id}", response_model=MaskingConfigResponse)
async def get_config(config_id: uuid.UUID, current_user: dict = Depends(get_current_user)):
    cfg = await service.get_config(str(config_id))
    if not cfg:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Config not found")
    return cfg


@router.post("/mask", response_model=MaskResponse)
async def mask_data(payload: MaskRequest, current_user: dict = Depends(get_current_user)):
    return await service.mask(payload)


@router.post("/unmask", response_model=Dict[str, Any])
async def unmask_data(payload: UnmaskRequest, current_user: dict = Depends(get_current_user)):
    return await service.unmask(payload)
