"""
Tests for Multi-Agent Reasoning Pipeline, Solver Arithmetic, and Firewall Boundaries.
"""

import pytest
import asyncio
from app.db.mongo import db_manager
from app.db.seed import seed_database
from app.agents.pipeline import pipeline
from app.agents.a5_solver import a5_solver
from app.agents.a6_arbiter import a6_arbiter
from app.agents.a7_redactor import a7_redactor
from app.agents.a8_admin_gate import a8_admin_gate


@pytest.mark.asyncio
async def test_solver_deterministic_math():
    demand = [
        {"resource_key": "food_kits", "quantity": 100},
        {"resource_key": "water_kits", "quantity": 250},
        {"resource_key": "medical_kits", "quantity": 10}
    ]
    candidates = [
        {
            "provider_id": "DEPOT_A",
            "provider_name": "Depot A (Close)",
            "distance_km": 2.0,
            "eta_hours": 0.5,
            "inventory": {"food_kits": 50, "water_kits": 100, "medical_kits": 20}
        },
        {
            "provider_id": "DEPOT_B",
            "provider_name": "Depot B (Large Hub)",
            "distance_km": 15.0,
            "eta_hours": 2.0,
            "inventory": {"food_kits": 500, "water_kits": 1000, "medical_kits": 5}
        }
    ]

    options = await a5_solver.solve(demand, candidates, run_id="test_run")

    assert "fastest" in options
    assert "max_coverage" in options
    assert "least_depleting" in options

    # Check fastest option allocates from closest first
    fastest = options["fastest"]
    assert fastest["coverage_ratio"] == 1.0
    alloc_a = [a for a in fastest["allocations"] if a["provider_id"] == "DEPOT_A"][0]
    assert alloc_a["items"]["food_kits"] == 50  # took all 50 available
    assert alloc_a["items"]["water_kits"] == 100
    assert alloc_a["items"]["medical_kits"] == 10

    # Ensure no allocated quantity exceeds inventory
    for opt_id, opt in options.items():
        for alloc in opt["allocations"]:
            p_id = alloc["provider_id"]
            cand_inv = [c["inventory"] for c in candidates if c["provider_id"] == p_id][0]
            for r_key, qty in alloc["items"].items():
                assert qty <= cand_inv[r_key], f"Allocated {qty} exceeds stock {cand_inv[r_key]}"


@pytest.mark.asyncio
async def test_arbiter_hallucination_firewall():
    options = {
        "fastest": {"option_id": "fastest", "title": "Fast Plan", "max_eta_hours": 1.0, "allocations": []},
        "max_coverage": {"option_id": "max_coverage", "title": "Max Plan", "max_eta_hours": 3.0, "allocations": []},
        "least_depleting": {"option_id": "least_depleting", "title": "Balanced Plan", "max_eta_hours": 2.0, "allocations": []}
    }
    triage = {"priority_level": "P1_CRITICAL", "risk_score": 9.5}
    debate = {"consensus_summary": "Urgent medical required"}

    res = await a6_arbiter.arbitrate(options, triage, debate, run_id="test_arbiter")
    chosen = res["decision"]["selected_option_id"]
    assert chosen in options, f"Selected option '{chosen}' is not in valid pre-solved set"


@pytest.mark.asyncio
async def test_privacy_redaction():
    req_data = {
        "uid": "7F3K",
        "sender": "+919876543210",
        "geo": {"latitude": 23.25991, "longitude": 77.41263}
    }
    plan = {"option_id": "fastest"}

    redacted = await a7_redactor.redact(req_data, plan, run_id="test_redactor")
    assert redacted["uid"] == "7F3K"
    assert redacted["masked_phone"] == "+91******3210"
    assert redacted["masked_coordinates"] == [77.41, 23.26]  # fuzzed


@pytest.mark.asyncio
async def test_full_pipeline_execution():
    await db_manager.connect()
    await seed_database(force=True)
    a8_admin_gate.set_autopilot(enabled=True, timeout_seconds=0.1)

    raw_sms = "Q|001|7F3K|15223C03Q0|6QR6VFBQ33|7F"
    result = await pipeline.run(raw_input=raw_sms, transport="sms", sender="+919876543210")

    assert result["status"] == "success"
    assert "match" in result
    match = result["match"]
    assert match["status"] == "committed"
    assert match["sms_ack_frame"].startswith("C|001|7F3K|")
    assert "OK" in match["sms_ack_frame"]
