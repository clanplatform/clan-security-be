import uuid
import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Optional, List, Dict
from app.core.config import settings
from app.schemas.session import SessionCreate, SessionResponse, SessionActivityUpdate


class SessionService:
    def __init__(self):
        self._sessions: Dict[str, dict] = {}

    def _calc_risk(self, session: dict, new_ip: Optional[str] = None, new_country: Optional[str] = None) -> int:
        risk = 0
        if new_ip and session.get("ip_address") and new_ip != session["ip_address"]:
            risk += 30
        if new_country and session.get("geo_country") and new_country != session["geo_country"]:
            risk += 50
        return min(risk, 100)

    async def create_session(self, payload: SessionCreate) -> SessionResponse:
        sid = str(uuid.uuid4())
        token = secrets.token_hex(32)
        token_hash = hashlib.sha256(token.encode()).hexdigest()
        now = datetime.utcnow()
        session = {"id": uuid.UUID(sid), "user_id": payload.user_id, "session_token_hash": token_hash,
                   "ip_address": payload.ip_address, "user_agent": payload.user_agent, "status": "ACTIVE",
                   "risk_score": 0, "last_activity_at": now, "created_at": now,
                   "expires_at": now + timedelta(minutes=settings.SESSION_TIMEOUT_MINUTES),
                   "revoked_at": None, "device_fingerprint": payload.device_fingerprint,
                   "geo_country": payload.geo_country}
        self._sessions[sid] = session
        return SessionResponse(**session)

    async def get_session(self, sid: str) -> Optional[SessionResponse]:
        s = self._sessions.get(sid)
        return SessionResponse(**s) if s else None

    async def list_sessions(self, user_id: Optional[str] = None) -> List[SessionResponse]:
        sessions = list(self._sessions.values())
        if user_id:
            sessions = [s for s in sessions if s["user_id"] == user_id]
        return [SessionResponse(**s) for s in sessions]

    async def update_activity(self, sid: str, payload: SessionActivityUpdate) -> Optional[SessionResponse]:
        s = self._sessions.get(sid)
        if not s:
            return None
        now = datetime.utcnow()
        risk = self._calc_risk(s, payload.ip_address, payload.geo_country)
        s["last_activity_at"] = now
        if payload.ip_address:
            s["ip_address"] = payload.ip_address
        if payload.geo_country:
            s["geo_country"] = payload.geo_country
        s["risk_score"] = risk
        if risk >= 50:
            s["status"] = "SUSPICIOUS"
        return SessionResponse(**s)

    async def revoke(self, sid: str) -> Optional[SessionResponse]:
        s = self._sessions.get(sid)
        if not s:
            return None
        s["status"] = "REVOKED"
        s["revoked_at"] = datetime.utcnow()
        return SessionResponse(**s)

    async def revoke_all(self, user_id: str) -> int:
        count = 0
        now = datetime.utcnow()
        for s in self._sessions.values():
            if s["user_id"] == user_id and s["status"] == "ACTIVE":
                s["status"] = "REVOKED"
                s["revoked_at"] = now
                count += 1
        return count
