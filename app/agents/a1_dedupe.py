"""
Agent A1: Deduplication & Anti-Flood Fraud Detection (Deterministic Python).
Enforces unique sequence constraints across (uid, seq) and detects suspicious rapid-fire flooding.
"""

import time
import hashlib
from typing import Dict, Any, Tuple
from app.db.mongo import get_collection
from app.bus.eventbus import event_bus

# Rolling window memory to detect suspicious spam attacks / flood requests
RECENT_SEND_TIMESTAMPS: Dict[str, list] = {}


class DedupeAgent:
    name = "A1_Dedupe"

    async def check_and_record(self, intake_data: Dict[str, Any], run_id: str) -> Tuple[bool, str]:
        """
        Returns (is_suppressed_or_denied, reason_key).
        Detects exact duplicates and rapid-fire spam flooding (>4 requests in 30s).
        """
        await event_bus.emit(
            "agent.entered",
            self.name,
            {"stage": "A1", "description": "Deduplication & Anti-Fraud Flood Detection"},
            run_id=run_id
        )

        uid = intake_data.get("uid") or intake_data.get("organization_id") or "UNKNOWN"
        seq = str(intake_data.get("seq", "000"))
        raw_sender = intake_data.get("sender") or uid
        from_hash = hashlib.sha256(raw_sender.encode()).hexdigest()[:8]

        now = time.time()
        dedupe_key = f"{from_hash}:{seq}"
        sms_col = get_collection("sms_messages")

        # 1. Anti-Flood Rate Limiting Check (Spam / Suspicious Hoarding)
        if raw_sender not in RECENT_SEND_TIMESTAMPS:
            RECENT_SEND_TIMESTAMPS[raw_sender] = []
        
        # Keep only timestamps from last 60 seconds
        RECENT_SEND_TIMESTAMPS[raw_sender] = [t for t in RECENT_SEND_TIMESTAMPS[raw_sender] if now - t < 60.0]
        RECENT_SEND_TIMESTAMPS[raw_sender].append(now)

        if len(RECENT_SEND_TIMESTAMPS[raw_sender]) > 6:
            await event_bus.emit(
                "agent.message",
                self.name,
                {
                    "status": "denied_suspicious_flood",
                    "sender": raw_sender,
                    "reason": f"Suspicious rapid-fire spam detected: {len(RECENT_SEND_TIMESTAMPS[raw_sender])} requests within 60s. Auto-denying dispatch."
                },
                run_id=run_id
            )
            return True, f"SUSPICIOUS_FLOOD_{from_hash}"

        # 2. Query exact (from_hash, seq) duplicate in database
        existing = await sms_col.find_one({"from_hash": from_hash, "seq": seq})
        if existing is not None:
            await event_bus.emit(
                "agent.message",
                self.name,
                {"status": "duplicate_detected", "dedupe_key": dedupe_key, "action": "suppress_duplicate"},
                run_id=run_id
            )
            return True, dedupe_key

        # Record valid incoming message
        await sms_col.insert_one({
            "from_hash": from_hash,
            "sender": raw_sender,
            "seq": seq,
            "dedupe_key": dedupe_key,
            "run_id": run_id,
            "type": intake_data.get("type"),
            "created_at": now
        })

        await event_bus.emit(
            "agent.message",
            self.name,
            {"status": "unique_message_verified", "dedupe_key": dedupe_key},
            run_id=run_id
        )

        return False, dedupe_key


a1_dedupe = DedupeAgent()
