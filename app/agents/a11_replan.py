"""
Agent A11: Replanner Trigger (Deterministic Python).
Handles route blockage, provider rejection, or field delivery failure.
Re-enters the reasoning pipeline at A3 Geo Matcher with updated candidate exclusions.
"""

from typing import Dict, Any, List
from app.bus.eventbus import event_bus


class ReplannerAgent:
    name = "A11_Replanner"

    async def trigger_replan(
        self,
        reason: str,
        failed_provider_ids: List[str],
        request_data: Dict[str, Any],
        run_id: str
    ) -> Dict[str, Any]:
        await event_bus.emit(
            "agent.entered",
            self.name,
            {"stage": "A11", "description": "Replanning Trigger & Route Invalidation"},
            run_id=run_id
        )

        await event_bus.emit(
            "replan.triggered",
            self.name,
            {
                "reason": reason,
                "excluded_providers": failed_provider_ids,
                "action": "re-entering pipeline at A3 (Geo Matcher)"
            },
            run_id=run_id
        )

        return {
            "replan_needed": True,
            "reason": reason,
            "excluded_providers": failed_provider_ids
        }


a11_replan = ReplannerAgent()
