import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.threat_intelligence import (FeedCreate, FeedResponse, ActorCreate, ActorResponse, TTPCreate, TTPResponse)
from app.services.threat_intelligence_service import ThreatIntelligenceService
from app.api.deps import get_current_user

router = APIRouter()
service = ThreatIntelligenceService()


@router.post("/feeds", response_model=FeedResponse, status_code=status.HTTP_201_CREATED)
async def create_feed(payload: FeedCreate, current_user: dict = Depends(get_current_user)):
    return await service.create_feed(payload)


@router.get("/feeds", response_model=List[FeedResponse])
async def list_feeds(current_user: dict = Depends(get_current_user)):
    return await service.list_feeds()


@router.post("/actors", response_model=ActorResponse, status_code=status.HTTP_201_CREATED)
async def create_actor(payload: ActorCreate, current_user: dict = Depends(get_current_user)):
    return await service.create_actor(payload)


@router.get("/actors", response_model=List[ActorResponse])
async def list_actors(current_user: dict = Depends(get_current_user)):
    return await service.list_actors()


@router.post("/ttps", response_model=TTPResponse, status_code=status.HTTP_201_CREATED)
async def create_ttp(payload: TTPCreate, current_user: dict = Depends(get_current_user)):
    return await service.create_ttp(payload)


@router.get("/ttps", response_model=List[TTPResponse])
async def list_ttps(current_user: dict = Depends(get_current_user)):
    return await service.list_ttps()


@router.get("/summary")
async def summary(current_user: dict = Depends(get_current_user)):
    return await service.get_summary()
