"""
WebSocket Live Agent Event Streaming Endpoint.
Streams real-time agent deliberations, Groq token emissions, and debate trees to the Admin Portal.
Supports '?since=<seq>' reconnection replay and automatic state hydration from MongoDB agent_events.
"""

import asyncio
import json
import logging
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from app.bus.eventbus import event_bus
from app.db.mongo import clean_mongo_doc

logger = logging.getLogger("pact.ws")
router = APIRouter(tags=["WebSocket"])


@router.websocket("/ws/agents")
async def websocket_agents_endpoint(
    websocket: WebSocket,
    since: int = Query(0, ge=0)
):
    """
    Primary WebSocket Stream for the Admin Command Portal.
    Broadcasts live agent reasoning events, debate trees, tool calls, and LLM tokens.
    """
    await websocket.accept()
    queue = event_bus.subscribe()

    try:
        # Immediately hydrate recent history to render latest agent decisions and state
        history = await event_bus.get_history(since_seq=since, limit=100)
        for event in history:
            clean_e = clean_mongo_doc(event)
            await websocket.send_text(json.dumps(clean_e, default=str))

        while True:
            event = await queue.get()
            clean_e = clean_mongo_doc(event)
            await websocket.send_text(json.dumps(clean_e, default=str))

    except (WebSocketDisconnect, asyncio.CancelledError):
        logger.debug("WebSocket client disconnected or connection closed.")
    except Exception as e:
        logger.warning("WebSocket stream exception: %s", str(e))
    finally:
        event_bus.unsubscribe(queue)
