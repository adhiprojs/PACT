"""
In-process asyncio Pub/Sub Event Bus for PACT.
Broadcasts multi-agent deliberations, Groq token streams, tool calls, and debate turns.
Persists events to MongoDB with sequence numbering and supports '?since=<seq>' replay.
"""

import asyncio
import time
import logging
from typing import Dict, Any, List, Set, Optional
from app.db.mongo import get_collection, clean_mongo_doc

logger = logging.getLogger("pact.eventbus")


class EventBus:
    _instance: Optional["EventBus"] = None

    def __init__(self):
        self._seq: int = 0
        self._subscribers: Set[asyncio.Queue] = set()
        self._lock = asyncio.Lock()

    @classmethod
    def get_instance(cls) -> "EventBus":
        if cls._instance is None:
            cls._instance = EventBus()
        return cls._instance

    async def emit(
        self,
        event_type: str,
        agent: str,
        payload: Dict[str, Any],
        run_id: str = "run_default",
        trace_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Emits an event to all connected subscribers and persists to agent_events.
        """
        async with self._lock:
            self._seq += 1
            current_seq = self._seq

        event = {
            "v": 1,
            "seq": current_seq,
            "ts": time.time(),
            "trace_id": trace_id or f"tr_{run_id}",
            "run_id": run_id,
            "agent": agent,
            "type": event_type,
            "payload": payload,
            "created_at": time.time()
        }

        # Persist a shallow copy to database so MongoDB mutation doesn't taint in-memory event
        try:
            events_col = get_collection("agent_events")
            await events_col.insert_one(dict(event))
        except Exception as e:
            logger.warning("Failed to persist event %s: %s", event_type, str(e))

        # Push clean sanitized event to all active in-memory subscriber queues
        clean_event = clean_mongo_doc(event)
        dead_subs = set()
        for q in list(self._subscribers):
            try:
                q.put_nowait(clean_event)
            except asyncio.QueueFull:
                dead_subs.add(q)
            except Exception:
                dead_subs.add(q)

        for d in dead_subs:
            self._subscribers.discard(d)

        return clean_event

    def subscribe(self) -> asyncio.Queue:
        """Registers a new WebSocket or internal subscriber queue."""
        q = asyncio.Queue(maxsize=1000)
        self._subscribers.add(q)
        return q

    def unsubscribe(self, q: asyncio.Queue):
        """Removes a subscriber queue."""
        self._subscribers.discard(q)

    async def get_history(self, since_seq: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Retrieves past events for client reconnect replay or initial page hydration."""
        events_col = get_collection("agent_events")
        if since_seq > 0:
            cursor = events_col.find({"seq": {"$gt": since_seq}}).sort("seq", 1).limit(limit)
            items = await cursor.to_list(limit)
        else:
            # Hydrate recent events for the latest run so dashboard loads complete state immediately
            latest_event = await events_col.find_one({}, sort=[("seq", -1)])
            if latest_event and latest_event.get("run_id"):
                latest_run_id = latest_event["run_id"]
                cursor = events_col.find({"run_id": latest_run_id}).sort("seq", 1).limit(limit)
                items = await cursor.to_list(limit)
            else:
                cursor = events_col.find({}).sort("seq", -1).limit(30)
                items = await cursor.to_list(30)
                items.reverse()
        return clean_mongo_doc(items)


event_bus = EventBus.get_instance()
