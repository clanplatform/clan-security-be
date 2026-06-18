import uuid
import hashlib
import secrets
import base64
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from app.core.config import settings
from app.schemas.identity import (VerificationCreate, VerificationResponse, OTPRequest,
                                   OTPVerifyRequest, OTPVerifyResponse, MFASetupResponse)


class IdentityVerificationService:
    def __init__(self):
        self._verifications: Dict[str, dict] = {}
        self._otps: Dict[str, dict] = {}  # user_id -> {otp_hash, expires_at, used}

    async def create_verification(self, payload: VerificationCreate) -> VerificationResponse:
        vid = str(uuid.uuid4())
        now = datetime.utcnow()
        v = {"id": uuid.UUID(vid), "user_id": payload.user_id, "verification_type": payload.verification_type,
             "status": "PENDING", "provider": payload.provider, "verified_at": None,
             "created_at": now, "expires_at": now + timedelta(hours=24)}
        self._verifications[vid] = v
        return VerificationResponse(**v)

    async def get_verification(self, vid: str) -> Optional[VerificationResponse]:
        v = self._verifications.get(vid)
        return VerificationResponse(**v) if v else None

    async def list_verifications(self) -> List[VerificationResponse]:
        return [VerificationResponse(**v) for v in self._verifications.values()]

    async def send_otp(self, payload: OTPRequest) -> Dict[str, Any]:
        otp_code = str(secrets.randbelow(900000) + 100000)
        otp_hash = hashlib.sha256(otp_code.encode()).hexdigest()
        expires_at = datetime.utcnow() + timedelta(minutes=settings.OTP_EXPIRY_MINUTES)
        self._otps[payload.user_id] = {"otp_hash": otp_hash, "expires_at": expires_at,
                                        "used": False, "channel": payload.channel}
        return {"user_id": payload.user_id, "channel": payload.channel,
                "message": f"OTP sent to {payload.destination}",
                "expires_in_minutes": settings.OTP_EXPIRY_MINUTES,
                "_dev_otp": otp_code if settings.ENVIRONMENT == "development" else None}

    async def verify_otp(self, payload: OTPVerifyRequest) -> OTPVerifyResponse:
        record = self._otps.get(payload.user_id)
        if not record:
            return OTPVerifyResponse(user_id=payload.user_id, valid=False, message="No OTP found for user")
        if record["used"]:
            return OTPVerifyResponse(user_id=payload.user_id, valid=False, message="OTP already used")
        if datetime.utcnow() > record["expires_at"]:
            return OTPVerifyResponse(user_id=payload.user_id, valid=False, message="OTP expired")
        provided_hash = hashlib.sha256(payload.otp_code.encode()).hexdigest()
        if not secrets.compare_digest(provided_hash, record["otp_hash"]):
            return OTPVerifyResponse(user_id=payload.user_id, valid=False, message="Invalid OTP")
        record["used"] = True
        return OTPVerifyResponse(user_id=payload.user_id, valid=True, message="OTP verified successfully")

    async def setup_mfa(self, user_id: str) -> MFASetupResponse:
        secret = base64.b32encode(secrets.token_bytes(20)).decode()
        qr_uri = f"otpauth://totp/{settings.MFA_ISSUER}:{user_id}?secret={secret}&issuer={settings.MFA_ISSUER}"
        backup_codes = [secrets.token_hex(5).upper() for _ in range(8)]
        return MFASetupResponse(user_id=user_id, secret=secret, qr_uri=qr_uri, backup_codes=backup_codes)
