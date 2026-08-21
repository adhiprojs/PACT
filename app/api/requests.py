"""
Requests API endpoints.
Provides emergency submission, status polling, and location streaming.
"""

import time
from typing import Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from app.db.mongo import get_collection, clean_mongo_doc
from app.bus.eventbus import event_bus

router = APIRouter(prefix="/api/v1", tags=["Requests"])


class NeedReportPayload(BaseModel):
    type: str = "need"
    organization_id: str
    location_code: str
    location_name: Optional[str] = ""
    location: Optional[str] = ""
    resource: str
    resource_code: str
    quantity: int = 1
    urgency: str = "medium"
    urgency_code: str = "M"
    notes: Optional[str] = ""
    source: Optional[str] = "android"
    latitude: Optional[float] = 13.0827
    longitude: Optional[float] = 80.2707


class LocationUpdatePayload(BaseModel):
    organization_id: str
    latitude: float
    longitude: float


@router.post("/needs")
async def post_need_report(payload: NeedReportPayload):
    """
    Direct internet API for Android Field App need submission.
    Triggers the multi-agent coordination pipeline.
    """
    lat = payload.latitude if (payload.latitude and payload.latitude != 0.0) else 13.0827
    lon = payload.longitude if (payload.longitude and payload.longitude != 0.0) else 80.2707

    from app.codec.requester_codec import encode_q_frame, encode_requester_payload
    from app.codec.taxonomy import RESOURCE_BY_KEY

    res_key = payload.resource.lower().replace(" ", "_")
    needs_bits = [res_key] if res_key in RESOURCE_BY_KEY else [0]
    
    urg_char = payload.urgency_code.upper().strip()[:1] if payload.urgency_code else "M"
    hc_code = "0" if payload.quantity <= 1 else ("1" if payload.quantity <= 5 else "2")

    payload_10 = encode_requester_payload(
        situation_code="0",
        headcount_code=hc_code,
        injury_code="0",
        mobility_code="0",
        urgency_code=urg_char,
        needs_keys_or_bits=needs_bits
    )

    seq = f"{int(time.time()*10)%900+100:03d}"
    uid = payload.organization_id.upper().strip()[:5]
    raw_frame = encode_q_frame(seq=seq, uid=uid, payload_str=payload_10, lat=lat, lon=lon)

    from app.agents.pipeline import pipeline
    run_result = await pipeline.run(
        raw_input=raw_frame,
        sender=payload.organization_id,
        transport="internet_api"
    )

    return {
        "status": "success",
        "need_id": run_result.get("run_id", f"RUN_{seq}"),
        "raw_frame": raw_frame,
        "pipeline_status": run_result.get("status", "completed")
    }


@router.post("/location/update")
async def update_location(payload: LocationUpdatePayload):
    """
    Ingests background GPS location from Android field workers.
    """
    org_id = payload.organization_id.upper().strip()
    lat = payload.latitude
    lon = payload.longitude

    providers_col = get_collection("providers")
    offers_col = get_collection("offers")

    loc_obj = {"type": "Point", "coordinates": [lon, lat]}
    await providers_col.update_one(
        {"provider_id": org_id},
        {"$set": {"loc": loc_obj, "last_seen": time.time()}},
        upsert=False
    )
    await offers_col.update_one(
        {"provider_id": org_id},
        {"$set": {"loc": loc_obj, "last_seen": time.time()}},
        upsert=False
    )
    return {"status": "ok", "organization_id": org_id, "lat": lat, "lon": lon}


@router.get("/requests")
async def list_requests(limit: int = Query(50, ge=1, le=200)):
    """Lists all incoming emergency requests."""
    requests_col = get_collection("requests")
    cursor = requests_col.find({}).sort("created_at", -1).limit(limit)
    items = await cursor.to_list(limit)
    return {"count": len(items), "requests": clean_mongo_doc(items)}


@router.get("/requests/by-org/{organization_id}")
async def get_requests_by_org(organization_id: str):
    """
    Returns live requests and approval status for a specific field organization or worker,
    including allocated helper provider details and cargo breakdown.
    """
    requests_col = get_collection("requests")
    matches_col = get_collection("matches")

    clean_org = organization_id.upper().strip()
    prefix = clean_org[:5]

    cursor = requests_col.find({
        "$or": [
            {"uid": {"$regex": f"^{prefix}", "$options": "i"}},
            {"sender": clean_org},
            {"parsed.uid": {"$regex": f"^{prefix}", "$options": "i"}}
        ]
    }).sort("created_at", -1).limit(25)
    
    docs = await cursor.to_list(25)

    result_list = []
    for d in docs:
        run_id = d.get("run_id")
        match = await matches_col.find_one({"run_id": run_id}) if run_id else None
        
        status = "pending"
        allocated_provider = None
        allocated_cargo = None
        eta_hours = None
        plan_id = None

        if match:
            status = match.get("status", "allocated")
            plan_id = match.get("match_id")
            allocs = match.get("allocations") or match.get("chosen_plan", {}).get("allocations", [])
            if allocs:
                first_alloc = allocs[0]
                allocated_provider = first_alloc.get("provider_name") or first_alloc.get("provider_id")
                items = first_alloc.get("items", {})
                if items:
                    allocated_cargo = ", ".join([f"{v} {k.replace('_', ' ').title()}" for k, v in items.items()])
                eta_hours = first_alloc.get("eta_hours")
        elif d.get("status"):
            status = d.get("status")

        payload = d.get("payload", {})
        coords = d.get("geo", {}).get("coordinates") or [80.2707, 13.0827]

        result_list.append({
            "id": d.get("uid") or d.get("run_id") or "REQ",
            "type": payload.get("situation", {}).get("name", "Emergency"),
            "resource": (payload.get("needed_resources", [{}])[0].get("label", "Aid Pack")),
            "quantity": payload.get("people_estimate", 1),
            "status": status,
            "allocated_provider": allocated_provider,
            "allocated_cargo": allocated_cargo,
            "eta_hours": eta_hours,
            "plan_id": plan_id,
            "latitude": coords[1] if len(coords) > 1 else None,
            "longitude": coords[0] if len(coords) > 0 else None,
            "created_at": str(d.get("created_at", ""))
        })

    return {"count": len(result_list), "requests": result_list}


@router.get("/requests/{req_id}")
async def get_request(req_id: str):
    """Retrieves a single request by ID or UID."""
    requests_col = get_collection("requests")
    doc = await requests_col.find_one({"$or": [{"_id": req_id}, {"run_id": req_id}, {"parsed.uid": req_id}]})
    if not doc:
        raise HTTPException(status_code=404, detail="Request not found")
    return clean_mongo_doc(doc)
