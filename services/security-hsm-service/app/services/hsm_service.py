import uuid
import base64
import hmac
import hashlib
from datetime import datetime
from typing import Optional, List, Dict, Any
from app.schemas.hsm import HSMKeyGenRequest, HSMKeyResponse, HSMSignRequest, HSMSignResponse, HSMVerifyRequest, HSMVerifyResponse


class HSMService:
    def __init__(self):
        self._keys: Dict[str, dict] = {}
        self._secrets: Dict[str, bytes] = {}

    async def get_status(self) -> Dict[str, Any]:
        active = sum(1 for k in self._keys.values() if k["status"] == "ACTIVE")
        return {"status": "operational", "slot_count": 1, "active_keys": active,
                "total_keys": len(self._keys), "firmware_version": "1.4.2", "fips_compliant": True}

    async def generate_key(self, payload: HSMKeyGenRequest) -> HSMKeyResponse:
        kid = str(uuid.uuid4())
        secret = hashlib.sha256(f"{payload.label}{kid}".encode()).digest()
        self._secrets[kid] = secret
        key = {"id": uuid.UUID(kid), "label": payload.label, "key_type": payload.key_type,
                "key_size": payload.key_size, "status": "ACTIVE", "slot_id": 0,
                "created_at": datetime.utcnow(), "tenant_id": payload.tenant_id}
        self._keys[kid] = key
        return HSMKeyResponse(**key)

    async def get_key(self, kid: str) -> Optional[HSMKeyResponse]:
        k = self._keys.get(kid)
        return HSMKeyResponse(**k) if k else None

    async def list_keys(self) -> List[HSMKeyResponse]:
        return [HSMKeyResponse(**k) for k in self._keys.values() if k["status"] != "DESTROYED"]

    async def sign(self, payload: HSMSignRequest) -> HSMSignResponse:
        secret = self._secrets.get(payload.key_id)
        if not secret:
            from fastapi import HTTPException, status
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Key not found")
        data_bytes = base64.b64decode(payload.data) if self._is_b64(payload.data) else payload.data.encode()
        sig = hmac.new(secret, data_bytes, hashlib.sha256).digest()
        return HSMSignResponse(key_id=payload.key_id, signature=base64.b64encode(sig).decode(), algorithm=payload.algorithm)

    async def verify(self, payload: HSMVerifyRequest) -> HSMVerifyResponse:
        secret = self._secrets.get(payload.key_id)
        if not secret:
            from fastapi import HTTPException, status
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Key not found")
        data_bytes = base64.b64decode(payload.data) if self._is_b64(payload.data) else payload.data.encode()
        expected_sig = hmac.new(secret, data_bytes, hashlib.sha256).digest()
        try:
            provided_sig = base64.b64decode(payload.signature)
        except Exception:
            provided_sig = payload.signature.encode()
        valid = hmac.compare_digest(expected_sig, provided_sig)
        return HSMVerifyResponse(key_id=payload.key_id, valid=valid, algorithm=payload.algorithm)

    async def delete_key(self, kid: str) -> bool:
        if kid not in self._keys:
            return False
        self._keys[kid]["status"] = "DESTROYED"
        return True

    @staticmethod
    def _is_b64(s: str) -> bool:
        try:
            base64.b64decode(s)
            return True
        except Exception:
            return False
