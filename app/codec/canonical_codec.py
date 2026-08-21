"""
Comprehensive SMS Codec for all PACT and legacy message types.
Supports: Q, G, N, R, A, S, C, X, M, P, RT, E and legacy demo formats.
"""

from typing import Dict, Any, Optional, List
import re
from app.codec.checksum import calculate_xor_checksum, verify_checksum
from app.codec.pack10 import decode_pack10, encode_pack10
from app.codec.requester_codec import decode_q_frame
from app.codec.provider_codec import decode_g_frame
from app.codec.taxonomy import RESOURCE_BY_CODE, URGENCY, STATUS_CODES, PROVIDER_AVAILABILITY

# Location lookup table for short location codes
KNOWN_LOCATIONS: Dict[str, Dict[str, Any]] = {
    "RA": {"name": "Region A (North Camp)", "lat": 23.2599, "lon": 77.4126},
    "RB": {"name": "Region B (South Relief Zone)", "lat": 23.2300, "lon": 77.4350},
    "RC": {"name": "Region C (East Flood Plain)", "lat": 23.2800, "lon": 77.3900},
    "D1": {"name": "District North (Old City)", "lat": 23.2650, "lon": 77.4050},
    "D2": {"name": "District South (Industrial Zone)", "lat": 23.2100, "lon": 77.4500},
}

# Mapping common alias names to short resource codes
RESOURCE_ALIASES: Dict[str, str] = {
    "F": "F", "FOOD": "F", "FOOD_KITS": "F",
    "W": "W", "WATER": "W", "WATER_KITS": "W",
    "M": "M", "MEDICAL": "M", "MEDICINE": "M", "MEDICAL_KITS": "M",
    "T": "T", "TENTS": "T", "TENT": "T",
    "B": "B", "BLANKETS": "B", "BLANKET": "B",
    "H": "H", "HYGIENE": "H", "HYGIENE_KITS": "H",
    "X": "X", "RESCUE": "X", "RESCUE_TEAM": "X",
    "V": "V", "EVAC": "V", "EVAC_TRANSPORT": "V",
    "P": "P", "POWER": "P", "GENERATOR": "P", "POWER_KITS": "P",
    "I": "I", "INFANT": "I", "BABY": "I", "INFANT_KITS": "I",
    "D": "D", "DOCTOR": "D", "MEDICAL_TEAM": "D",
    "E": "E", "EQUIPMENT": "E", "HEAVY_EQUIPMENT": "E",
}


def parse_location(loc_str: str) -> Dict[str, Any]:
    """
    Parses location field which can be:
    1. Known code e.g. "RA"
    2. PACK10 string e.g. "6QR6VFBQ33"
    3. Decimal coordinates e.g. "23.2599,77.4126"
    4. Geohash e.g. "GEO:te7u2f"
    5. Hex coords e.g. "HX:0DDBF6D82E22A1B0"
    """
    s = loc_str.strip()
    if s.upper() in KNOWN_LOCATIONS:
        info = KNOWN_LOCATIONS[s.upper()]
        return {
            "location_code": s.upper(),
            "location_name": info["name"],
            "latitude": info["lat"],
            "longitude": info["lon"],
            "coordinates": [info["lon"], info["lat"]],
            "type": "code"
        }

    if "," in s:
        parts = s.split(",")
        try:
            lat = float(parts[0].strip())
            lon = float(parts[1].strip())
            return {
                "location_code": None,
                "location_name": f"Coord ({lat:.4f}, {lon:.4f})",
                "latitude": lat,
                "longitude": lon,
                "coordinates": [lon, lat],
                "type": "coordinates"
            }
        except ValueError:
            pass

    if len(s) == 10 and re.match(r"^[0-9A-Za-z]{10}$", s):
        try:
            lat, lon, acc = decode_pack10(s)
            return {
                "location_code": s.upper(),
                "location_name": f"PACK10 ({lat:.5f}, {lon:.5f})",
                "latitude": lat,
                "longitude": lon,
                "accuracy_m": acc,
                "coordinates": [lon, lat],
                "type": "pack10"
            }
        except Exception:
            pass

    if s.startswith("GEO:"):
        return {
            "location_code": s,
            "location_name": f"Geohash {s}",
            "latitude": 23.2599,
            "longitude": 77.4126,
            "coordinates": [77.4126, 23.2599],
            "type": "geohash"
        }

    # Default fallback
    return {
        "location_code": s,
        "location_name": s,
        "latitude": 23.2599,
        "longitude": 77.4126,
        "coordinates": [77.4126, 23.2599],
        "type": "unresolved"
    }


