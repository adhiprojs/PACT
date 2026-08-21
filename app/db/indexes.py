"""
Database indexing utilities for PACT.
Ensures geospatial 2dsphere indexes and unique deduplication constraints.
"""

import logging
from app.db.mongo import get_collection

logger = logging.getLogger("pact.indexes")


async def ensure_indexes():
    """Initializes all necessary MongoDB indexes."""
    try:
        offers = get_collection("offers")
        await offers.create_index([("loc", "2dsphere")])
        await offers.create_index([("provider_id", 1)])
        await offers.create_index([("resource_bitfield", 1)])

        requests_col = get_collection("requests")
        await requests_col.create_index([("loc", "2dsphere")])
        await requests_col.create_index([("uid", 1), ("seq", 1)], unique=False)
        await requests_col.create_index([("created_at", -1)])

        sms_col = get_collection("sms_messages")
        await sms_col.create_index([("from_hash", 1), ("seq", 1)])

        events_col = get_collection("agent_events")
        await events_col.create_index([("created_at", 1)], expireAfterSeconds=86400)
        await events_col.create_index([("seq", 1)])
        await events_col.create_index([("run_id", 1)])

        matches_col = get_collection("matches")
        await matches_col.create_index([("match_id", 1)], unique=True)
        await matches_col.create_index([("status", 1)])

        locks_col = get_collection("locks")
        await locks_col.create_index([("created_at", 1)], expireAfterSeconds=60)

        logger.info("MongoDB geospatial and compound indexes configured successfully.")
    except Exception as e:
        logger.warning("Index creation notice: %s", str(e))
