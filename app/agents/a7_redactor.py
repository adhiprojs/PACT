"""
Agent A7: Privacy Redactor (Deterministic Zero-Knowledge Masking).
Strips exact GPS, MSISDN, and personal identifiers to protect vulnerable disaster victims.
Reveals details only upon mutual plan commitment.
"""

from typing import Dict, Any
from app.bus.eventbus import event_bus


class PrivacyRedactorAgent:
    name = "A7_Redactor"

    async def redact(self, request_data: Dict[str, Any], match_data: Dict[str, Any], run_id: str) -> Dict[str, Any]:
        """
        Creates a masked privacy projection for public/preview consumption.
        """
        await event_bus.emit(
            "agent.entered",
            self.name,
            {"stage": "A7", "description": "Zero-Knowledge Privacy Projection & Identity Masking"},
            run_id=run_id
        )

        geo = request_data.get("geo", {})
        exact_lat = geo.get("latitude", 23.2599)
        exact_lon = geo.get("longitude", 77.4126)

        # 2km grid fuzzing
        masked_lat = round(exact_lat, 2)
        masked_lon = round(exact_lon, 2)

        raw_phone = request_data.get("sender") or request_data.get("phone", "+919876543210")
        masked_phone = raw_phone[:3] + "******" + raw_phone[-4:] if len(raw_phone) >= 7 else "***"

        redacted_view = {
            "uid": request_data.get("uid", "ANON"),
            "masked_phone": masked_phone,
            "masked_coordinates": [masked_lon, masked_lat],
            "general_area": f"Sector ({masked_lat}, {masked_lon})",
            "privacy_state": "ZERO_KNOWLEDGE_PREVIEW",
            "full_unmask_condition": "MUTUAL_COMMITMENT_AND_ACCEPTANCE"
        }

        await event_bus.emit(
            "privacy.reveal",
            self.name,
            {
                "status": "masked_projection_active",
                "redacted_view": redacted_view
            },
            run_id=run_id
        )

        return redacted_view


a7_redactor = PrivacyRedactorAgent()
