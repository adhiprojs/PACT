"""
Agent A8: Admin Gate (Human-in-the-Loop Interrupt & Autopilot Engine).
Parks pipeline on an asyncio.Future keyed by decision_id.
Enables instant dispatcher Approve, Override, or Reject, or automated dispatch via Autopilot timer.
"""

import asyncio
import time
import logging
from typing import Dict, Any, Optional
from app.config import AUTOPILOT_ENABLED, AUTOPILOT_TIMEOUT_SECONDS
from app.bus.eventbus import event_bus
from app.db.mongo import get_collection

logger = logging.getLogger("pact.admin_gate")


class AdminGateAgent:
    name = "A8_AdminGate"

    def __init__(self):
        self._pending_futures: Dict[str, asyncio.Future] = {}
        self._pending_decisions: Dict[str, Dict[str, Any]] = {}
        self.autopilot_enabled: bool = AUTOPILOT_ENABLED
        self.autopilot_timeout: float = AUTOPILOT_TIMEOUT_SECONDS

    async def await_approval(
        self,
        decision_id: str,
        chosen_plan: Dict[str, Any],
        options: Dict[str, Any],
        run_id: str
    ) -> Dict[str, Any]:
        """
        Pauses execution until admin action is submitted or autopilot timeout expires.
        """
        loop = asyncio.get_running_loop()
        fut = loop.create_future()
        self._pending_futures[decision_id] = fut
        self._pending_decisions[decision_id] = {
            "decision_id": decision_id,
            "run_id": run_id,
            "chosen_plan": chosen_plan,
            "options": options,
            "created_at": time.time(),
            "status": "pending_admin"
        }

        await event_bus.emit(
            "awaiting_admin",
            self.name,
            {
                "decision_id": decision_id,
                "chosen_option_id": chosen_plan.get("option_id"),
                "autopilot_enabled": self.autopilot_enabled,
                "autopilot_timeout_seconds": self.autopilot_timeout,
                "options": options
            },
            run_id=run_id
        )

        try:
            if self.autopilot_enabled:
                # Wait with timeout for human interrupt
                try:
                    result = await asyncio.wait_for(fut, timeout=self.autopilot_timeout)
                except asyncio.TimeoutError:
                    result = {
                        "action": "approve",
                        "auto_approved": True,
                        "dispatcher_notes": f"Auto-approved by Autopilot timer ({self.autopilot_timeout}s timeout)."
                    }
                    await event_bus.emit(
                        "admin.action",
                        self.name,
                        {"decision_id": decision_id, "action": "autopilot_approved", "notes": result["dispatcher_notes"]},
                        run_id=run_id
                    )
            else:
                # Wait indefinitely for admin action
                result = await fut
                await event_bus.emit(
                    "admin.action",
                    self.name,
                    {"decision_id": decision_id, "action": result.get("action"), "details": result},
                    run_id=run_id
                )

            # Record in admin_actions collection (never TTL)
            admin_actions_col = get_collection("admin_actions")
            await admin_actions_col.insert_one({
                "decision_id": decision_id,
                "run_id": run_id,
                "action": result.get("action"),
                "auto_approved": result.get("auto_approved", False),
                "details": result,
                "timestamp": time.time()
            })

            return result

        finally:
            self._pending_futures.pop(decision_id, None)
            self._pending_decisions.pop(decision_id, None)

    def resolve_decision(self, decision_id: str, action_data: Dict[str, Any]) -> bool:
        """Called by HTTP REST admin action endpoint."""
        fut = self._pending_futures.get(decision_id)
        if fut and not fut.done():
            fut.set_result(action_data)
            return True
        return False

    def list_pending(self) -> Dict[str, Any]:
        return self._pending_decisions

    def set_autopilot(self, enabled: bool, timeout_seconds: Optional[float] = None):
        self.autopilot_enabled = enabled
        if timeout_seconds:
            self.autopilot_timeout = timeout_seconds


a8_admin_gate = AdminGateAgent()
