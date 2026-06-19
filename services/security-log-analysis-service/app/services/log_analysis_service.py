import uuid
import time
from collections import Counter
from datetime import datetime
from typing import Optional, List, Dict, Any
from app.schemas.log_analysis import (LogEntryIngest, LogEntryResponse, LogQueryRequest,
                                       LogQueryResponse, LogAnomalyResponse)

ERROR_THRESHOLD = 10


class LogAnalysisService:
    def __init__(self):
        self._logs: Dict[str, dict] = {}
        self._anomalies: Dict[str, dict] = {}

    def _build_entry(self, payload: LogEntryIngest) -> dict:
        now = datetime.utcnow()
        lid = str(uuid.uuid4())
        return {"id": uuid.UUID(lid), "ingested_at": now,
                "timestamp": payload.timestamp or now, **payload.model_dump(exclude={"timestamp"})}

    def _detect_anomalies(self, entry: dict):
        if entry["log_level"] in ("ERROR", "CRITICAL"):
            source_errors = sum(1 for l in self._logs.values()
                                if l["source"] == entry["source"] and l["log_level"] in ("ERROR", "CRITICAL"))
            if source_errors >= ERROR_THRESHOLD:
                aid = str(uuid.uuid4())
                self._anomalies[aid] = {"id": uuid.UUID(aid), "source": entry["source"],
                                         "anomaly_type": "HIGH_ERROR_RATE", "severity": "HIGH",
                                         "description": f"Source '{entry['source']}' exceeded {ERROR_THRESHOLD} errors",
                                         "log_count": source_errors, "detected_at": datetime.utcnow()}

    async def ingest(self, payload: LogEntryIngest) -> LogEntryResponse:
        entry = self._build_entry(payload)
        self._logs[str(entry["id"])] = entry
        self._detect_anomalies(entry)
        return LogEntryResponse(**entry)

    async def ingest_batch(self, payloads: List[LogEntryIngest]) -> Dict[str, Any]:
        count = 0
        for p in payloads:
            entry = self._build_entry(p)
            self._logs[str(entry["id"])] = entry
            count += 1
        return {"ingested": count, "total_logs": len(self._logs)}

    async def query(self, payload: LogQueryRequest) -> LogQueryResponse:
        start = time.monotonic()
        items = list(self._logs.values())
        if payload.source:
            items = [l for l in items if l["source"] == payload.source]
        if payload.log_level:
            items = [l for l in items if l["log_level"] == payload.log_level]
        if payload.start_time:
            items = [l for l in items if l["timestamp"] >= payload.start_time]
        if payload.end_time:
            items = [l for l in items if l["timestamp"] <= payload.end_time]
        if payload.query:
            q = payload.query.lower()
            items = [l for l in items if q in l["message"].lower()]
        items.sort(key=lambda x: x["timestamp"], reverse=True)
        sliced = items[:payload.limit]
        elapsed = (time.monotonic() - start) * 1000
        return LogQueryResponse(total=len(items), entries=[LogEntryResponse(**l) for l in sliced], query_time_ms=elapsed)

    async def get_anomalies(self) -> List[LogAnomalyResponse]:
        return [LogAnomalyResponse(**a) for a in self._anomalies.values()]

    async def get_stats(self) -> Dict[str, Any]:
        by_level = Counter(l["log_level"] for l in self._logs.values())
        by_source = Counter(l["source"] for l in self._logs.values())
        return {"total_logs": len(self._logs), "anomalies": len(self._anomalies),
                "by_level": dict(by_level), "top_sources": dict(by_source.most_common(10))}
