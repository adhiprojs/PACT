"""
Master Multi-Agent Pipeline Orchestrator for PACT (A0 -> A11).
Coordinates deterministic Python tools and Groq LLMs while enforcing the Hallucination Firewall.
"""

import time
import uuid
import logging
from typing import Dict, Any, List, Optional
from app.bus.eventbus import event_bus
from app.db.mongo import get_collection
from app.codec.fanout import q_to_n_fanout

from app.agents.a0_intake import a0_intake
from app.agents.a1_dedupe import a1_dedupe
from app.agents.a2_triage import a2_triage
from app.agents.a3_geo_matcher import a3_geo_matcher
from app.agents.a4_advocates import a4_advocates
from app.agents.a5_solver import a5_solver
from app.agents.a6_arbiter import a6_arbiter
from app.agents.a7_redactor import a7_redactor
from app.agents.a8_admin_gate import a8_admin_gate
from app.agents.a9_narrator import a9_narrator
from app.agents.a10_verify import a10_verify
from app.agents.a11_replan import a11_replan

logger = logging.getLogger("pact.pipeline")


class PipelineOrchestrator:
    async def run(
        self,
        raw_input: str,
        transport: str = "http",
        sender: Optional[str] = None
    ) -> Dict[str, Any]:
        run_id = f"run_{uuid.uuid4().hex[:8]}"
        trace_id = f"tr_{int(time.time()*1000)}"

        await event_bus.emit(
            "run.started",
            "Orchestrator",
            {"run_id": run_id, "transport": transport, "raw_input": raw_input, "sender": sender},
            run_id=run_id,
            trace_id=trace_id
        )

        try:
            # 1. A0: Intake & Checksum
            success, parsed_data, err_msg = await a0_intake.process(raw_input, run_id=run_id, transport=transport)
            if not success:
                await event_bus.emit("error", "Orchestrator", {"stage": "A0", "error": err_msg}, run_id=run_id)
                return {"status": "error", "stage": "A0", "error": err_msg, "run_id": run_id}

            if sender:
                parsed_data["sender"] = sender

            # 2. A1: Deduplication & Anti-Fraud Flood Detection
            is_dup, dedupe_key = await a1_dedupe.check_and_record(parsed_data, run_id=run_id)
            if is_dup:
                from app.codec.checksum import calculate_xor_checksum
                is_fraud = "SUSPICIOUS_FLOOD" in dedupe_key
                status_code = "DENIED_SPAM" if is_fraud else "DUP"
                ack_body = f"C|{parsed_data.get('seq', '000')}|{parsed_data.get('uid', 'SOS')}|{status_code}|00"
                ack_crc = calculate_xor_checksum(ack_body)
                full_ack = f"{ack_body}|{ack_crc}"

                await event_bus.emit(
                    "run.completed",
                    "Orchestrator",
                    {
                        "status": "denied_flood" if is_fraud else "duplicate_suppressed",
                        "reason": "Rapid-fire flood rate limit triggered" if is_fraud else "Duplicate sequence",
                        "ack_sms": full_ack
                    },
                    run_id=run_id
                )
                return {"status": "denied" if is_fraud else "duplicate", "dedupe_key": dedupe_key, "ack_sms": full_ack, "run_id": run_id}

            # If S Status update from delivery truck driver
            if parsed_data.get("message_type") == "S" or parsed_data.get("type") == "status":
                plan_id = parsed_data.get("plan_id", "PLAN_001")
                new_status = parsed_data.get("status", "in_transit")
                status_code = parsed_data.get("status_code", "1")
                matches_col = get_collection("matches")
                
                await matches_col.update_one(
                    {"match_id": plan_id},
                    {"$set": {"delivery_status": new_status, "delivery_status_code": status_code, "updated_at": time.time()}}
                )
                
                status_ack = f"C|{parsed_data.get('seq', '001')}|{plan_id}|ACK_{new_status.upper()}"
                from app.codec.checksum import calculate_xor_checksum
                ack_crc = calculate_xor_checksum(status_ack)
                full_status_ack = f"{status_ack}|{ack_crc}"
                
                await event_bus.emit(
                    "match.status_updated",
                    "Orchestrator",
                    {"plan_id": plan_id, "status": new_status, "status_code": status_code, "ack": full_status_ack},
                    run_id=run_id
                )
                
                await event_bus.emit(
                    "run.completed",
                    "Orchestrator",
                    {"run_id": run_id, "status": "status_updated", "plan_id": plan_id, "delivery_status": new_status, "ack_sms": full_status_ack},
                    run_id=run_id
                )
                return {
                    "status": "status_updated",
                    "run_id": run_id,
                    "plan_id": plan_id,
                    "delivery_status": new_status,
                    "ack_sms": full_status_ack
                }

            # Normalize request and persist to MongoDB
            requests_col = get_collection("requests")
            req_doc = {
                "run_id": run_id,
                "raw_frame": raw_input,
                "parsed": parsed_data,
                "transport": transport,
                "loc": parsed_data.get("geo", {}).get("coordinates", [77.4126, 23.2599]),
                "status": "in_progress",
                "created_at": time.time()
            }
            await requests_col.insert_one(req_doc)

            # Fan-out to discrete needs if Q citizen request
            if parsed_data.get("message_type") == "Q" or parsed_data.get("type") == "individual_request":
                need_items = q_to_n_fanout(parsed_data)
            else:
                # Standard N need or other message
                need_items = [{
                    "need_id": f"ND_{parsed_data.get('seq')}",
                    "uid": parsed_data.get("organization_id", "ORG"),
                    "resource_key": parsed_data.get("resource", "food_kits"),
                    "quantity": parsed_data.get("quantity", 100),
                    "urgency": parsed_data.get("urgency", "medium"),
                    "location_coordinates": parsed_data.get("geo", {}).get("coordinates", [77.4126, 23.2599])
                }]

            # 3. A2: Triage Assessment
            triage_info = await a2_triage.evaluate(parsed_data, run_id=run_id)

            # Iterative candidate matching & solving loop (allows A11 Replanning)
            excluded_providers: List[str] = []
            pinned_provider_id: Optional[str] = None
            max_attempts = 3
            attempt = 0
            final_match_record = None

            target_coords = parsed_data.get("geo", {}).get("coordinates", [77.4126, 23.2599])
            needs_bitfield = parsed_data.get("payload", {}).get("needs_bitfield", 0)

            while attempt < max_attempts:
                attempt += 1

                # 4. A3: Geo Candidates Matcher
                candidates = await a3_geo_matcher.find_candidates(
                    target_coords=target_coords,
                    needed_bitfield=needs_bitfield,
                    run_id=run_id,
                    excluded_providers=excluded_providers
                )

                if not candidates:
                    await event_bus.emit(
                        "error",
                        "Orchestrator",
                        {"error": "NO_PROVIDERS_IN_RANGE", "radius_exhausted": True},
                        run_id=run_id
                    )
                    break

                # 5. A4: Provider Advocates Deliberation
                debate_info = await a4_advocates.deliberate(
                    candidates=candidates,
                    triage_info=triage_info,
                    needed_resources=need_items,
                    run_id=run_id
                )

                # 6. A5: Allocation Solver (Deterministic Math)
                options = await a5_solver.solve(
                    need_items=need_items,
                    candidates=candidates,
                    run_id=run_id,
                    pinned_provider_id=pinned_provider_id
                )

                # 7. A6: Arbiter (Option Selection)
                arbiter_res = await a6_arbiter.arbitrate(
                    options=options,
                    triage_info=triage_info,
                    debate_info=debate_info,
                    run_id=run_id
                )
                chosen_plan = arbiter_res["chosen_plan"]

                # 8. A7: Privacy Redactor
                redacted_view = await a7_redactor.redact(parsed_data, chosen_plan, run_id=run_id)

                # 9. A8: Admin Gate (Autopilot / Human Interrupt)
                decision_id = f"dec_{run_id}_{attempt}"
                admin_action = await a8_admin_gate.await_approval(
                    decision_id=decision_id,
                    chosen_plan=chosen_plan,
                    options=options,
                    run_id=run_id
                )

                action_type = admin_action.get("action", "approve")

                if action_type == "reject":
                    # Admin rejected this plan -> trigger replanner
                    rejected_provider = admin_action.get("reject_provider_id") or candidates[0].get("provider_id")
                    excluded_providers.append(rejected_provider)
                    await a11_replan.trigger_replan(
                        reason=admin_action.get("reject_reason", "Dispatcher Rejected Allocation"),
                        failed_provider_ids=excluded_providers,
                        request_data=parsed_data,
                        run_id=run_id
                    )
                    continue

                if action_type == "override":
                    if admin_action.get("override_option_id") in options:
                        chosen_plan = options[admin_action["override_option_id"]]
                    elif admin_action.get("pinned_provider_id"):
                        pinned_provider_id = admin_action["pinned_provider_id"]
                        continue

                # 10. A9: Operational Narration
                narrative = await a9_narrator.narrate(
                    request_data=parsed_data,
                    triage_info=triage_info,
                    chosen_plan=chosen_plan,
                    admin_action=admin_action,
                    run_id=run_id
                )

                # 11. A10: Verification & Database Commit
                final_match_record = await a10_verify.commit_and_verify(
                    request_data=parsed_data,
                    triage_info=triage_info,
                    chosen_plan=chosen_plan,
                    admin_action=admin_action,
                    run_id=run_id
                )
                break

            await event_bus.emit(
                "run.completed",
                "Orchestrator",
                {
                    "run_id": run_id,
                    "status": "success" if final_match_record else "failed",
                    "match": final_match_record
                },
                run_id=run_id
            )

            return {
                "status": "success" if final_match_record else "failed",
                "run_id": run_id,
                "parsed": parsed_data,
                "triage": triage_info,
                "match": final_match_record
            }

        except Exception as e:
            logger.exception("Pipeline execution error in %s", run_id)
            await event_bus.emit("error", "Orchestrator", {"error": str(e)}, run_id=run_id)
            return {"status": "error", "error": str(e), "run_id": run_id}


pipeline = PipelineOrchestrator()
