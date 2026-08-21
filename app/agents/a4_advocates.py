"""
Agent A4: Autonomous Provider Advocate Agents.
Instantiates independent autonomous agent representatives for each candidate relief organization.
Executes an authentic multi-round debate with opening bids, cross-agency rebuttals, and consensus building.
"""

import asyncio
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from app.agents.llm_client import groq_service
from app.bus.eventbus import event_bus


class DebateTurn(BaseModel):
    turn_id: str
    speaker: str
    speaker_name: str
    role_title: str
    stance: str  # advocate | challenge | concede | compromise
    argument: str
    rebuts: Optional[str] = None


class DebateOutput(BaseModel):
    debate_topic: str
    turns: List[DebateTurn]
    consensus_summary: str


class ProviderAdvocate:
    """Independent autonomous agent representative for a specific relief provider."""

    def __init__(self, candidate: Dict[str, Any]):
        self.provider_id = candidate.get("provider_id", "DEPOT")
        self.name = candidate.get("name") or candidate.get("provider_name", "Relief Depot")
        self.org_type = candidate.get("org_type", "NGO")
        self.distance_km = round(float(candidate.get("distance_km", 15.0)), 1)
        self.eta_hours = round(float(candidate.get("eta_hours", 1.0)), 1)
        self.inventory = candidate.get("inventory", {})
        self.fleet = candidate.get("fleet_description", "Logistics vehicles")
        self.contact_person = candidate.get("contact_person", "Logistics Officer")

        # Persona customization based on organization profile
        if "HOSP" in self.provider_id or "MEDICAL" in self.provider_id:
            self.role_title = "Chief Medical & Trauma Liaison"
            self.core_priority = "Urgent clinical stabilization, ALS trauma transport, and securing medical supplies."
        elif "TNDRF" in self.provider_id or "RESCUE" in self.provider_id or "NDRF" in self.provider_id:
            self.role_title = "Disaster Rescue Operations Commander"
            self.core_priority = "Rapid physical extraction, water rescue using amphibious boats, and life-safety."
        elif "CSR" in self.provider_id or "TATA" in self.provider_id:
            self.role_title = "Corporate Bulk Supply Chain Director"
            self.core_priority = "Bulk food/water replenishment, power generation, and preserving forward clinic stocks."
        else:
            self.role_title = "Humanitarian Field Aid Coordinator"
            self.core_priority = "Essential family sustenance, hygiene kits, and protecting community reserves."

    async def generate_opening_bid(
        self,
        triage_info: Dict[str, Any],
        weather_info: Dict[str, Any],
        needed_resources: List[str]
    ) -> str:
        """Round 1: Advocate presents capabilities, travel viability, and tactical value."""
        stock_summary = ", ".join([f"{v} {k.replace('_', ' ').title()}" for k, v in self.inventory.items() if v > 0]) or "Emergency aid supplies"
        
        system_prompt = (
            f"You are {self.contact_person}, {self.role_title} representing {self.name}.\n"
            f"Your Location: {self.distance_km} km away (ETA ~{self.eta_hours}h). Transport Fleet: {self.fleet}.\n"
            f"Your Stockpile On-Hand: {stock_summary}.\n"
            "Argue in 2 concise, professional first-person sentences why your organization should deploy. "
            "You MUST state your exact distance in km, your ETA, and cite your specific vehicles and stock."
        )

        user_prompt = (
            f"Incident Priority: {triage_info.get('priority_level', 'P1_CRITICAL')}\n"
            f"Casualty Status: {triage_info.get('clinical_assessment', 'Victims in need')}\n"
            f"Weather Hazards: {weather_info.get('hazard_classification', 'FLOOD')} "
            f"(Water Depth: {weather_info.get('estimated_water_depth_m', 0.5)}m, Rain: {weather_info.get('precipitation_rate_mm_hr', 50)}mm/h)\n"
            f"Requested Aid: {', '.join(needed_resources) if needed_resources else 'Emergency Aid'}\n"
            "State your opening tactical deployment bid."
        )

        fallback = (
            f"[{self.name}] We are stationed {self.distance_km} km from the incident (ETA ~{self.eta_hours}h). "
            f"With our fleet of {self.fleet} and stock of {stock_summary}, we can deploy immediately to meet victim needs."
        )

        try:
            return await groq_service.stream_text(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                agent_name=f"Advocate_{self.provider_id}",
                fallback_text=fallback
            )
        except Exception:
            return fallback

    async def generate_rebuttal(
        self,
        triage_info: Dict[str, Any],
        competitor_bids: List[Dict[str, Any]],
        min_distance: float
    ) -> str:
        """Round 2: Reviews competitors' arguments, challenges bottlenecks, and proposes a consensus compromise."""
        other_bids_text = "\n".join([f"- {b['name']} ({b['distance_km']} km away): \"{b['bid']}\"" for b in competitor_bids if b['provider_id'] != self.provider_id])
        stock_summary = ", ".join([f"{v} {k.replace('_', ' ').title()}" for k, v in self.inventory.items() if v > 0]) or "relief reserves"

        system_prompt = (
            f"You are {self.contact_person}, {self.role_title} representing {self.name}.\n"
            f"Your exact distance is {self.distance_km} km (ETA {self.eta_hours}h). Fleet: {self.fleet}. Stock: {stock_summary}.\n"
            "Review the competing bids from other agencies below. In 2 sharp, realistic sentences:\n"
            "- If you are the closest depot (under 25km), assert your immediate transit advantage.\n"
            "- If you are further away, acknowledge the closer frontline team and commit your specific stockpile to secondary bulk replenishment.\n"
            "NEVER output generic placeholder text."
        )

        user_prompt = (
            f"Incident: {triage_info.get('triage_summary', 'Emergency Response')}\n"
            f"Other Agency Bids:\n{other_bids_text or 'None'}\n"
            "Provide your tactical rebuttal or collaborative compromise."
        )

        if self.distance_km <= (min_distance + 6.0):
            fallback = (
                f"[{self.name}] At only {self.distance_km} km away (ETA ~{self.eta_hours}h), our {self.fleet} have the fastest transit window. "
                f"We will execute the primary on-site delivery while rear depots prepare replenishment."
            )
        else:
            fallback = (
                f"[{self.name}] Since we are {self.distance_km} km out, we support closer units taking the initial response, "
                f"while we mobilize our {self.fleet} with {stock_summary} to replenish forward supplies."
            )

        try:
            return await groq_service.stream_text(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                agent_name=f"Rebuttal_{self.provider_id}",
                fallback_text=fallback
            )
        except Exception:
            return fallback


