import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from app.schemas.pci import PCIControlCreate, PCIControlResponse, ComplianceCheckCreate, ComplianceCheckResponse
from app.services.pci_service import PCIService
from app.api.deps import get_current_user

controls_router = APIRouter()
checks_router = APIRouter()
service = PCIService()


@controls_router.post("/", response_model=PCIControlResponse, status_code=status.HTTP_201_CREATED)
async def create_control(payload: PCIControlCreate, current_user: dict = Depends(get_current_user)):
    return await service.create_control(payload)


@controls_router.get("/", response_model=List[PCIControlResponse])
async def list_controls(
    category: Optional[str] = Query(None),
    status_filter: Optional[str] = Query(None, alias="status"),
    current_user: dict = Depends(get_current_user),
):
    return await service.list_controls(category=category, status_filter=status_filter)


@controls_router.get("/{control_id}", response_model=PCIControlResponse)
async def get_control(control_id: uuid.UUID, current_user: dict = Depends(get_current_user)):
    ctrl = await service.get_control(str(control_id))
    if not ctrl:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Control not found")
    return ctrl


@controls_router.get("/summary/overview")
async def get_compliance_summary(current_user: dict = Depends(get_current_user)):
    return await service.get_summary()


@checks_router.post("/", response_model=ComplianceCheckResponse, status_code=status.HTTP_201_CREATED)
async def create_check(payload: ComplianceCheckCreate, current_user: dict = Depends(get_current_user)):
    return await service.create_check(payload)


@checks_router.get("/", response_model=List[ComplianceCheckResponse])
async def list_checks(
    control_id: Optional[str] = Query(None),
    result: Optional[str] = Query(None),
    current_user: dict = Depends(get_current_user),
):
    return await service.list_checks(control_id=control_id, result=result)
