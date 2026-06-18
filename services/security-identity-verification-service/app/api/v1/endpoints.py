import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.identity import (VerificationCreate, VerificationResponse, OTPRequest,
                                   OTPVerifyRequest, OTPVerifyResponse, MFASetupResponse)
from app.services.identity_service import IdentityVerificationService
from app.api.deps import get_current_user

router = APIRouter()
service = IdentityVerificationService()


@router.post("/verifications", response_model=VerificationResponse, status_code=status.HTTP_201_CREATED)
async def create_verification(payload: VerificationCreate, current_user: dict = Depends(get_current_user)):
    return await service.create_verification(payload)


@router.get("/verifications", response_model=List[VerificationResponse])
async def list_verifications(current_user: dict = Depends(get_current_user)):
    return await service.list_verifications()


@router.get("/verifications/{verification_id}", response_model=VerificationResponse)
async def get_verification(verification_id: uuid.UUID, current_user: dict = Depends(get_current_user)):
    v = await service.get_verification(str(verification_id))
    if not v:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Verification not found")
    return v


@router.post("/otp/send")
async def send_otp(payload: OTPRequest, current_user: dict = Depends(get_current_user)):
    return await service.send_otp(payload)


@router.post("/otp/verify", response_model=OTPVerifyResponse)
async def verify_otp(payload: OTPVerifyRequest, current_user: dict = Depends(get_current_user)):
    return await service.verify_otp(payload)


@router.post("/mfa/setup", response_model=MFASetupResponse)
async def setup_mfa(current_user: dict = Depends(get_current_user)):
    return await service.setup_mfa(current_user.get("sub", "unknown"))
