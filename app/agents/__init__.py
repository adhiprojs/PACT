"""
PACT Multi-Agent System Package.
Exports all reasoning agents (A0 through A11) and the master pipeline.
"""

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
from app.agents.pipeline import pipeline, PipelineOrchestrator

__all__ = [
    "a0_intake",
    "a1_dedupe",
    "a2_triage",
    "a3_geo_matcher",
    "a4_advocates",
    "a5_solver",
    "a6_arbiter",
    "a7_redactor",
    "a8_admin_gate",
    "a9_narrator",
    "a10_verify",
    "a11_replan",
    "pipeline",
    "PipelineOrchestrator",
]
