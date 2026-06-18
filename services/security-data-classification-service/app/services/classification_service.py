import uuid
import re
from datetime import datetime
from typing import List, Dict, Any
from app.schemas.classification import (
    ClassificationLabelCreate, ClassificationLabelResponse,
    ClassificationRuleCreate, ClassificationRuleResponse, ClassifyRequest,
)


class ClassificationService:
    def __init__(self):
        self._labels: Dict[str, dict] = {}
        self._rules: Dict[str, dict] = {}
        self._seed_labels()

    def _seed_labels(self):
        defaults = [
            ("Public", 1, "#28a745", "Publicly available information"),
            ("Internal", 2, "#17a2b8", "For internal use only"),
            ("Confidential", 3, "#ffc107", "Confidential business information"),
            ("Restricted", 4, "#dc3545", "Highly sensitive data"),
            ("Top Secret", 5, "#6f42c1", "Highest sensitivity classification"),
        ]
        for name, level, color, desc in defaults:
            lid = str(uuid.uuid4())
            self._labels[lid] = {"id": uuid.UUID(lid), "name": name, "level": level,
                                  "color": color, "description": desc,
                                  "handling_requirements": None, "is_active": True,
                                  "created_at": datetime.utcnow()}

    async def create_label(self, payload: ClassificationLabelCreate) -> ClassificationLabelResponse:
        lid = str(uuid.uuid4())
        label = {"id": uuid.UUID(lid), "is_active": True, "created_at": datetime.utcnow(), **payload.model_dump()}
        self._labels[lid] = label
        return ClassificationLabelResponse(**label)

    async def list_labels(self) -> List[ClassificationLabelResponse]:
        items = sorted(self._labels.values(), key=lambda l: l["level"])
        return [ClassificationLabelResponse(**l) for l in items if l["is_active"]]

    async def create_rule(self, payload: ClassificationRuleCreate) -> ClassificationRuleResponse:
        rid = str(uuid.uuid4())
        rule = {"id": uuid.UUID(rid), "is_active": True, "created_at": datetime.utcnow(), **payload.model_dump()}
        self._rules[rid] = rule
        return ClassificationRuleResponse(**rule)

    async def list_rules(self) -> List[ClassificationRuleResponse]:
        return [ClassificationRuleResponse(**r) for r in self._rules.values() if r["is_active"]]

    async def classify(self, payload: ClassifyRequest) -> Dict[str, Any]:
        matches = []
        content_lower = payload.content.lower()
        for rule in self._rules.values():
            if not rule["is_active"]:
                continue
            try:
                if rule["rule_type"] == "REGEX":
                    matched = bool(re.search(rule["pattern"], payload.content))
                else:
                    matched = rule["pattern"].lower() in content_lower
                if matched:
                    label = self._labels.get(str(rule["label_id"]))
                    if label:
                        matches.append({"rule": rule["name"], "label": label["name"],
                                        "level": label["level"], "confidence": rule["confidence_threshold"]})
            except re.error:
                pass
        highest = max(matches, key=lambda m: m["level"]) if matches else None
        return {
            "classification": highest["label"] if highest else "Public",
            "level": highest["level"] if highest else 1,
            "confidence": highest["confidence"] if highest else 100,
            "matched_rules": len(matches),
        }
