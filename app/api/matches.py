"""
Matches and Allocation Plans API Endpoints.
Provides match listing, provider filtering, details, and privacy unmask handshake.
"""

from typing import Optional
from fastapi import APIRouter, HTTPException, Query
from app.db.mongo import get_collection, clean_mongo_doc

router = APIRouter(prefix="/api/v1/matches", tags=["Matches"])


@router.get("")
async def list_matches(
    provider_id: Optional[str] = Query(None, description="Filter matches by allocated provider ID"),
    limit: int = Query(50, ge=1, le=100)
):
    """Lists committed and pending humanitarian matches, with optional provider filtering."""
    matches_col = get_collection("matches")
    requests_col = get_collection("requests")

    query = {}
    if provider_id and provider_id != "ADMIN_ALL":
        clean_pid = provider_id.strip().upper()

        # Canonical Alias Map for 5-character GSM-7 mobile app codes
        ALIAS_MAP = {
            "NGO01": "NGO_TN_RED_CROSS",
            "TND01": "TNDRF_ARAKKONAM_CHENNAI",
            "HOS01": "HOSPITAL_CHENNAI_RGGGH",
            "CSR01": "CSR_TATA_SOUTH_HUB",
            "COI01": "COIMBATORE_GHAT_RESCUE",
            "RADM1": "NGO_TN_RED_CROSS"
        }

        target_ids = [clean_pid]
        if clean_pid in ALIAS_MAP:
            target_ids.append(ALIAS_MAP[clean_pid])
        if clean_pid[:5] in ALIAS_MAP:
            target_ids.append(ALIAS_MAP[clean_pid[:5]])
        
        prefix_3 = clean_pid[:3]

        query = {
            "$or": [
                {"allocations.provider_id": {"$in": target_ids}},
                {"allocations.provider_id": {"$regex": f"^{prefix_3}", "$options": "i"}},
                {"chosen_plan.allocations.provider_id": {"$in": target_ids}},
                {"chosen_plan.allocations.provider_id": {"$regex": f"^{prefix_3}", "$options": "i"}},
                {"selected_plan.allocations.provider_id": {"$in": target_ids}},
                {"selected_plan.allocations.provider_id": {"$regex": f"^{prefix_3}", "$options": "i"}},
                {"plan.allocations.provider_id": {"$in": target_ids}},
                {"provider_id": {"$in": target_ids}}
            ]
        }

    cursor = matches_col.find(query).sort("created_at", -1).limit(limit)
    items = await cursor.to_list(limit)

    # Attach request geo coordinates & details to each match for interactive mapping
    enriched_items = []
    for m in items:
        run_id = m.get("run_id")
        req_doc = await requests_col.find_one({"run_id": run_id}) if run_id else None
        m_copy = clean_mongo_doc(dict(m))

        # Extract primary allocated provider & items
        allocations = m_copy.get("allocations") or m_copy.get("chosen_plan", {}).get("allocations", [])
        if allocations:
            primary_alloc = allocations[0]
            m_copy["provider_id"] = primary_alloc.get("provider_id")
            m_copy["provider_name"] = primary_alloc.get("provider_name")
            m_copy["items"] = primary_alloc.get("items")
            m_copy["distance_km"] = primary_alloc.get("distance_km")
            m_copy["eta_hours"] = primary_alloc.get("eta_hours")

        if req_doc:
            clean_req = clean_mongo_doc(req_doc)
            m_copy["request_geo"] = clean_req.get("geo") or clean_req.get("loc")
            payload = clean_req.get("payload", {})
            m_copy["situation"] = payload.get("situation", {}).get("name", "Emergency Incident")
            m_copy["urgency"] = payload.get("urgency", {}).get("label", "Medium")
            m_copy["headcount"] = payload.get("headcount", {}).get("label", "1 person")

        enriched_items.append(m_copy)

    return {"count": len(enriched_items), "matches": enriched_items}


@router.get("/{match_id}")
async def get_match(match_id: str):
    """Retrieves single match record with associated request details."""
    matches_col = get_collection("matches")
    requests_col = get_collection("requests")

    doc = await matches_col.find_one({"$or": [{"match_id": match_id}, {"_id": match_id}]})
    if not doc:
        raise HTTPException(status_code=404, detail="Match not found")

    doc_copy = clean_mongo_doc(dict(doc))
    run_id = doc_copy.get("run_id")
    req_doc = await requests_col.find_one({"run_id": run_id}) if run_id else None

    allocations = doc_copy.get("allocations") or doc_copy.get("chosen_plan", {}).get("allocations", [])
    if allocations:
        primary_alloc = allocations[0]
        doc_copy["provider_id"] = primary_alloc.get("provider_id")
        doc_copy["provider_name"] = primary_alloc.get("provider_name")
        doc_copy["items"] = primary_alloc.get("items")
        doc_copy["distance_km"] = primary_alloc.get("distance_km")
        doc_copy["eta_hours"] = primary_alloc.get("eta_hours")

    if req_doc:
        clean_req = clean_mongo_doc(req_doc)
        doc_copy["request_geo"] = clean_req.get("geo") or clean_req.get("loc")
        doc_copy["payload"] = clean_req.get("payload", {})
        doc_copy["raw_frame"] = clean_req.get("raw_frame")
        payload = clean_req.get("payload", {})
        doc_copy["situation"] = payload.get("situation", {}).get("name", "Emergency Incident")
        doc_copy["urgency"] = payload.get("urgency", {}).get("label", "Medium")
        doc_copy["headcount"] = payload.get("headcount", {}).get("label", "1 person")

    return doc_copy


@router.post("/{match_id}/reveal")
async def reveal_match_privacy(match_id: str):
    """
    Mutual Handshake Unmasking.
    Reveals exact coordinates and direct contact channels once mutual commitment is confirmed.
    """
    matches_col = get_collection("matches")
    match = await matches_col.find_one({"match_id": match_id})
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")

    await matches_col.update_one({"match_id": match_id}, {"$set": {"masked": False, "revealed": True}})

    requests_col = get_collection("requests")
    req = await requests_col.find_one({"run_id": match.get("run_id")})

    return {
        "status": "unmasked",
        "match_id": match_id,
        "revealed": True,
        "exact_location": req.get("loc") if req else None,
        "raw_frame": req.get("raw_frame") if req else None
    }
