"""
Agent A6: Arbiter (Groq LLM with Strict Pydantic Validation & Hallucination Firewall).
Selects a single pre-calculated option_id from the A5 Solver based on the A4 debate.
Enforces the Hallucination Firewall: Strictly prohibited from modifying numbers.
"""

from typing import Dict, Any
from pydantic import BaseModel, Field
from app.agents.llm_client import groq_service
from app.bus.eventbus import event_bus


class ArbiterDecision(BaseModel):
    selected_option_id: str = Field(..., description="Must be one of: fastest | max_coverage | least_depleting")
    reasoning: str = Field(..., description="Tactical justification for the chosen allocation plan")
    confidence_score: float = Field(..., ge=0.0, le=1.0)


class ArbiterAgent:
    name = "A6_Arbiter"

    async def arbitrate(
        self,
        options: Dict[str, Any],
        triage_info: Dict[str, Any],
        debate_info: Dict[str, Any],
        run_id: str
    ) -> Dict[str, Any]:
        await event_bus.emit(
            "agent.entered",
            self.name,
            {"stage": "A6", "description": "Plan Arbitration & Selection (Hallucination Firewalled)"},
            run_id=run_id
        )

        priority = triage_info.get("priority_level", "P2_HIGH")

        # Deterministic fallback decision
        if priority == "P1_CRITICAL":
            fallback_id = "fastest"
            fallback_reason = "Critical life-safety threat mandates fastest physical arrival time over secondary stock considerations."
        elif options.get("max_coverage", {}).get("coverage_ratio", 0) > options.get("fastest", {}).get("coverage_ratio", 0):
            fallback_id = "max_coverage"
            fallback_reason = "Maximizing total supply coverage provides highest overall relief for the affected group."
        else:
            fallback_id = "least_depleting"
            fallback_reason = "Depletion balancing protects forward medical outposts while fulfilling requested quota."

        fallback_decision = {
            "selected_option_id": fallback_id,
            "reasoning": fallback_reason,
            "confidence_score": 0.95
        }

        system_prompt = (
            "You are the PACT Arbiter Agent. Evaluate the multi-agent debate and triage urgency to select "
            "the single best allocation plan among the 3 provided solver options.\n"
            "HALLUCINATION FIREWALL MANDATE: You are strictly prohibited from generating numbers, modifying stock, "
            "or creating new allocations. You MUST select an existing 'selected_option_id' from ['fastest', 'max_coverage', 'least_depleting'].\n"
            "You must output a JSON object strictly matching this format:\n"
            "{\n"
            '  "selected_option_id": "fastest",\n'
            '  "reasoning": "Tactical justification for this choice.",\n'
            '  "confidence_score": 0.95\n'
            "}"
        )

        options_summary = []
        for opt_id, opt in options.items():
            cov = opt.get("coverage_ratio", 1.0) * 100
            eta = opt.get("max_eta_hours", 1.0)
            dep = opt.get("depletion_impact", "low")
            title = opt.get("title", opt_id)
            options_summary.append(
                f"Option '{opt_id}': {title} - Coverage: {cov}%, Max ETA: {eta}h, Depletion: {dep}"
            )

        # Extract key debate dialogue turns
        debate_turns = debate_info.get("turns", [])
        debate_dialogue = []
        for t in debate_turns[:6]:
            debate_dialogue.append(f"• [{t.get('speaker_name', 'Advocate')}]: \"{t.get('argument')}\"")

        user_prompt = (
            f"TRIAGE PRIORITY: {priority}\n"
            f"MULTI-AGENT DEBATE TRANSCRIPT:\n" + ("\n".join(debate_dialogue) if debate_dialogue else debate_info.get('consensus_summary', 'None')) + "\n\n"
            f"DEBATE CONSENSUS: {debate_info.get('consensus_summary')}\n\n"
            f"AVAILABLE PRE-SOLVED OPTIONS:\n" + "\n".join(options_summary) + "\n\n"
            "As Chief Incident Arbiter, judge the arguments and choose the single winning option."
        )

        result = await groq_service.stream_chat(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            agent_name=self.name,
            run_id=run_id,
            schema=ArbiterDecision,
            fallback_data=fallback_decision
        )

        # Enforce Hallucination Firewall validation
        chosen_id = result.get("selected_option_id")
        if chosen_id not in options:
            await event_bus.emit(
                "error",
                self.name,
                {"warning": f"LLM proposed invalid option_id '{chosen_id}'. Firewalled to fallback '{fallback_id}'."},
                run_id=run_id
            )
            result["selected_option_id"] = fallback_id
            chosen_id = fallback_id

        selected_plan = options[chosen_id]

        await event_bus.emit(
            "decision.proposed",
            self.name,
            {
                "selected_option_id": chosen_id,
                "reasoning": result.get("reasoning"),
                "chosen_plan": selected_plan
            },
            run_id=run_id
        )

        return {
            "decision": result,
            "chosen_plan": selected_plan
        }


a6_arbiter = ArbiterAgent()
