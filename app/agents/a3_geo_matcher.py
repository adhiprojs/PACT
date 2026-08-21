"""
Agent A3: Geospatial Candidate Matcher (Deterministic Python + MongoDB $geoNear).
Executes cascading spatial radius queries (10km -> 25km -> 60km -> 150km) on 'offers'.
"""

from typing import Dict, Any, List
from app.db.mongo import get_collection
from app.bus.eventbus import event_bus


class GeoMatcherAgent:
    name = "A3_GeoMatcher"

    async def find_candidates(
        self,
        target_coords: List[float],  # [lng, lat]
        needed_bitfield: int,
        run_id: str,
        excluded_providers: List[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Runs $geoNear aggregation with cascading radius rings to find suitable provider offers.
        """
        await event_bus.emit(
            "agent.entered",
            self.name,
            {"stage": "A3", "description": "Geospatial Candidate Matching ($geoNear)", "target_loc": target_coords},
            run_id=run_id
        )

        excluded = excluded_providers or []
        offers_col = get_collection("offers")
        radius_ladder_km = [15, 50, 150, 400, 1500]

        candidates = []
        matched_radius_km = 0

        for radius_km in radius_ladder_km:
            max_dist_meters = radius_km * 1000

            geo_query = {
                "near": {"type": "Point", "coordinates": target_coords},
                "distanceField": "distance_meters",
                "maxDistance": max_dist_meters,
                "spherical": True,
                "query": {
                    "status": "available",
                    "provider_id": {"$nin": excluded}
                }
            }

            pipeline = [
                {"$geoNear": geo_query},
                {"$limit": 8}
            ]

            # Emit tool call event
            await event_bus.emit(
                "agent.tool_call",
                self.name,
                {
                    "tool": "MongoDB.$geoNear",
                    "collection": "offers",
                    "radius_km": radius_km,
                    "pipeline": pipeline
                },
                run_id=run_id
            )

            cursor = offers_col.aggregate(pipeline)
            found = await cursor.to_list(10)

            # Filter providers who hold at least 1 requested resource
            relevant = []
            for doc in found:
                p_bitfield = doc.get("resource_bitfield", 0)
                if (p_bitfield & needed_bitfield) > 0 or needed_bitfield == 0:
                    doc["distance_km"] = round(doc.get("distance_meters", 0) / 1000.0, 2)
                    relevant.append(doc)

            if len(relevant) >= 2:
                candidates = relevant
                matched_radius_km = radius_km
                break
            elif relevant and not candidates:
                candidates = relevant
                matched_radius_km = radius_km

        # If radial ladder didn't find enough, fetch all active offers and sort by Haversine distance
        if not candidates:
            all_offers = await offers_col.find({"status": "available", "provider_id": {"$nin": excluded}}).to_list(50)
            if all_offers:
                from math import radians, cos, sin, asin, sqrt
                def haversine(lon1, lat1, lon2, lat2):
                    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
                    dlon = lon2 - lon1
                    dlat = lat2 - lat1
                    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
                    c = 2 * asin(sqrt(a))
                    return 6371 * c

                for doc in all_offers:
                    coords = doc.get("loc", {}).get("coordinates", [80.2707, 13.0827])
                    dist = haversine(target_coords[0], target_coords[1], coords[0], coords[1])
                    doc["distance_km"] = round(dist, 2)
                    doc["distance_meters"] = dist * 1000

                all_offers.sort(key=lambda x: x["distance_km"])
                candidates = all_offers[:4]
                matched_radius_km = int(candidates[-1]["distance_km"] + 10) if candidates else 50

        await event_bus.emit(
            "agent.completed",
            self.name,
            {
                "status": "candidates_found",
                "candidate_count": len(candidates),
                "search_center": {"coordinates": target_coords},
                "radius_km": matched_radius_km,
                "providers": [c.get("provider_id") for c in candidates]
            },
            run_id=run_id
        )

        return candidates


a3_geo_matcher = GeoMatcherAgent()
