"""
Agent A10: Verification & Digital Handshake (Deterministic Python).
Commits allocation to MongoDB, deducts provider stock to prevent double-booking,
and generates the canonical GSM-7 confirmation SMS frame.
"""

import time
import uuid
from typing import Dict, Any, List
from app.db.mongo import get_collection
from app.codec.checksum import calculate_xor_checksum
from app.bus.eventbus import event_bus


class VerificationAgent:
    name = "A10_Verification"

    async def commit_and_verify(
        self,
        request_data: Dict[str, Any],
        triage_info: Dict[str, Any],
        chosen_plan: Dict[str, Any],
        admin_action: Dict[str, Any],
        run_id: str
    ) -> Dict[str, Any]:
        await event_bus.emit(
            "agent.entered",
            self.name,
            {"stage": "A10", "description": "Database Allocation Commitment & Stock Update"},
            run_id=run_id
        )

        match_id = f"PLAN_{int(time.time()*1000)%100000:05d}"
        uid = request_data.get("uid", "CIT00")
        seq = str(request_data.get("seq", "001"))

        allocations = chosen_plan.get("allocations", [])
        offers_col = get_collection("offers")
        providers_col = get_collection("providers")
        matches_col = get_collection("matches")

        # Deduct inventory in MongoDB
        for alloc in allocations:
            p_id = alloc.get("provider_id")
            items = alloc.get("items", {})
            for res_key, qty in items.items():
                await offers_col.update_one(
                    {"provider_id": p_id},
                    {"$inc": {f"inventory.{res_key}": -qty}}
                )
                await providers_col.update_one(
                    {"provider_id": p_id},
                    {"$inc": {f"inventory.{res_key}": -qty}}
                )

        # Generate SMS Confirmation frame for Citizen: C|SEQ|UID|REF|STATE|ETA|CRC
        eta_int = int(round(chosen_plan.get("max_eta_hours", 2.0)))
        ack_body = f"C|{seq}|{uid}|{match_id}|OK|{eta_int}"
        ack_crc = calculate_xor_checksum(ack_body)
        full_ack_sms = f"{ack_body}|{ack_crc}"

        # Generate allocation frames for providers
        provider_sms_frames = []
        for alloc in allocations:
            p_id = alloc.get("provider_id")
            for res_key, qty in alloc.get("items", {}).items():
                p_body = f"A|{seq}|{match_id}|{p_id}|{res_key[:1].upper()}|{qty}|{uid}|{eta_int}"
                p_crc = calculate_xor_checksum(p_body)
                provider_sms_frames.append(f"{p_body}|{p_crc}")

        match_record = {
            "match_id": match_id,
            "run_id": run_id,
            "request_id": request_data.get("raw_frame") or uid,
            "uid": uid,
            "status": "committed",
            "selected_option_id": chosen_plan.get("option_id"),
            "allocations": allocations,
            "chosen_plan": chosen_plan,
            "triage_info": triage_info,
            "admin_action": admin_action,
            "sms_ack_frame": full_ack_sms,
            "provider_sms_frames": provider_sms_frames,
            "masked": True,
            "revealed": False,
            "created_at": time.time()
        }

        await matches_col.insert_one(match_record)

        await event_bus.emit(
            "decision.committed",
            self.name,
            {
                "match_id": match_id,
                "status": "committed",
                "allocations": allocations,
                "inventory_deducted": True
            },
            run_id=run_id
        )

        await event_bus.emit(
            "notify.sent",
            self.name,
            {
                "recipient": uid,
                "transport": "sms",
                "sms_frame": full_ack_sms,
                "message": f"Confirmation dispatched to victim: {full_ack_sms}"
            },
            run_id=run_id
        )

        await event_bus.emit(
            "verify.result",
            self.name,
            {
                "status": "verified_and_committed",
                "match_id": match_id,
                "ack_frame": full_ack_sms
            },
            run_id=run_id
        )

        return match_record


a10_verify = VerificationAgent()
