import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from app.schemas.network_monitoring import (DeviceCreate, DeviceResponse, FlowCreate, FlowResponse, NetworkStatsResponse)
from app.services.network_monitoring_service import NetworkMonitoringService
from app.api.deps import get_current_user

router = APIRouter()
service = NetworkMonitoringService()


@router.post("/devices", response_model=DeviceResponse, status_code=status.HTTP_201_CREATED)
async def register_device(payload: DeviceCreate, current_user: dict = Depends(get_current_user)):
    return await service.register_device(payload)


@router.get("/devices", response_model=List[DeviceResponse])
async def list_devices(current_user: dict = Depends(get_current_user)):
    return await service.list_devices()


@router.get("/devices/{device_id}", response_model=DeviceResponse)
async def get_device(device_id: uuid.UUID, current_user: dict = Depends(get_current_user)):
    d = await service.get_device(str(device_id))
    if not d:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Device not found")
    return d


@router.post("/flows", response_model=FlowResponse, status_code=status.HTTP_201_CREATED)
async def record_flow(payload: FlowCreate, current_user: dict = Depends(get_current_user)):
    return await service.record_flow(payload)


@router.get("/flows", response_model=List[FlowResponse])
async def list_flows(source_ip: Optional[str] = Query(None), current_user: dict = Depends(get_current_user)):
    return await service.list_flows(source_ip=source_ip)


@router.get("/stats", response_model=NetworkStatsResponse)
async def get_stats(current_user: dict = Depends(get_current_user)):
    return await service.get_stats()
