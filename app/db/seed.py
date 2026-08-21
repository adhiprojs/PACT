"""
Seed Data for Disaster Coordination Simulation.
Initializes realistic depots, relief providers, stockpiles, and active crisis zones.
"""

import time
import logging
from app.db.mongo import get_collection
from app.codec.pack10 import encode_pack10
from app.codec.taxonomy import RESOURCE_BY_KEY

logger = logging.getLogger("pact.seed")

SEED_PROVIDERS = [
    {
        "provider_id": "NGO_ALPHA",
        "name": "Red Cross Emergency Response Corps",
        "org_type": "NGO",
        "org_type_code": "R",
        "contact_phone": "+919811122233",
        "contact_person": "Capt. Meera Sharma",
        "location_name": "Region A Depot (North Camp)",
        "loc": {"type": "Point", "coordinates": [77.4050, 23.2650]},  # [lng, lat]
        "pack10": encode_pack10(23.2650, 77.4050),
        "radius_km": 30,
        "eta_hours": 0.5,
        "status": "available",
        "inventory": {
            "food_kits": 650,
            "water_kits": 1200,
            "medical_kits": 250,
            "blankets": 400,
            "hygiene_kits": 300,
            "evac_transport": 5,
        },
        "fleet_description": "5x 4WD All-Terrain Logistics Vans",
        "created_at": time.time(),
    },
    {
        "provider_id": "CSR_BETA",
        "name": "Tata / Corporate Disaster Relief Hub",
        "org_type": "CSR",
        "org_type_code": "C",
        "contact_phone": "+919822233344",
        "contact_person": "Rajesh Varma (Logistics Head)",
        "location_name": "District South Logistics Park",
        "loc": {"type": "Point", "coordinates": [77.4400, 23.2200]},
        "pack10": encode_pack10(23.2200, 77.4400),
        "radius_km": 60,
        "eta_hours": 2.0,
        "status": "available",
        "inventory": {
            "food_kits": 3500,
            "water_kits": 7000,
            "tents": 300,
            "blankets": 1200,
            "power_kits": 25,
            "evac_transport": 12,
        },
        "fleet_description": "12x Heavy Commercial Cargo Trucks",
        "created_at": time.time(),
    },
    {
        "provider_id": "NDRF_SQUAD_07",
        "name": "NDRF National Rescue Battalion 07",
        "org_type": "GOV",
        "org_type_code": "G",
        "contact_phone": "+919833344455",
        "contact_person": "Commandant A. K. Roy",
        "location_name": "District North Airbase & Barracks",
        "loc": {"type": "Point", "coordinates": [77.3900, 23.2800]},
        "pack10": encode_pack10(23.2800, 77.3900),
        "radius_km": 120,
        "eta_hours": 1.0,
        "status": "available",
        "inventory": {
            "rescue_team": 8,
            "evac_transport": 15,
            "medical_team": 4,
            "heavy_equipment": 6,
            "power_kits": 10,
        },
        "fleet_description": "Amphibious Vehicles, Cutters & Lifeboats",
        "created_at": time.time(),
    },
    {
        "provider_id": "HOSPITAL_APEX",
        "name": "Apex Trauma & Medical Rapid Response",
        "org_type": "HOS",
        "org_type_code": "P",
        "contact_phone": "+919844455566",
        "contact_person": "Dr. Sunita Patel (Triage Chief)",
        "location_name": "Central Medical Enclave",
        "loc": {"type": "Point", "coordinates": [77.4180, 23.2550]},
        "pack10": encode_pack10(23.2550, 77.4180),
        "radius_km": 25,
        "eta_hours": 0.5,
        "status": "available",
        "inventory": {
            "medical_kits": 800,
            "infant_kits": 250,
            "medical_team": 6,
            "evac_transport": 8,
            "hygiene_kits": 500,
        },
        "fleet_description": "8x Advanced Life Support Ambulances",
        "created_at": time.time(),
    },
    {
        "provider_id": "VOLUNTEER_CORPS",
        "name": "Bhopal Citizen Volunteer Relief Network",
        "org_type": "VOL",
        "org_type_code": "V",
        "contact_phone": "+919855566677",
        "contact_person": "Vikram Sen",
        "location_name": "Region B Community Center",
        "loc": {"type": "Point", "coordinates": [77.4300, 23.2350]},
        "pack10": encode_pack10(23.2350, 77.4300),
        "radius_km": 20,
        "eta_hours": 1.0,
        "status": "available",
        "inventory": {
            "food_kits": 400,
            "water_kits": 900,
            "blankets": 600,
            "hygiene_kits": 350,
            "infant_kits": 80,
        },
        "fleet_description": "Community Vans and Two-Wheelers",
        "created_at": time.time(),
    },
    # --- TAMIL NADU REGIONAL RELIEF DEPOTS ---
    {
        "provider_id": "HOSPITAL_CHENNAI_RGGGH",
        "name": "Rajiv Gandhi / Apollo Trauma Medical Center",
        "org_type": "HOS",
        "org_type_code": "P",
        "contact_phone": "+919444111222",
        "contact_person": "Dr. K. Senthil Nathan (Trauma Chief)",
        "location_name": "Chennai Central Medical Hub",
        "loc": {"type": "Point", "coordinates": [80.2707, 13.0827]},
        "pack10": encode_pack10(13.0827, 80.2707),
        "radius_km": 40,
        "eta_hours": 0.5,
        "status": "available",
        "inventory": {
            "medical_kits": 1200,
            "infant_kits": 400,
            "medical_team": 10,
            "evac_transport": 12,
            "hygiene_kits": 800,
        },
        "fleet_description": "12x Advanced Cardiac ALS Ambulances",
        "created_at": time.time(),
    },
    {
        "provider_id": "NGO_TN_RED_CROSS",
        "name": "Red Cross Tamil Nadu Disaster Relief",
        "org_type": "NGO",
        "org_type_code": "R",
        "contact_phone": "+919444222333",
        "contact_person": "S. Anuradha (State Coordinator)",
        "location_name": "Egmore Emergency Depot (Chennai)",
        "loc": {"type": "Point", "coordinates": [80.2609, 13.0732]},
        "pack10": encode_pack10(13.0732, 80.2609),
        "radius_km": 50,
        "eta_hours": 0.5,
        "status": "available",
        "inventory": {
            "food_kits": 2500,
            "water_kits": 5000,
            "blankets": 1800,
            "tents": 250,
            "hygiene_kits": 1000,
            "evac_transport": 8,
        },
        "fleet_description": "8x Heavy Relief Cargo Vans",
        "created_at": time.time(),
    },
    {
        "provider_id": "TNDRF_ARAKKONAM_CHENNAI",
        "name": "Tamil Nadu Disaster Response Force (TNDRF)",
        "org_type": "GOV",
        "org_type_code": "G",
        "contact_phone": "+919444333444",
        "contact_person": "Commander M. Karunakaran",
        "location_name": "TNDRF Coastal & Flood Rescue Base",
        "loc": {"type": "Point", "coordinates": [80.2200, 13.0400]},
        "pack10": encode_pack10(13.0400, 80.2200),
        "radius_km": 150,
        "eta_hours": 1.0,
        "status": "available",
        "inventory": {
            "rescue_team": 15,
            "evac_transport": 25,
            "heavy_equipment": 10,
            "power_kits": 20,
            "medical_team": 6,
        },
        "fleet_description": "Inflatable Speedboats, Amphibious Vehicles & Cutters",
        "created_at": time.time(),
    },
    {
        "provider_id": "CSR_TATA_SOUTH_HUB",
        "name": "Tata / CSR Southern Disaster Logistics Hub",
        "org_type": "CSR",
        "org_type_code": "C",
        "contact_phone": "+919444555666",
        "contact_person": "V. Ramachandran (Supply Chain Head)",
        "location_name": "Guindy Industrial Warehouse (Chennai)",
        "loc": {"type": "Point", "coordinates": [80.2025, 13.0067]},
        "pack10": encode_pack10(13.0067, 80.2025),
        "radius_km": 80,
        "eta_hours": 1.5,
        "status": "available",
        "inventory": {
            "food_kits": 8000,
            "water_kits": 15000,
            "tents": 800,
            "blankets": 4000,
            "power_kits": 50,
            "evac_transport": 20,
        },
        "fleet_description": "20x Multi-Axle Freight Container Trucks",
        "created_at": time.time(),
    },
    {
        "provider_id": "COIMBATORE_GHAT_RESCUE",
        "name": "Coimbatore & Nilgiris Disaster Rescue Unit",
        "org_type": "NGO",
        "org_type_code": "R",
        "contact_phone": "+919444777888",
        "contact_person": "P. Selvakumar",
        "location_name": "Coimbatore Logistics Hub",
        "loc": {"type": "Point", "coordinates": [76.9558, 11.0168]},
        "pack10": encode_pack10(11.0168, 76.9558),
        "radius_km": 100,
        "eta_hours": 1.0,
        "status": "available",
        "inventory": {
            "food_kits": 1500,
            "water_kits": 3000,
            "tents": 200,
            "blankets": 1000,
            "medical_kits": 500,
            "rescue_team": 6,
        },
        "fleet_description": "Hill-Climb 4x4 Mountain Rescue Vehicles",
        "created_at": time.time(),
    },
    {
        "provider_id": "MADURAI_TRAUMA_HUB",
        "name": "Madurai South Emergency Response Base",
        "org_type": "HOS",
        "org_type_code": "P",
        "contact_phone": "+919444888999",
        "contact_person": "Dr. R. Alagappan",
        "location_name": "Madurai Medical Logistics Center",
        "loc": {"type": "Point", "coordinates": [78.1198, 9.9252]},
        "pack10": encode_pack10(9.9252, 78.1198),
        "radius_km": 90,
        "eta_hours": 1.0,
        "status": "available",
        "inventory": {
            "medical_kits": 900,
            "food_kits": 1200,
            "water_kits": 2500,
            "medical_team": 5,
            "evac_transport": 6,
        },
        "fleet_description": "6x Field Ambulances & Mobile Clinics",
        "created_at": time.time(),
    }
]