def parse_sms(raw_text: str) -> Dict[str, Any]:
    """
    Main parser for any incoming SMS text.
    Handles Q, G, N, R, A, S, C, X, M, P, RT, E, and legacy demo strings.
    """
    trimmed = raw_text.strip()
    if not trimmed:
        raise ValueError("Empty SMS string")

    # Check for legacy text delivery confirmation: "DELIVERED RegionA food 200"
    if trimmed.upper().startswith("DELIVERED "):
        parts = trimmed.split()
        loc = parts[1] if len(parts) > 1 else "RA"
        res = parts[2] if len(parts) > 2 else "food"
        qty = int(parts[3]) if len(parts) > 3 and parts[3].isdigit() else 100
        res_code = RESOURCE_ALIASES.get(res.upper(), "F")
        return {
            "type": "status",
            "message_type": "S",
            "seq": "000",
            "location_code": loc,
            "resource": RESOURCE_BY_CODE.get(res_code, {}).get("key", "food_kits"),
            "quantity": qty,
            "status": "delivered",
            "status_code": "3",
            "source": "sms",
            "legacy": True
        }

    parts = [p.strip() for p in trimmed.split("|")]
    type_code = parts[0].upper()

    # 1. Citizen Help Request 'Q'
    if type_code == "Q":
        return decode_q_frame(trimmed)

    # 2. Provider Offer 'G'
    if type_code == "G":
        return decode_g_frame(trimmed)

    # 3. Need Request 'N'
    # Canonical: N|SEQ|ORG|LOC|RESOURCE|QTY|URGENCY|CRC
    # Legacy: N|ORG|LOC|RESOURCE|QTY|URGENCY
    if type_code == "N":
        if len(parts) >= 8:
            seq, org, loc_raw, res_raw, qty_raw, urg_raw, crc = parts[1:8]
            crc_valid = verify_checksum(trimmed)
            loc = parse_location(loc_raw)
            res_code = RESOURCE_ALIASES.get(res_raw.upper(), res_raw)
            res_info = RESOURCE_BY_CODE.get(res_code, {"key": res_raw.lower()})
            return {
                "type": "need",
                "message_type": "N",
                "seq": seq,
                "organization_id": org,
                "location": loc,
                "location_code": loc.get("location_code"),
                "location_name": loc.get("location_name"),
                "resource_code": res_code,
                "resource": res_info.get("key"),
                "quantity": int(qty_raw) if qty_raw.isdigit() else 0,
                "urgency_code": urg_raw.upper(),
                "urgency": URGENCY.get(urg_raw.upper(), {}).get("label", "Medium").lower(),
                "checksum": crc,
                "checksum_valid": crc_valid,
                "source": "sms",
                "geo": {"coordinates": loc.get("coordinates", [77.4126, 23.2599])}
            }
        elif len(parts) >= 6:  # Legacy format
            org, loc_raw, res_raw, qty_raw, urg_raw = parts[1:6]
            loc = parse_location(loc_raw)
            res_code = RESOURCE_ALIASES.get(res_raw.upper(), res_raw)
            res_info = RESOURCE_BY_CODE.get(res_code, {"key": res_raw.lower()})
            return {
                "type": "need",
                "message_type": "N",
                "seq": "000",
                "organization_id": org,
                "location": loc,
                "location_code": loc.get("location_code"),
                "location_name": loc.get("location_name"),
                "resource_code": res_code,
                "resource": res_info.get("key"),
                "quantity": int(qty_raw) if qty_raw.isdigit() else 0,
                "urgency_code": urg_raw.upper(),
                "urgency": URGENCY.get(urg_raw.upper(), {}).get("label", "Medium").lower(),
                "checksum": None,
                "checksum_valid": True,
                "legacy": True,
                "source": "sms",
                "geo": {"coordinates": loc.get("coordinates", [77.4126, 23.2599])}
            }

    # 4. Resource Availability 'R'
    # Canonical: R|SEQ|ORG|LOC|RESOURCE|QTY|STATUS|CRC
    # Legacy: R|ORG|RESOURCE|QTY|STATUS
    if type_code == "R":
        if len(parts) >= 8:
            seq, org, loc_raw, res_raw, qty_raw, status_raw, crc = parts[1:8]
            crc_valid = verify_checksum(trimmed)
            loc = parse_location(loc_raw)
            res_code = RESOURCE_ALIASES.get(res_raw.upper(), res_raw)
            res_info = RESOURCE_BY_CODE.get(res_code, {"key": res_raw.lower()})
            return {
                "type": "resource",
                "message_type": "R",
                "seq": seq,
                "organization_id": org,
                "location": loc,
                "location_code": loc.get("location_code"),
                "location_name": loc.get("location_name"),
                "resource_code": res_code,
                "resource": res_info.get("key"),
                "quantity": int(qty_raw) if qty_raw.isdigit() else 0,
                "status_code": status_raw.upper(),
                "status": PROVIDER_AVAILABILITY.get(status_raw.upper(), "available"),
                "checksum": crc,
                "checksum_valid": crc_valid,
                "source": "sms",
                "geo": {"coordinates": loc.get("coordinates", [77.4126, 23.2599])}
            }
        elif len(parts) >= 5:  # Legacy format
            org, res_raw, qty_raw, status_raw = parts[1:5]
            loc = parse_location("RA")
            res_code = RESOURCE_ALIASES.get(res_raw.upper(), res_raw)
            res_info = RESOURCE_BY_CODE.get(res_code, {"key": res_raw.lower()})
            return {
                "type": "resource",
                "message_type": "R",
                "seq": "000",
                "organization_id": org,
                "location": loc,
                "location_code": "RA",
                "location_name": "Region A",
                "resource_code": res_code,
                "resource": res_info.get("key"),
                "quantity": int(qty_raw) if qty_raw.isdigit() else 0,
                "status_code": status_raw.upper(),
                "status": PROVIDER_AVAILABILITY.get(status_raw.upper(), "available"),
                "legacy": True,
                "source": "sms",
                "geo": {"coordinates": [77.4126, 23.2599]}
            }

    # 5. Allocation 'A'
    # Canonical: A|SEQ|PLAN|ORG|RESOURCE|QTY|LOC|ETA|CRC
    if type_code == "A":
        if len(parts) >= 9:
            seq, plan_id, org, res_raw, qty_raw, loc_raw, eta_raw, crc = parts[1:9]
            loc = parse_location(loc_raw)
            res_code = RESOURCE_ALIASES.get(res_raw.upper(), res_raw)
            res_info = RESOURCE_BY_CODE.get(res_code, {"key": res_raw.lower()})
            return {
                "type": "allocation",
                "message_type": "A",
                "seq": seq,
                "plan_id": plan_id,
                "organization_id": org,
                "resource_code": res_code,
                "resource": res_info.get("key"),
                "quantity": int(qty_raw) if qty_raw.isdigit() else 0,
                "destination_code": loc.get("location_code"),
                "destination_name": loc.get("location_name"),
                "eta_hours": float(eta_raw) if eta_raw.replace(".", "").isdigit() else 1.0,
                "checksum": crc,
                "checksum_valid": verify_checksum(trimmed),
                "source": "sms"
            }

    # 6. Status Update 'S'
    # Canonical: S|SEQ|PLAN|STATUS|CRC
    if type_code == "S":
        if len(parts) >= 5:
            seq, plan_id, stat_code, crc = parts[1:5]
            return {
                "type": "status",
                "message_type": "S",
                "seq": seq,
                "plan_id": plan_id,
                "status_code": stat_code,
                "status": STATUS_CODES.get(stat_code, "unknown"),
                "checksum": crc,
                "checksum_valid": verify_checksum(trimmed),
                "source": "sms"
            }
        elif len(parts) >= 4:
            seq, plan_id, stat_code = parts[1:4]
            return {
                "type": "status",
                "message_type": "S",
                "seq": seq,
                "plan_id": plan_id,
                "status_code": stat_code,
                "status": STATUS_CODES.get(stat_code, "unknown"),
                "checksum": None,
                "checksum_valid": True,
                "source": "sms"
            }

    # 7. Confirmation 'C'
    # Canonical: C|SEQ|REF|RESULT|CRC or citizen ack C|SEQ|UID|REF|STATE|ETA|CRC
    if type_code == "C":
        if len(parts) >= 7:  # Citizen ACK variant: C|001|7F3K|PLAN101|OK|4|7F
            seq, uid, ref, state, eta, crc = parts[1:7]
            return {
                "type": "citizen_confirmation",
                "message_type": "C",
                "seq": seq,
                "uid": uid,
                "reference": ref,
                "result": state.lower(),
                "eta_hours": float(eta) if eta.replace(".", "").isdigit() else 1.0,
                "checksum": crc,
                "checksum_valid": verify_checksum(trimmed),
                "source": "sms"
            }
        elif len(parts) >= 5:
            seq, ref, result, crc = parts[1:5]
            return {
                "type": "confirmation",
                "message_type": "C",
                "seq": seq,
                "reference": ref,
                "result": result.lower(),
                "checksum": crc,
                "checksum_valid": verify_checksum(trimmed),
                "source": "sms"
            }

    # 8. Cancel 'X'
    # Canonical: X|SEQ|REF|REASON|CRC
    if type_code == "X":
        if len(parts) >= 5:
            seq, ref, reason, crc = parts[1:5]
            return {
                "type": "cancel",
                "message_type": "X",
                "seq": seq,
                "reference": ref,
                "reason": reason.lower(),
                "checksum": crc,
                "checksum_valid": verify_checksum(trimmed),
                "source": "sms"
            }

    # 9. Map Marker 'M'
    # Canonical: M|SEQ|LOC|MARKER_TYPE|SEVERITY|DATA|CRC
    if type_code == "M":
        if len(parts) >= 7:
            seq, loc_raw, m_type, sev_raw, data_raw, crc = parts[1:7]
            loc = parse_location(loc_raw)
            return {
                "type": "marker",
                "message_type": "M",
                "seq": seq,
                "location": loc,
                "marker_type": m_type.lower(),
                "severity": int(sev_raw) if sev_raw.isdigit() else 5,
                "data": data_raw,
                "checksum": crc,
                "checksum_valid": verify_checksum(trimmed),
                "source": "sms"
            }

    # 10. Polygon Chunk 'P'
    # Canonical: P|CHUNK/TOTAL|SEQ|LOC|ZONE_TYPE|POINTS|END|CRC
    if type_code == "P":
        if len(parts) >= 8:
            chunk_ratio, seq, loc_raw, zone_type, points_raw, end_flag, crc = parts[1:8]
            chunk_num, total_chunks = 1, 1
            if "/" in chunk_ratio:
                cp = chunk_ratio.split("/")
                chunk_num, total_chunks = int(cp[0]), int(cp[1])
            
            # Points are separated by ';' and coords by ','
            point_list = []
            for pt in points_raw.split(";"):
                if "," in pt:
                    coords = pt.split(",")
                    lat = float(coords[0].strip())
                    lon = float(coords[1].strip())
                    point_list.append([lon, lat])  # GeoJSON [lng, lat]

            return {
                "type": "polygon",
                "message_type": "P",
                "seq": seq,
                "chunk": chunk_num,
                "total_chunks": total_chunks,
                "location_code": loc_raw,
                "zone_type": zone_type.lower(),
                "points": point_list,
                "complete": (end_flag.upper() == "Y"),
                "checksum": crc,
                "checksum_valid": verify_checksum(trimmed),
                "source": "sms"
            }

    # 11. Route Update 'RT' or 'ROUTE'
    if type_code in ("RT", "ROUTE"):
        if len(parts) >= 6:
            seq, org, route_id, points_raw, crc = parts[1:6]
            point_list = []
            for pt in points_raw.split(";"):
                if "," in pt:
                    coords = pt.split(",")
                    lat = float(coords[0].strip())
                    lon = float(coords[1].strip())
                    point_list.append([lon, lat])
            return {
                "type": "route",
                "message_type": "RT",
                "seq": seq,
                "organization_id": org,
                "route_id": route_id,
                "points": point_list,
                "checksum": crc,
                "checksum_valid": verify_checksum(trimmed),
                "source": "sms"
            }

    # 12. Error Message 'E'
    if type_code == "E":
        if len(parts) >= 5:
            seq, code, msg, crc = parts[1:5]
            return {
                "type": "error",
                "message_type": "E",
                "seq": seq,
                "error_code": code,
                "message": msg,
                "checksum": crc,
                "checksum_valid": verify_checksum(trimmed),
                "source": "sms"
            }

    raise ValueError(f"Unrecognized or unsupported frame format: '{trimmed}'")
