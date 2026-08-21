"""
Pydantic Schemas and DB Models for PACT Platform.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
import time


class GeoLocation(BaseModel):
    type: str = "Point"
    coordinates: List[float] = Field(..., description="[longitude, latitude]")
    accuracy_m: Optional[int] = 5
    pack10: Optional[str] = None
    location_code: Optional[str] = None
    location_name: Optional[str] = None


class CitizenRequestCreate(BaseModel):
    uid: str
    seq: str = "001"
    raw_frame: Optional[str] = None
    situation_code: str = "3"
    headcount_code: str = "2"
    injury_code: str = "2"
    mobility_code: str = "2"
    urgency_code: str = "C"
    needs_keys: List[str] = ["water_kits", "medical_kits", "evac_transport"]
    vulnerability_bits: List[int] = []
    latitude: float = 23.25991
    longitude: float = 77.41263


class ProviderOfferCreate(BaseModel):
    provider_id: str
    organization_name: str
    org_type_code: str = "N"
    offered_resource_keys: List[str] = ["food_kits", "water_kits", "medical_kits", "evac_transport"]
    capacity_code: str = "4"
    radius_code: str = "3"
    eta_code: str = "2"
    availability_code: str = "A"
    latitude: float = 23.2650
    longitude: float = 77.4050
    stock: Dict[str, int] = Field(default_factory=dict)
    contact_phone: Optional[str] = "+919876543210"


class IngestWirePayload(BaseModel):
    text: Optional[str] = None
    body: Optional[str] = None
    Body: Optional[str] = None
    sender: Optional[str] = None
    From: Optional[str] = None
    from_: Optional[str] = Field(default=None, alias="from")
    transport: str = "http"


class AdminActionRequest(BaseModel):
    decision_id: str
    action: str = Field(..., description="approve | override | reject")
    override_option_id: Optional[str] = None
    pinned_provider_id: Optional[str] = None
    reject_reason: Optional[str] = None
    dispatcher_notes: Optional[str] = None


class DecisionOption(BaseModel):
    option_id: str  # fastest | max_coverage | least_depleting
    title: str
    description: str
    allocations: List[Dict[str, Any]]
    total_fulfilled: Dict[str, int]
    coverage_ratio: float
    max_eta_hours: float
    depletion_impact: str


class MatchRecord(BaseModel):
    match_id: str
    request_id: str
    run_id: str
    status: str = "committed"  # pending_admin, approved, committed, dispatched, delivered, rejected
    selected_option_id: str
    chosen_option: Dict[str, Any]
    triage_info: Dict[str, Any]
    created_at: float = Field(default_factory=time.time)
    masked: bool = True
    revealed: bool = False
    sms_ack_sent: Optional[str] = None
    provider_allocations: List[Dict[str, Any]] = Field(default_factory=list)
