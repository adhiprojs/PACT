"""
Groq LLM Client with Streaming, Concurrency Limiting, and Robust Deterministic Fallbacks.
Enforces Pydantic schema validation and stream token emission to the event bus.
"""

import asyncio
import json
import logging
from typing import Dict, Any, Optional, AsyncGenerator, Type
from pydantic import BaseModel
from app.config import GROQ_API_KEY, GROQ_MODEL
from app.bus.eventbus import event_bus

logger = logging.getLogger("pact.llm")

# Global semaphore to cap concurrent Groq calls
GROQ_SEMAPHORE = asyncio.Semaphore(6)


class GroqService:
    def __init__(self):
        self._client = None
        self._initialized = False

    def _get_client(self):
        if not self._initialized:
            if GROQ_API_KEY:
                try:
                    from groq import AsyncGroq
                    self._client = AsyncGroq(api_key=GROQ_API_KEY, timeout=8.0)
                    logger.info("Initialized Groq Async Client for model %s", GROQ_MODEL)
                except Exception as e:
                    logger.warning("Failed to initialize AsyncGroq (%s). Fallback engine active.", str(e))
            self._initialized = True
        return self._client

    async def stream_chat(
        self,
        system_prompt: str,
        user_prompt: str,
        agent_name: str,
        run_id: str,
        schema: Optional[Type[BaseModel]] = None,
        fallback_data: Optional[Dict[str, Any]] = None,
        json_mode: bool = True
    ) -> Dict[str, Any]:
        """
        Executes an LLM call with token streaming to the event bus.
        Falls back seamlessly to deterministic output if Groq is unavailable,
        times out, or schema validation fails.
        """
        client = self._get_client()

        if client is None:
            # Deterministic simulated token streaming
            logger.info("Groq API key not configured or client unavailable. Using simulated agent streaming for %s.", agent_name)
            return await self._simulate_stream(agent_name, run_id, fallback_data or {})

        async with GROQ_SEMAPHORE:
            try:
                await event_bus.emit("agent.thinking", agent_name, {"status": "contacting_groq", "model": GROQ_MODEL}, run_id=run_id)

                kwargs: Dict[str, Any] = {
                    "model": GROQ_MODEL,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    "temperature": 0.2,
                    "stream": True
                }
                if json_mode:
                    kwargs["response_format"] = {"type": "json_object"}

                response_stream = await asyncio.wait_for(
                    client.chat.completions.create(**kwargs),
                    timeout=8.0
                )

                accumulated_text = ""
                async for chunk in response_stream:
                    delta = chunk.choices[0].delta.content or ""
                    if delta:
                        accumulated_text += delta
                        await event_bus.emit(
                            "agent.token",
                            agent_name,
                            {"token": delta, "accumulated_len": len(accumulated_text)},
                            run_id=run_id
                        )

                # Parse JSON and validate against Pydantic schema
                if json_mode:
                    parsed_json = json.loads(accumulated_text)
                    if schema:
                        validated_obj = schema.model_validate(parsed_json)
                        return validated_obj.model_dump()
                    return parsed_json
                else:
                    return {"text": accumulated_text}

            except Exception as e:
                logger.warning("Groq API invocation failed for %s (%s). Engaging deterministic fallback.", agent_name, str(e))
                return await self._simulate_stream(agent_name, run_id, fallback_data or {})

    async def stream_text(
        self,
        system_prompt: str,
        user_prompt: str,
        agent_name: str,
        fallback_text: str = ""
    ) -> str:
        """Executes a streaming text completion for debate turns and dialogues."""
        client = self._get_client()
        if client is None:
            return fallback_text

        async with GROQ_SEMAPHORE:
            try:
                response = await asyncio.wait_for(
                    client.chat.completions.create(
                        model=GROQ_MODEL,
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_prompt}
                        ],
                        temperature=0.4,
                        max_tokens=250,
                        stream=False
                    ),
                    timeout=6.0
                )
                text = response.choices[0].message.content or ""
                return text.strip() if text.strip() else fallback_text
            except Exception as e:
                logger.warning("Groq text completion failed for %s (%s). Using fallback dialogue.", agent_name, str(e))
                return fallback_text

    async def _simulate_stream(self, agent_name: str, run_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Simulates rich tactical commander and doctor reasoning for visual dashboard vitality."""
        if agent_name == "A2_Triage":
            summary = (
                f"🩺 [Triage Doctor Clinical Assessment]: Patient group in immediate peril. "
                f"Assigned priority {data.get('priority_level', 'P1_CRITICAL')} (Risk Score {data.get('risk_score', 9.5)}/10). "
                f"Rapid extrication and ALS medical kits required before survival window closes."
            )
        elif agent_name == "A4_Advocates":
            summary = (
                f"💬 [Multi-Agency Tactical Conference]: "
                f"Relief commanders from Red Cross, TNDRF, and Corporate Logistics have coordinated routes. "
                f"Consensus: Closest units deploy first-response extraction, regional hubs supply bulk reserves."
            )
        elif agent_name == "A6_Arbiter":
            summary = (
                f"⚖️ [Strategic Arbiter Command Memo]: Selected optimal response plan. "
                f"Speed of initial medical contact prioritized over inventory conservation due to life-threat gravity."
            )
        elif agent_name == "A9_Narrator":
            summary = (
                f"📢 [Incident Command Dispatch]: Multi-agency rescue operation authorized. "
                f"Units dispatched to target coordinates. Cellular acknowledgement transmitted to victim."
            )
        else:
            summary = f"[{agent_name}] Operational assessment completed."

        words = summary.split()
        for word in words:
            await event_bus.emit("agent.token", agent_name, {"token": word + " "}, run_id=run_id)
            await asyncio.sleep(0.015)
        return data


groq_service = GroqService()
