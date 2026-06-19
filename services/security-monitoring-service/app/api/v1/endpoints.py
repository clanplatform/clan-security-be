import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from app.schemas.monitoring import MetricCreate, MetricResponse, AlertCreate, AlertResponse, DashboardResponse
from app.services.monitoring_service import MonitoringService
from app.api.deps import get_current_user

router = APIRouter()
service = MonitoringService()


@router.post("/metrics", response_model=MetricResponse, status_code=status.HTTP_201_CREATED)
async def record_metric(payload: MetricCreate, current_user: dict = Depends(get_current_user)):
    return await service.record_metric(payload)


@router.get("/metrics", response_model=List[MetricResponse])
async def list_metrics(name: Optional[str] = Query(None), current_user: dict = Depends(get_current_user)):
    return await service.list_metrics(name=name)


@router.post("/alerts", response_model=AlertResponse, status_code=status.HTTP_201_CREATED)
async def create_alert(payload: AlertCreate, current_user: dict = Depends(get_current_user)):
    return await service.create_alert(payload)


@router.get("/alerts", response_model=List[AlertResponse])
async def list_alerts(active_only: bool = Query(True), current_user: dict = Depends(get_current_user)):
    return await service.list_alerts(active_only=active_only)


@router.post("/alerts/{alert_id}/acknowledge", response_model=AlertResponse)
async def acknowledge_alert(alert_id: uuid.UUID, current_user: dict = Depends(get_current_user)):
    a = await service.acknowledge_alert(str(alert_id), current_user)
    if not a:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Alert not found")
    return a


@router.get("/dashboard", response_model=DashboardResponse)
async def get_dashboard(current_user: dict = Depends(get_current_user)):
    return await service.get_dashboard()
