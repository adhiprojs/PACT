"""
Taxonomy and bitfield definitions for PACT Base-36 Codec and SMS Protocol.
Governs requester situations, headcount estimations, injuries, mobility,
12-bit resources bitfield, 5-bit vulnerability bitfield, and provider metadata.
"""

from typing import Dict, List, Any

# Situation Types (pos 1 of Requester Frame)
SITUATIONS: Dict[str, Dict[str, Any]] = {
    "0": {"code": "GEN", "name": "General Emergency", "icon": "⚠️", "severity_base": 5},
    "1": {"code": "FLD", "name": "Flood / Rising Water", "icon": "🌊", "severity_base": 7},
    "2": {"code": "EQK", "name": "Earthquake / Tremor", "icon": "🏚️", "severity_base": 8},
    "3": {"code": "COL", "name": "Building Collapse", "icon": "🏢", "severity_base": 9},
    "4": {"code": "FIR", "name": "Fire / Explosion", "icon": "🔥", "severity_base": 8},
    "5": {"code": "LND", "name": "Landslide / Mudslide", "icon": "⛰️", "severity_base": 7},
    "6": {"code": "CYC", "name": "Cyclone / Hurricane", "icon": "🌀", "severity_base": 8},
    "7": {"code": "MED", "name": "Medical Outbreak / Epidemic", "icon": "🏥", "severity_base": 7},
    "8": {"code": "PWR", "name": "Severe Infrastructure Outage", "icon": "🔌", "severity_base": 5},
    "9": {"code": "CHM", "name": "Chemical / Gas Leak", "icon": "☣️", "severity_base": 9},
    "A": {"code": "TSU", "name": "Tsunami", "icon": "🌊", "severity_base": 10},
    "B": {"code": "WNT", "name": "Severe Winter Storm / Cold", "icon": "❄️", "severity_base": 6},
}

# Headcount Buckets (pos 2 of Requester Frame)
HEADCOUNTS: Dict[str, Dict[str, Any]] = {
    "0": {"label": "1 person", "min": 1, "max": 1, "est": 1},
    "1": {"label": "2 people", "min": 2, "max": 2, "est": 2},
    "2": {"label": "3-4 people", "min": 3, "max": 4, "est": 3},
    "3": {"label": "5-8 people", "min": 5, "max": 8, "est": 6},
    "4": {"label": "9-15 people", "min": 9, "max": 15, "est": 12},
    "5": {"label": "16-30 people", "min": 16, "max": 30, "est": 23},
    "6": {"label": "31-50 people", "min": 31, "max": 50, "est": 40},
    "7": {"label": "51-100 people", "min": 51, "max": 100, "est": 75},
    "8": {"label": "101-200 people", "min": 101, "max": 200, "est": 150},
    "9": {"label": "201-500 people", "min": 201, "max": 500, "est": 350},
    "A": {"label": "500+ people", "min": 500, "max": 2000, "est": 600},
}

# Injury Severity (pos 3 of Requester Frame)
INJURIES: Dict[str, Dict[str, Any]] = {
    "0": {"code": "NONE", "label": "No Injuries / Uninjured", "score": 0},
    "1": {"code": "MIN", "label": "Minor / Ambulatory", "score": 2},
    "2": {"code": "SER", "label": "Serious / Non-ambulatory", "score": 6},
    "3": {"code": "CRT", "label": "Critical / Life-Threatening", "score": 9},
    "4": {"code": "FAT", "label": "Fatalities Present", "score": 10},
}

# Mobility / Entrapment (pos 4 of Requester Frame)
MOBILITY: Dict[str, Dict[str, Any]] = {
    "0": {"code": "MOB", "label": "Fully Mobile", "score": 0},
    "1": {"code": "IMP", "label": "Impeded / Blocked Routes", "score": 3},
    "2": {"code": "TRP", "label": "Trapped in Structure / Rubble", "score": 8},
    "3": {"code": "WTR", "label": "Waterbound / Isolated", "score": 7},
    "4": {"code": "ROF", "label": "Rooftop / Elevated", "score": 6},
    "5": {"code": "BSM", "label": "Underground / Basement", "score": 8},
}

# Urgency Codes (pos 5 of Requester Frame)
URGENCY: Dict[str, Dict[str, Any]] = {
    "L": {"label": "Low", "rank": 1, "color": "#10B981"},
    "M": {"label": "Medium", "rank": 2, "color": "#F59E0B"},
    "H": {"label": "High", "rank": 3, "color": "#F97316"},
    "C": {"label": "Critical", "rank": 4, "color": "#EF4444"},
}

