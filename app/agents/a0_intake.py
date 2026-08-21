"""
Agent A0: Intake and Frame Verification (Deterministic Python).
Validates XOR checksum, parses wire format delimiters, and extracts metadata.
"""

from typing import Dict, Any, Tuple
from app.codec.canonical_codec import parse_sms
from app.codec.checksum import verify_checksum
from app.bus.eventbus import event_bus


class IntakeAgent:
    name = "A0_Intake"

    async def process(self, raw_input: str, run_id: str, transport: str = "http") -> Tuple[bool, Dict[str, Any], str]:
        """
        Validates and parses raw incoming wire frames.
        Returns (success, parsed_dict, error_message).
        """
        await event_bus.emit(
            "agent.entered",
            self.name,
            {"stage": "A0", "description": "Intake & Checksum Verification", "transport": transport},
            run_id=run_id
        )

        try:
            trimmed = raw_input.strip()
            if not trimmed:
                return False, {}, "EMPTY_PAYLOAD"

            parsed = parse_sms(trimmed)
            parsed["transport"] = transport

            # Checksum check
            if "checksum_valid" in parsed and not parsed["checksum_valid"]:
                await event_bus.emit(
                    "error",
                    self.name,
                    {"error_code": "BAD_CRC", "message": "XOR Checksum validation failed"},
                    run_id=run_id
                )
                return False, parsed, "INVALID_CHECKSUM"

            geo_info = parsed.get("geo") or {
                "latitude": 13.0827,
                "longitude": 80.2707,
                "coordinates": [80.2707, 13.0827]
            }

            await event_bus.emit(
                "agent.completed",
                self.name,
                {
                    "status": "intake_verified",
                    "type": parsed.get("type", "emergency_request"),
                    "seq": parsed.get("seq", "001"),
                    "uid": parsed.get("uid", "SOS01"),
                    "situation": parsed.get("payload", {}).get("situation", {}).get("name", "Flood Crisis"),
                    "geo": geo_info,
                    "checksum": parsed.get("checksum", "OK")
                },
                run_id=run_id
            )

            return True, parsed, ""

        except Exception as e:
            await event_bus.emit("error", self.name, {"error": str(e)}, run_id=run_id)
            return False, {}, str(e)


a0_intake = IntakeAgent()