def calculate_bitfield_from_inventory(inventory: dict) -> int:
    """Computes the 12-bit integer matching available inventory keys."""
    val = 0
    for key, qty in inventory.items():
        if qty > 0 and key in RESOURCE_BY_KEY:
            val |= (1 << RESOURCE_BY_KEY[key]["bit"])
    return val


async def seed_database(force: bool = False):
    """Populates the database with initial provider depots and inventory."""
    providers_col = get_collection("providers")
    offers_col = get_collection("offers")

    count = await providers_col.count_documents({})
    if count > 0 and not force:
        logger.info("Database already seeded with %d providers.", count)
        return

    await providers_col.delete_many({})
    await offers_col.delete_many({})

    for p in SEED_PROVIDERS:
        await providers_col.insert_one(p)

        bitfield = calculate_bitfield_from_inventory(p["inventory"])
        offer_doc = {
            "offer_id": f"OFFER_{p['provider_id']}",
            "provider_id": p["provider_id"],
            "provider_name": p["name"],
            "name": p["name"],
            "org_type": p.get("org_type", "NGO"),
            "org_type_code": p["org_type_code"],
            "loc": p["loc"],
            "pack10": p["pack10"],
            "location_name": p["location_name"],
            "resource_bitfield": bitfield,
            "inventory": p["inventory"],
            "fleet_description": p.get("fleet_description", "Emergency Fleet"),
            "radius_km": p["radius_km"],
            "eta_hours": p["eta_hours"],
            "status": "available",
            "contact_phone": p["contact_phone"],
            "contact_person": p["contact_person"],
            "created_at": time.time(),
        }
        await offers_col.insert_one(offer_doc)

    logger.info("Successfully seeded %d provider relief depots.", len(SEED_PROVIDERS))
