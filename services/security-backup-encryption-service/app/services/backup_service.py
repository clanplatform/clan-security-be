import uuid
import secrets
from datetime import datetime
from typing import Optional, List, Dict
from app.schemas.backup import BackupKeyCreate, BackupKeyResponse, BackupJobCreate, BackupJobResponse, VerifyRequest


class BackupService:
    def __init__(self):
        self._keys: Dict[str, dict] = {}
        self._jobs: Dict[str, dict] = {}

    async def create_key(self, payload: BackupKeyCreate) -> BackupKeyResponse:
        kid = str(uuid.uuid4())
        key = {"id": uuid.UUID(kid), "key_version": 1, "status": "ACTIVE",
               "created_at": datetime.utcnow(), "rotated_at": None, **payload.model_dump()}
        self._keys[kid] = key
        return BackupKeyResponse(**key)

    async def get_key(self, key_id: str) -> Optional[BackupKeyResponse]:
        k = self._keys.get(key_id)
        return BackupKeyResponse(**k) if k else None

    async def list_keys(self) -> List[BackupKeyResponse]:
        return [BackupKeyResponse(**k) for k in self._keys.values() if k["status"] != "DELETED"]

    async def rotate_key(self, key_id: str) -> Optional[BackupKeyResponse]:
        key = self._keys.get(key_id)
        if not key:
            return None
        key["key_version"] += 1
        key["rotated_at"] = datetime.utcnow()
        return BackupKeyResponse(**key)

    async def create_job(self, payload: BackupJobCreate) -> BackupJobResponse:
        jid = str(uuid.uuid4())
        job = {"id": uuid.UUID(jid), "status": "SCHEDULED", "last_run": None,
               "next_run": None, "size_bytes": None, "checksum": None,
               "created_at": datetime.utcnow(), "is_verified": False, **payload.model_dump()}
        self._jobs[jid] = job
        return BackupJobResponse(**job)

    async def list_jobs(self) -> List[BackupJobResponse]:
        return [BackupJobResponse(**j) for j in self._jobs.values()]

    async def verify_backup(self, payload: VerifyRequest) -> dict:
        job = self._jobs.get(str(payload.job_id))
        if not job:
            return {"verified": False, "error": "Job not found"}
        expected = job.get("checksum")
        verified = expected is None or expected == payload.checksum
        if verified:
            job["is_verified"] = True
        return {"verified": verified, "job_id": str(payload.job_id),
                "timestamp": datetime.utcnow().isoformat()}