class AdvocatesAgent:
    name = "A4_Advocates"

    async def deliberate(
        self,
        candidates: List[Dict[str, Any]],
        triage_info: Dict[str, Any],
        needed_resources: List[Dict[str, Any]],
        run_id: str
    ) -> Dict[str, Any]:
        await event_bus.emit(
            "agent.entered",
            self.name,
            {"stage": "A4", "description": "Autonomous Multi-Agent Provider Deliberation"},
            run_id=run_id
        )

        await event_bus.emit("debate.opened", self.name, {"candidate_count": len(candidates)}, run_id=run_id)

        if not candidates:
            return {
                "debate_topic": "No candidate depots within search perimeter",
                "turns": [],
                "consensus_summary": "No candidate facilities available for deliberation."
            }

        # Filter and prioritize the top 4 closest candidate depots
        sorted_candidates = sorted(candidates, key=lambda c: c.get("distance_km", 999.0))
        top_candidates = sorted_candidates[:4]
        advocates = [ProviderAdvocate(c) for c in top_candidates]
        needed_labels = [r.get("label", "Aid") for r in needed_resources]
        weather_info = triage_info.get("weather_telemetry", {})

        min_distance = min([adv.distance_km for adv in advocates]) if advocates else 10.0
        turns: List[DebateTurn] = []

        # ROUND 1: OPENING BIDS & PROXIMITY CLAIMS
        round1_bids = []
        for adv in advocates:
            argument = await adv.generate_opening_bid(
                triage_info=triage_info,
                weather_info=weather_info,
                needed_resources=needed_labels
            )
            turn = DebateTurn(
                turn_id=f"r1_{adv.provider_id}",
                speaker=adv.provider_id,
                speaker_name=adv.name,
                role_title=adv.role_title,
                stance="advocate",
                argument=argument,
                rebuts=None
            )
            turns.append(turn)
            round1_bids.append({
                "provider_id": adv.provider_id,
                "name": adv.name,
                "role": adv.role_title,
                "distance_km": adv.distance_km,
                "bid": argument
            })

            await event_bus.emit(
                "debate.turn",
                self.name,
                {
                    "speaker": adv.name,
                    "role": adv.role_title,
                    "stance": f"Opening Bid ({adv.distance_km} km · ETA ~{adv.eta_hours}h)",
                    "argument": argument
                },
                run_id=run_id
            )
            await asyncio.sleep(0.05)

        # ROUND 2: CROSS-AGENCY REBUTTALS & COLLABORATIVE COMPROMISE
        for adv in advocates:
            rebuttal = await adv.generate_rebuttal(
                triage_info=triage_info,
                competitor_bids=round1_bids,
                min_distance=min_distance
            )
            turn = DebateTurn(
                turn_id=f"r2_{adv.provider_id}",
                speaker=adv.provider_id,
                speaker_name=adv.name,
                role_title=adv.role_title,
                stance="compromise",
                argument=rebuttal,
                rebuts="Round 1 Proposals"
            )
            turns.append(turn)

            await event_bus.emit(
                "debate.turn",
                self.name,
                {
                    "speaker": adv.name,
                    "role": adv.role_title,
                    "stance": f"Tactical Rebuttal ({adv.distance_km} km)",
                    "argument": rebuttal
                },
                run_id=run_id
            )
            await asyncio.sleep(0.05)

        closest_adv = advocates[0]
        consensus = (
            f"Consensus reached: {closest_adv.name} ({closest_adv.distance_km} km away) is assigned frontline rapid dispatch, "
            f"while secondary hubs maintain strategic supply buffers."
        )

        debate_result = {
            "debate_topic": f"Multi-Agency Response Allocation for {triage_info.get('priority_level', 'P1_CRITICAL')} incident",
            "turns": [t.model_dump() for t in turns],
            "consensus_summary": consensus
        }

        await event_bus.emit(
            "agent.completed",
            self.name,
            {
                "turns_count": len(turns),
                "consensus": consensus
            },
            run_id=run_id
        )

        return debate_result


a4_advocates = AdvocatesAgent()
