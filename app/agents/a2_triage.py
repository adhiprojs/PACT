"""
Agent A2: Triage Assessment (Groq Llama-3.3-70B / Fallback).
Evaluates crisis severity, medical emergencies, and life risks with real meteorological tool calling.
"""

from typing import Dict, Any, List
from pydantic import BaseModel, Field
from app.agents.llm_client import groq_service
from app.agents.tools import get_weather_and_flood_risk
from app.bus.eventbus import event_bus


class TriageOutput(BaseModel):
    priority_level: str = Field(..., description="P1_CRITICAL | P2_HIGH | P3_MEDIUM | P4_LOW")
    risk_score: float = Field(..., ge=1.0, le=10.0)
    hazard_tags: List[str] = Field(default_factory=list)
    clinical_assessment: str = Field(..., description="Detailed medical and human situational assessment")
    triage_summary: str = Field(..., description="Short operational analysis")
    immediate_risks: List[str] = Field(default_factory=list)


class TriageAgent:
    name = "A2_Triage"

    async def evaluate(self, request_data: Dict[str, Any], run_id: str) -> Dict[str, Any]:
        await event_bus.emit(
            "agent.entered",
            self.name,
            {"stage": "A2", "description": "Crisis Severity & Meteorological Tool Triage"},
            run_id=run_id
        )

        payload = request_data.get("payload", {})
        situation_name = payload.get("situation", {}).get("name", "Unknown Emergency")
        headcount_label = payload.get("headcount", {}).get("label", "1 person")
        people_est = payload.get("people_estimate", 1)
        injury_label = payload.get("injury", {}).get("label", "No injuries")
        mobility_label = payload.get("mobility", {}).get("label", "Mobile")
        urgency_label = payload.get("urgency", {}).get("label", "Medium")
        vulnerabilities = [v.get("label") for v in payload.get("vulnerabilities", [])]
        needed_resources = [r.get("label") for r in payload.get("needed_resources", [])]

        # Extract coordinates & execute Tool Calling for Weather/Flood Hazards
        geo = request_data.get("geo", {})
        coords = geo.get("coordinates", [80.2707, 13.0827])
        lat = geo.get("latitude") or (coords[1] if len(coords) > 1 else 13.0827)
        lon = geo.get("longitude") or (coords[0] if len(coords) > 0 else 80.2707)

        # ⚙️ EXECUTABLE TOOL CALL
        weather_data = get_weather_and_flood_risk(latitude=lat, longitude=lon)
        await event_bus.emit(
            "agent.tool_called",
            self.name,
            {
                "tool_name": "get_weather_and_flood_risk",
                "arguments": {"latitude": lat, "longitude": lon},
                "result": weather_data,
                "summary": f"Weather Telemetry: {weather_data['hazard_classification']} | Rain: {weather_data['precipitation_rate_mm_hr']}mm/h | Water Depth: {weather_data['estimated_water_depth_m']}m"
            },
            run_id=run_id
        )

        # Calculate deterministic baseline incorporating real weather data
        base_score = 4.0
        if "Critical" in urgency_label or "Fatal" in injury_label:
            base_score += 4.0
        elif "High" in urgency_label or "Serious" in injury_label:
            base_score += 2.5

        if "Trapped" in mobility_label or "Waterbound" in mobility_label:
            base_score += 1.5
        if weather_data.get("estimated_water_depth_m", 0) > 0.5:
            base_score += 1.0
        if vulnerabilities:
            base_score += min(2.0, len(vulnerabilities) * 0.7)

        final_score = min(10.0, round(base_score, 1))

        if final_score >= 8.0:
            priority = "P1_CRITICAL"
        elif final_score >= 6.0:
            priority = "P2_HIGH"
        elif final_score >= 4.0:
            priority = "P3_MEDIUM"
        else:
            priority = "P4_LOW"

        fallback_result = {
            "priority_level": priority,
            "risk_score": final_score,
            "hazard_tags": [situation_name.split("/")[0].strip(), urgency_label.upper()] + weather_data.get("active_hazard_flags", []),
            "clinical_assessment": f"Emergency incident involving {people_est} individuals under {situation_name}. Telemetry indicates {weather_data['hazard_classification']} ({weather_data['precipitation_rate_mm_hr']}mm/h rain, ~{weather_data['estimated_water_depth_m']}m standing water). Victim status: {injury_label}, {mobility_label}. Immediate clinical stabilization and specialized water extraction required.",
            "triage_summary": f"{situation_name} involving {headcount_label}. Status: {injury_label}, {mobility_label}. Weather: {weather_data['hazard_classification']}.",
            "immediate_risks": [
                f"Meteorological threat: {', '.join(weather_data.get('active_hazard_flags', []))}",
                f"Entrapment risk: {mobility_label}",
                f"Medical risk: {injury_label}",
                f"Vulnerable individuals: {', '.join(vulnerabilities) if vulnerabilities else 'None flagged'}"
            ]
        }

        system_prompt = (
            "You are the Chief Triage Medical Officer for a disaster response platform. "
            "Analyze the medical trauma, meteorological flood risks from tool telemetry, and survival timeline of the victims.\n"
            "Write like a real emergency doctor assessing casualties with human empathy, tactical urgency, and precise weather context.\n"
            "CRITICAL FIREWALL RULE: NEVER invent, calculate, or alter numerical resource quantities.\n"
            "You must output a JSON object strictly matching this format:\n"
            "{\n"
            '  "priority_level": "P1_CRITICAL",\n'
            '  "risk_score": 9.5,\n'
            '  "hazard_tags": ["Building Collapse", "TRAPPED", "Urban Waterlogging"],\n'
            '  "clinical_assessment": "Detailed 2-3 sentence medical and humanitarian diagnosis of the victims condition, weather exposure, and survival window.",\n'
            '  "triage_summary": "Short operational assessment.",\n'
            '  "immediate_risks": ["Risk 1", "Risk 2"]\n'
            "}"
        )

        user_prompt = (
            f"SITUATION: {situation_name}\n"
            f"POPULATION: {headcount_label} (~{people_est} persons)\n"
            f"INJURIES: {injury_label}\n"
            f"MOBILITY: {mobility_label}\n"
            f"URGENCY: {urgency_label}\n"
            f"METEOROLOGICAL TOOL DATA:\n"
            f"  - Hazard Level: {weather_data['hazard_classification']}\n"
            f"  - Precipitation: {weather_data['precipitation_rate_mm_hr']} mm/hr\n"
            f"  - Wind: {weather_data['wind_speed_km_h']} km/h\n"
            f"  - Water Depth: {weather_data['estimated_water_depth_m']} meters\n"
            f"  - Active Threats: {', '.join(weather_data['active_hazard_flags'])}\n"
            f"VULNERABILITIES: {', '.join(vulnerabilities) if vulnerabilities else 'None'}\n"
            f"REQUESTED AID: {', '.join(needed_resources) if needed_resources else 'General'}\n"
        )

        result = await groq_service.stream_chat(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            agent_name=self.name,
            run_id=run_id,
            schema=TriageOutput,
            fallback_data=fallback_result
        )

        # Attach tool telemetry to final result
        result["weather_telemetry"] = weather_data

        await event_bus.emit(
            "agent.completed",
            self.name,
            {
                "priority": result.get("priority_level"),
                "risk_score": result.get("risk_score"),
                "summary": result.get("triage_summary")
            },
            run_id=run_id
        )

        return result


a2_triage = TriageAgent()