# 12-Bit Resources Taxonomy (Shared across Needs and Provider Inventory)
RESOURCES: List[Dict[str, Any]] = [
    {"bit": 0, "code": "F", "key": "food_kits", "label": "Food Kits", "unit": "kits", "per_person_ratio": 1.0},
    {"bit": 1, "code": "W", "key": "water_kits", "label": "Water Kits", "unit": "liters/kits", "per_person_ratio": 2.0},
    {"bit": 2, "code": "M", "key": "medical_kits", "label": "Medical Kits", "unit": "kits", "per_person_ratio": 0.5},
    {"bit": 3, "code": "T", "key": "tents", "label": "Tents / Shelter", "unit": "units", "per_person_ratio": 0.25},
    {"bit": 4, "code": "B", "key": "blankets", "label": "Blankets / Warmth", "unit": "units", "per_person_ratio": 1.0},
    {"bit": 5, "code": "H", "key": "hygiene_kits", "label": "Hygiene Kits", "unit": "kits", "per_person_ratio": 0.5},
    {"bit": 6, "code": "X", "key": "rescue_team", "label": "Search & Rescue Squad", "unit": "teams", "per_person_ratio": 0.1},
    {"bit": 7, "code": "V", "key": "evac_transport", "label": "Evacuation Transport", "unit": "vehicles", "per_person_ratio": 0.2},
    {"bit": 8, "code": "P", "key": "power_kits", "label": "Power / Generator Kits", "unit": "generators", "per_person_ratio": 0.05},
    {"bit": 9, "code": "I", "key": "infant_kits", "label": "Infant & Baby Kits", "unit": "kits", "per_person_ratio": 0.3},
    {"bit": 10, "code": "D", "key": "medical_team", "label": "Doctor / Medical Field Team", "unit": "teams", "per_person_ratio": 0.1},
    {"bit": 11, "code": "E", "key": "heavy_equipment", "label": "Heavy Clearance Equipment", "unit": "machines", "per_person_ratio": 0.05},
]

RESOURCE_BY_CODE = {r["code"]: r for r in RESOURCES}
RESOURCE_BY_KEY = {r["key"]: r for r in RESOURCES}
RESOURCE_BY_BIT = {r["bit"]: r for r in RESOURCES}

# 5-Bit Vulnerability Bitfield (pos 9 of Requester Frame)
VULNERABILITIES: List[Dict[str, Any]] = [
    {"bit": 0, "code": "INF", "label": "Infants / Children under 5", "weight": 2.0},
    {"bit": 1, "code": "ELD", "label": "Elderly (65+)", "weight": 1.5},
    {"bit": 2, "code": "PRG", "label": "Pregnant Women", "weight": 2.0},
    {"bit": 3, "code": "DIS", "label": "Disabled / Mobility Impaired", "weight": 1.5},
    {"bit": 4, "code": "CHR", "label": "Chronic Condition / Dialysis / O2", "weight": 2.5},
]

# Provider Metadata Lookups
PROVIDER_ORG_TYPES: Dict[str, Dict[str, Any]] = {
    "N": {"code": "NGO", "label": "Non-Governmental Org (NGO)", "fleet_type": "all-terrain vans"},
    "G": {"code": "GOV", "label": "Government Agency / NDRF", "fleet_type": "heavy rescue trucks"},
    "C": {"code": "CSR", "label": "Corporate CSR Fleet", "fleet_type": "commercial logistics"},
    "V": {"code": "VOL", "label": "Local Community Volunteers", "fleet_type": "4x4 light vehicles"},
    "M": {"code": "MIL", "label": "Military / Civil Defense", "fleet_type": "amphibious / helicopters"},
    "P": {"code": "HOS", "label": "Private Hospital / Clinic", "fleet_type": "ambulances"},
    "I": {"code": "INT", "label": "International Aid Agency", "fleet_type": "container transports"},
    "R": {"code": "RED", "label": "Red Cross / Red Crescent", "fleet_type": "mobile emergency units"},
}

CAPACITY_BUCKETS: Dict[str, int] = {
    "0": 10,
    "1": 50,
    "2": 100,
    "3": 250,
    "4": 500,
    "5": 1000,
    "6": 2500,
    "7": 5000,
    "8": 10000,
}

RADIUS_BUCKETS: Dict[str, int] = {
    "0": 5,
    "1": 10,
    "2": 25,
    "3": 50,
    "4": 100,
    "5": 150,
    "6": 250,
    "7": 500,
}

ETA_BUCKETS: Dict[str, float] = {
    "0": 0.5,
    "1": 1.0,
    "2": 2.0,
    "3": 4.0,
    "4": 8.0,
    "5": 12.0,
    "6": 24.0,
    "7": 48.0,
}

PROVIDER_AVAILABILITY: Dict[str, str] = {
    "A": "available",
    "L": "limited",
    "U": "unavailable",
}

STATUS_CODES: Dict[str, str] = {
    "0": "assigned",
    "1": "dispatched",
    "2": "in_transit",
    "3": "delivered",
    "4": "blocked",
    "5": "cancelled",
    "6": "self_resolved",
    "7": "still_waiting",
}
