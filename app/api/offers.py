"""
Provider Offers and Depot Registration Endpoints.
Provides search, registration, and depot details.
"""

import time
from typing import Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from app.db.mongo import get_collection, clean_mongo_doc

router = APIRouter(prefix="/api/v1/offers", tags=["Offers"])


class OfferCreate(BaseModel):
    provider_id: str
    provider_name: str
    latitude: float
    longitude: float
    inventory: Dict[str, int]
    fleet_description: Optional[str] = "Standard rescue vehicles"
    contact_person: Optional[str] = "Logistics Officer"
    phone: Optional[str] = ""


@router.post("")
async def create_offer(payload: OfferCreate):
    """Registers a new provider relief depot with spatial coordinates."""
    offers_col = get_collection("offers")

    offer_doc = {
        "provider_id": payload.provider_id.upper(),
        "provider_name": payload.provider_name,
        "location_name": payload.provider_name,
        "loc": {
            "type": "Point",
            "coordinates": [payload.longitude, payload.latitude]
        },
        "inventory": payload.inventory,
        "fleet_description": payload.fleet_description,
        "contact_person": payload.contact_person,
        "phone": payload.phone,
        "status": "available",
        "created_at": time.time()
    }

    await offers_col.update_one(
        {"provider_id": payload.provider_id.upper()},
        {"$set": offer_doc},
        upsert=True
    )

    return {"status": "registered", "offer": clean_mongo_doc(offer_doc)}


@router.get("")
async def list_offers(limit: int = Query(50, ge=1, le=100)):
    """Lists all active provider offers."""
    offers_col = get_collection("offers")
    cursor = offers_col.find({}).sort("created_at", -1).limit(limit)
    items = await cursor.to_list(limit)
    return {"count": len(items), "offers": clean_mongo_doc(items)}


@router.get("/{provider_id}")
async def get_provider_profile(provider_id: str):
    """Gets details, inventory, and location for a specific provider depot."""
    offers_col = get_collection("offers")
    depot = await offers_col.find_one({"provider_id": provider_id})
    if not depot:
        raise HTTPException(status_code=404, detail="Provider depot not found")
    return clean_mongo_doc(depot)
