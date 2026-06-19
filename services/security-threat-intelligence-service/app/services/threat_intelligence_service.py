import uuid
from collections import Counter
from datetime import datetime
from typing import Optional, List, Dict, Any
from app.schemas.threat_intelligence import (FeedCreate, FeedResponse, ActorCreate, ActorResponse, TTPCreate, TTPResponse)


class ThreatIntelligenceService:
    def __init__(self):
        self._feeds: Dict[str, dict] = {}
        self._actors: Dict[str, dict] = {}
        self._ttps: Dict[str, dict] = {}
        self._seed()

    def _seed(self):
        feeds = [
            ("AlienVault OTX", "OSINT", 80, "Open threat exchange community feeds"),
            ("MISP Community", "OSINT", 75, "Malware Information Sharing Platform"),
        ]
        for name, ftype, conf, desc in feeds:
            fid = str(uuid.uuid4())
            self._feeds[fid] = {"id": uuid.UUID(fid), "name": name, "feed_type": ftype, "url": None,
                                 "description": desc, "confidence": conf, "is_active": True,
                                 "last_updated": datetime.utcnow(), "created_at": datetime.utcnow()}
        actors = [
            ("APT28", "Fancy Bear", "RU", "ESPIONAGE", "EXPERT"),
            ("Lazarus Group", "Hidden Cobra", "KP", "FINANCIAL", "ADVANCED"),
        ]
        for name, aliases, country, motiv, soph in actors:
            aid = str(uuid.uuid4())
            self._actors[aid] = {"id": uuid.UUID(aid), "name": name, "aliases": aliases,
                                  "origin_country": country, "motivation": motiv, "sophistication": soph,
                                  "description": None, "created_at": datetime.utcnow()}

    async def create_feed(self, payload: FeedCreate) -> FeedResponse:
        fid = str(uuid.uuid4())
        f = {"id": uuid.UUID(fid), "is_active": True, "last_updated": None,
             "created_at": datetime.utcnow(), **payload.model_dump()}
        self._feeds[fid] = f
        return FeedResponse(**f)

    async def list_feeds(self) -> List[FeedResponse]:
        return [FeedResponse(**f) for f in self._feeds.values() if f["is_active"]]

    async def create_actor(self, payload: ActorCreate) -> ActorResponse:
        aid = str(uuid.uuid4())
        a = {"id": uuid.UUID(aid), "created_at": datetime.utcnow(), **payload.model_dump()}
        self._actors[aid] = a
        return ActorResponse(**a)

    async def list_actors(self) -> List[ActorResponse]:
        return [ActorResponse(**a) for a in self._actors.values()]

    async def create_ttp(self, payload: TTPCreate) -> TTPResponse:
        tid = str(uuid.uuid4())
        t = {"id": uuid.UUID(tid), "created_at": datetime.utcnow(), **payload.model_dump()}
        self._ttps[tid] = t
        return TTPResponse(**t)

    async def list_ttps(self) -> List[TTPResponse]:
        return [TTPResponse(**t) for t in self._ttps.values()]

    async def get_summary(self) -> Dict[str, Any]:
        by_tactic = Counter(t["tactic"] for t in self._ttps.values())
        by_motivation = Counter(a["motivation"] for a in self._actors.values())
        return {"total_feeds": len(self._feeds), "active_feeds": sum(1 for f in self._feeds.values() if f["is_active"]),
                "total_actors": len(self._actors), "total_ttps": len(self._ttps),
                "ttps_by_tactic": dict(by_tactic), "actors_by_motivation": dict(by_motivation)}
