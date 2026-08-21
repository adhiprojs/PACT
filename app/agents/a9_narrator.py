"""
Agent A9: Narrator (Groq LLM / Fallback).
Generates plain-English situational bulletins and live operational dispatch logs.
"""

from typing import Dict, Any
from pydantic import BaseModel, Field
from app.agents.llm_client import groq_service
from app.bus.eventbus import event_bus


class NarratorOutput(BaseModel):
    operational_bulletin: str = Field(..., description="Clear, professional plain-English dispatch bulletin")
    key_action_items: list[str] = Field(default_factory=list)


class NarratorAgent:
    name = "A9_Narrator"

    async def narrate(
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
            {"stage": "A9", "description": "Operational Dispatch Narration"},
            run_id=run_id
        )

        providers = [a.get("provider_name") for a in chosen_plan.get("allocations", [])]
        prov_str = ", ".join(providers) if providers else "Assigned Response Units"
        total_items = chosen_plan.get("total_fulfilled", {})
        item_summary = ", ".join(f"{v} {k}" for k, v in total_items.items() if v > 0)

        fallback_bulletin = (
            f"DISPATCH COMMITTED: Responding to {triage_info.get('priority_level', 'P1')} emergency. "
            f"{prov_str} tasked with immediate transit (ETA: {chosen_plan.get('max_eta_hours')}h). "
            f"Mobilizing {item_summary or 'emergency kits'} under plan '{chosen_plan.get('option_id')}'. "
            f"Action verified by {admin_action.get('dispatcher_notes', 'Admin Gate')}."
        )

        fallback_data = {
            "operational_bulletin": fallback_bulletin,
            "key_action_items": [
                f"Dispatch units: {prov_str}",
                f"Supplies committed: {item_summary}",
                f"Estimated arrival: within {chosen_plan.get('max_eta_hours')} hours"
            ]
        }

        system_prompt = (
            "You are the PACT Operational Narrator. Generate a succinct, high-clarity emergency response bulletin "
            "summarizing the finalized dispatch decision for commanders and field operators.\n"
            "You must output a JSON object strictly matching this format:\n"
            "{\n"
            '  "operational_bulletin": "DISPATCH COMMITTED: Responding to critical emergency...",\n'
            '  "key_action_items": ["Action 1", "Action 2"]\n'
            "}"
        )

        user_prompt = (
            f"PRIORITY: {triage_info.get('priority_level')}\n"
            f"PLAN: {chosen_plan.get('title')} ({chosen_plan.get('option_id')})\n"
            f"PROVIDERS: {prov_str}\n"
            f"FULFILLED SUPPLIES: {item_summary}\n"
            f"MAX ETA: {chosen_plan.get('max_eta_hours')} hours\n"
            f"ADMIN STATUS: {admin_action.get('action')}"
        )

        result = await groq_service.stream_chat(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            agent_name=self.name,
            run_id=run_id,
            schema=NarratorOutput,
            fallback_data=fallback_data
        )

        await event_bus.emit(
            "agent.message",
            self.name,
            {
                "stage": "A9",
                "bulletin": result,
                "text": result.get("operational_bulletin"),
                "action_items": result.get("key_action_items")
            },
            run_id=run_id
        )

        return result


a9_narrator = NarratorAgent()
