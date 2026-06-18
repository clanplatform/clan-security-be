import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.classification import (
    ClassificationLabelCreate, ClassificationLabelResponse,
    ClassificationRuleCreate, ClassificationRuleResponse, ClassifyRequest,
)
from app.services.classification_service import ClassificationService
from app.api.deps import get_current_user

router = APIRouter()
service = ClassificationService()


@router.post("/labels", response_model=ClassificationLabelResponse, status_code=status.HTTP_201_CREATED)
async def create_label(payload: ClassificationLabelCreate, current_user: dict = Depends(get_current_user)):
    return await service.create_label(payload)


@router.get("/labels", response_model=List[ClassificationLabelResponse])
async def list_labels(current_user: dict = Depends(get_current_user)):
    return await service.list_labels()


@router.post("/rules", response_model=ClassificationRuleResponse, status_code=status.HTTP_201_CREATED)
async def create_rule(payload: ClassificationRuleCreate, current_user: dict = Depends(get_current_user)):
    return await service.create_rule(payload)


@router.get("/rules", response_model=List[ClassificationRuleResponse])
async def list_rules(current_user: dict = Depends(get_current_user)):
    return await service.list_rules()


@router.post("/classify")
async def classify_data(payload: ClassifyRequest, current_user: dict = Depends(get_current_user)):
    return await service.classify(payload)
