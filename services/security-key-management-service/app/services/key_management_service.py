import uuid
import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from app.core.config import settings
from app.schemas.key_management import CryptoKeyCreate, CryptoKeyResponse, KeyRotateResponse


class KeyManagementService:
    def __init__(self):
        self._keys: Dict[str, dict] = {}

    def _build_key(self, kid: str, payload: CryptoKeyCreate, version: int = 1) -> dict:
        now = datetime.utcnow()
        return {
            "id": uuid.UUID(kid),
            "name": payload.name,
            "algorithm": payload.algorithm,
            "key_size": payload.key_size,
            "purpose": payload.purpose,
            "status": "ACTIVE",
            "version": version,
            "key_material_hash": hashlib.sha256(secrets.token_bytes(32)).hexdigest(),
            "description": payload.description,
            "rotation_period_days": payload.rotation_period_days,
            "last_rotated_at": now,
            "expires_at": now + timedelta(days=payload.rotation_period_days),
            "created_at": now,
            "updated_at": now,
            "tenant_id": payload.tenant_id,
        }

    async def create_key(self, payload: CryptoKeyCreate) -> CryptoKeyResponse:
        kid = str(uuid.uuid4())
        key = self._build_key(kid, payload)
        self._keys[kid] = key
        return CryptoKeyResponse(**key)

    async def get_key(self, kid: str) -> Optional[CryptoKeyResponse]:
        k = self._keys.get(kid)
        return CryptoKeyResponse(**k) if k else None

    async def list_keys(self, purpose: Optional[str] = None, status_filter: Optional[str] = None) -> List[CryptoKeyResponse]:
        items = list(self._keys.values())
        if purpose:
            items = [k for k in items if k["purpose"] == purpose]
        if status_filter:
            items = [k for k in items if k["status"] == status_filter]
        return [CryptoKeyResponse(**k) for k in items]

    async def rotate_key(self, kid: str) -> Optional[KeyRotateResponse]:
        old = self._keys.get(kid)
        if not old:
            return None
        new_id = str(uuid.uuid4())
        now = datetime.utcnow()
        new_key = {**old, "id": uuid.UUID(new_id), "version": old["version"] + 1,
                   "key_material_hash": hashlib.sha256(secrets.token_bytes(32)).hexdigest(),
                   "last_rotated_at": now,
                   "expires_at": now + timedelta(days=old["rotation_period_days"] or 90),
                   "created_at": now, "updated_at": now}
        old["status"] = "INACTIVE"
        old["updated_at"] = now
        self._keys[new_id] = new_key
        return KeyRotateResponse(old_key_id=kid, new_key_id=new_id,
                                  algorithm=new_key["algorithm"],
                                  new_version=new_key["version"], rotated_at=now)

    async def set_status(self, kid: str, new_status: str) -> Optional[CryptoKeyResponse]:
        k = self._keys.get(kid)
        if not k:
            return None
        k["status"] = new_status
        k["updated_at"] = datetime.utcnow()
        return CryptoKeyResponse(**k)

    async def delete_key(self, kid: str) -> bool:
        if kid not in self._keys:
            return False
        self._keys[kid]["status"] = "DESTROYED"
        return True

    async def get_rotation_due(self) -> Dict[str, Any]:
        now = datetime.utcnow()
        threshold = now + timedelta(days=settings.KEY_ROTATION_DAYS)
        due = [k for k in self._keys.values()
               if k["status"] == "ACTIVE" and k["expires_at"] and k["expires_at"] <= threshold]
        return {"rotation_due_within_days": settings.KEY_ROTATION_DAYS,
                "count": len(due),
                "keys": [{"id": str(k["id"]), "name": k["name"], "expires_at": k["expires_at"].isoformat()} for k in due]}
