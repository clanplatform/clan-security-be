import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)


class EventPublisher:
    """In-process event publisher. Replace with Kafka/Redis Streams in production."""

    def __init__(self):
        self._handlers: Dict[str, list] = {}

    def subscribe(self, event_type: str, handler):
        self._handlers.setdefault(event_type, []).append(handler)

    async def publish(self, event_type: str, payload: Dict[str, Any], service: str = "unknown"):
        handlers = self._handlers.get(event_type, [])
        for handler in handlers:
            try:
                await handler(event_type, payload, service)
            except Exception as e:
                logger.error(f"Event handler error for {event_type}: {e}")


event_publisher = EventPublisher()
