"""
Admin Command Center API Endpoints.
Provides system metrics, database seeding, live decision resolution, and autopilot configuration.
"""

from fastapi import APIRouter, HTTPException, Body
from typing import Dict, Any, Optional
from app.db.mongo import get_collection, db_manager
from app.db.seed import seed_database
from app.db.models import AdminActionRequest
from app.agents.a8_admin_gate import a8_admin_gate
from app.config import GROQ_MODEL

router = APIRouter(prefix="/api/v1/admin", tags=["Admin"])


@router.get("/stats")
async def get_system_stats():
    """Returns platform operational metrics and live status."""
    requests_col = get_collection("requests")
    offers_col = get_collection("offers")
    matches_col = get_collection("matches")
    events_col = get_collection("agent_events")

    req_count = await requests_col.count_documents({})
    off_count = await offers_col.count_documents({})
    mat_count = await matches_col.count_documents({})
    evt_count = await events_col.count_documents({})

    return {
        "status": "operational",
        "llm_model": GROQ_MODEL,
        "is_mock_db": db_manager.is_mock(),
        "autopilot": {
            "enabled": a8_admin_gate.autopilot_enabled,
            "timeout_seconds": a8_admin_gate.autopilot_timeout,
        },
        "metrics": {
            "total_requests": req_count,
            "active_offers": off_count,
            "committed_matches": mat_count,
            "agent_events_emitted": evt_count
        },
        "pending_decisions_count": len(a8_admin_gate.list_pending())
    }


@router.post("/seed")
async def trigger_seed(force: bool = True):
    """Resets and seeds default disaster relief depots and inventory."""
    await seed_database(force=force)
    return {"status": "seeded", "message": "Relief provider inventory seeded successfully."}


@router.get("/decisions/pending")
async def list_pending_decisions():
    """Lists all decisions waiting for human dispatcher action."""
    return {"pending": a8_admin_gate.list_pending()}


@router.post("/decisions/{decision_id}/action")
async def submit_admin_action(decision_id: str, action: AdminActionRequest):
    """
    Submits an Approve, Override, or Reject action to the A8 Admin Gate.
    Resolves the parked asyncio.Future in the agent pipeline.
    """
    action_data = action.model_dump()
    resolved = a8_admin_gate.resolve_decision(decision_id, action_data)
    if not resolved:
        raise HTTPException(status_code=404, detail=f"Pending decision '{decision_id}' not found or already resolved.")
    return {"status": "resolved", "decision_id": decision_id, "action": action.action}


@router.post("/autopilot")
async def configure_autopilot(
    enabled: bool = Body(..., embed=True),
    timeout_seconds: Optional[float] = Body(None, embed=True)
):
    """Enables/disables Autopilot auto-dispatch timer."""
    a8_admin_gate.set_autopilot(enabled, timeout_seconds)
    return {
        "status": "updated",
        "autopilot_enabled": a8_admin_gate.autopilot_enabled,
        "timeout_seconds": a8_admin_gate.autopilot_timeout
    }
