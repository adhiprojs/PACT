"""
Q -> N Fan-out Converter.
Converts a citizen emergency request (Q) into discrete need items (N),
computing resource kit quantities based on headcount estimates and vulnerability weights.
"""

import math
from typing import Dict, Any, List
from app.codec.taxonomy import RESOURCES, RESOURCE_BY_KEY


def q_to_n_fanout(decoded_q: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Fans out a single decoded Q request into a list of normalized Need records.
    Each set need bit produces one need item with estimated quantity.
    """
    payload = decoded_q.get("payload", {})
    headcount_est = payload.get("people_estimate", 1)
    needed_resources = payload.get("needed_resources", [])
    urgency_label = payload.get("urgency", {}).get("label", "Medium")
    urgency_code = payload.get("urgency_code", "M")
    uid = decoded_q.get("uid", "CIT00")
    geo = decoded_q.get("geo", {})
    coords = geo.get("coordinates", [77.4126, 23.2599])

    # Vulnerability multipliers
    vulnerabilities = payload.get("vulnerabilities", [])
    has_infants = any(v.get("code") == "INF" for v in vulnerabilities)
    has_elderly = any(v.get("code") == "ELD" for v in vulnerabilities)

    need_items = []

    for res in needed_resources:
        key = res["key"]
        code = res["code"]
        ratio = res.get("per_person_ratio", 1.0)

        # Quantity calculation based on resource type
        if key == "food_kits":
            qty = max(1, math.ceil(headcount_est * ratio))
        elif key == "water_kits":
            qty = max(2, math.ceil(headcount_est * ratio))
        elif key == "medical_kits":
            qty = max(1, math.ceil(headcount_est * ratio))
        elif key == "tents":
            qty = max(1, math.ceil(headcount_est * ratio))
        elif key == "blankets":
            qty = max(1, math.ceil(headcount_est * ratio * (1.5 if has_elderly else 1.0)))
        elif key == "hygiene_kits":
            qty = max(1, math.ceil(headcount_est * ratio))
        elif key == "infant_kits":
            qty = max(1, 2 if has_infants else 1)
        elif key in ("rescue_team", "medical_team", "heavy_equipment", "power_kits"):
            qty = 1
        elif key == "evac_transport":
            qty = max(1, math.ceil(headcount_est / 4.0))
        else:
            qty = max(1, math.ceil(headcount_est * ratio))

        need_items.append({
            "need_id": f"ND_{uid}_{code}",
            "uid": uid,
            "organization_id": f"CITIZEN_{uid}",
            "resource_code": code,
            "resource_key": key,
            "resource_label": res["label"],
            "unit": res["unit"],
            "quantity": qty,
            "urgency": urgency_label.lower(),
            "urgency_code": urgency_code,
            "location_coordinates": coords,
            "source": "q_fanout",
            "people_count": headcount_est,
            "situation": payload.get("situation", {}).get("name", "Emergency")
        })

    return need_items
