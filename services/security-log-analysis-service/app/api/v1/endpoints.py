import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from app.schemas.log_analysis import LogEntryIngest, LogEntryResponse, LogQueryRequest, LogQueryResponse, LogAnomalyResponse
from app.services.log_analysis_service import LogAnalysisService
from app.api.deps import get_current_user

router = APIRouter()
service = LogAnalysisService()


@router.post("/ingest", response_model=LogEntryResponse, status_code=status.HTTP_201_CREATED)
async def ingest_log(payload: LogEntryIngest, current_user: dict = Depends(get_current_user)):
    return await service.ingest(payload)


@router.post("/ingest/batch", status_code=status.HTTP_201_CREATED)
async def ingest_batch(payload: List[LogEntryIngest], current_user: dict = Depends(get_current_user)):
    return await service.ingest_batch(payload)


@router.post("/query", response_model=LogQueryResponse)
async def query_logs(payload: LogQueryRequest, current_user: dict = Depends(get_current_user)):
    return await service.query(payload)


@router.get("/anomalies", response_model=List[LogAnomalyResponse])
async def get_anomalies(current_user: dict = Depends(get_current_user)):
    return await service.get_anomalies()


@router.get("/stats")
async def get_stats(current_user: dict = Depends(get_current_user)):
    return await service.get_stats()
