import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from app.schemas.session import SessionCreate, SessionResponse, SessionActivityUpdate
from app.services.session_service import SessionService
from app.api.deps import get_current_user

router = APIRouter()
service = SessionService()


@router.post("/", response_model=SessionResponse, status_code=status.HTTP_201_CREATED)
async def create_session(payload: SessionCreate, current_user: dict = Depends(get_current_user)):
    return await service.create_session(payload)


@router.get("/", response_model=List[SessionResponse])
async def list_sessions(user_id: Optional[str] = Query(None), current_user: dict = Depends(get_current_user)):
    return await service.list_sessions(user_id=user_id)


@router.get("/{session_id}", response_model=SessionResponse)
async def get_session(session_id: uuid.UUID, current_user: dict = Depends(get_current_user)):
    s = await service.get_session(str(session_id))
    if not s:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
    return s


@router.put("/{session_id}/activity", response_model=SessionResponse)
async def update_activity(session_id: uuid.UUID, payload: SessionActivityUpdate, current_user: dict = Depends(get_current_user)):
    s = await service.update_activity(str(session_id), payload)
    if not s:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
    return s


@router.post("/{session_id}/revoke", response_model=SessionResponse)
async def revoke_session(session_id: uuid.UUID, current_user: dict = Depends(get_current_user)):
    s = await service.revoke(str(session_id))
    if not s:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
    return s


@router.post("/revoke-all/{user_id}")
async def revoke_all_user_sessions(user_id: str, current_user: dict = Depends(get_current_user)):
    count = await service.revoke_all(user_id)
    return {"user_id": user_id, "sessions_revoked": count}
