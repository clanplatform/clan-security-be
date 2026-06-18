import uuid
import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from app.schemas.certificate import CertificateCreate, CertificateResponse, CertificateRenewRequest


class CertificateService:
    def __init__(self):
        self._certs: Dict[str, dict] = {}

    async def create_certificate(self, payload: CertificateCreate) -> CertificateResponse:
        cid = str(uuid.uuid4())
        now = datetime.utcnow()
        fingerprint = hashlib.sha256(f"{payload.domain}{secrets.token_hex(8)}".encode()).hexdigest()
        cert = {
            "id": uuid.UUID(cid),
            "name": payload.name,
            "domain": payload.domain,
            "cert_type": payload.cert_type,
            "status": "PENDING",
            "issuer": "Let's Encrypt Authority X3",
            "subject": f"CN={payload.domain}",
            "fingerprint": fingerprint,
            "serial_number": secrets.token_hex(16).upper(),
            "key_algorithm": payload.key_algorithm,
            "key_size": payload.key_size,
            "valid_from": now,
            "valid_to": now + timedelta(days=365),
            "auto_renew": str(payload.auto_renew).lower(),
            "san_domains": ",".join(payload.san_domains) if payload.san_domains else None,
            "created_at": now,
            "updated_at": now,
            "tenant_id": payload.tenant_id,
        }
        self._certs[cid] = cert
        return CertificateResponse(**cert)

    async def get_certificate(self, cid: str) -> Optional[CertificateResponse]:
        c = self._certs.get(cid)
        return CertificateResponse(**c) if c else None

    async def list_certificates(
        self, cert_type: Optional[str] = None,
        status_filter: Optional[str] = None,
        expiring_soon: bool = False,
    ) -> List[CertificateResponse]:
        items = list(self._certs.values())
        if cert_type:
            items = [c for c in items if c["cert_type"] == cert_type]
        if status_filter:
            items = [c for c in items if c["status"] == status_filter]
        if expiring_soon:
            threshold = datetime.utcnow() + timedelta(days=30)
            items = [c for c in items if c["valid_to"] and c["valid_to"] <= threshold]
        return [CertificateResponse(**c) for c in items]

    async def renew_certificate(self, cid: str, payload: CertificateRenewRequest) -> Optional[CertificateResponse]:
        cert = self._certs.get(cid)
        if not cert:
            return None
        now = datetime.utcnow()
        cert["valid_from"] = now
        cert["valid_to"] = now + timedelta(days=payload.validity_days)
        cert["status"] = "ACTIVE"
        cert["updated_at"] = now
        cert["fingerprint"] = hashlib.sha256(f"{cert['domain']}{secrets.token_hex(8)}".encode()).hexdigest()
        return CertificateResponse(**cert)

    async def revoke_certificate(self, cid: str) -> Optional[CertificateResponse]:
        cert = self._certs.get(cid)
        if not cert:
            return None
        cert["status"] = "REVOKED"
        cert["updated_at"] = datetime.utcnow()
        return CertificateResponse(**cert)

    async def get_expiring(self, days: int) -> Dict[str, Any]:
        threshold = datetime.utcnow() + timedelta(days=days)
        expiring = [c for c in self._certs.values() if c["valid_to"] and c["valid_to"] <= threshold and c["status"] == "ACTIVE"]
        return {"expiring_in_days": days, "count": len(expiring),
                "certificates": [{"id": str(c["id"]), "domain": c["domain"], "valid_to": c["valid_to"].isoformat()} for c in expiring]}
