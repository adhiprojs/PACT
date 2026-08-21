"""
Provider offer frame and payload codec (Message Type 'G').
Encodes/decodes the 9-character Base-36 state string and full G-frame.
"""

from typing import Dict, Any, List, Optional
from app.codec.base36 import base36_encode, base36_decode
from app.codec.pack10 import encode_pack10, decode_pack10
from app.codec.checksum import calculate_xor_checksum, verify_checksum
from app.codec.taxonomy import (
    PROVIDER_ORG_TYPES, CAPACITY_BUCKETS, RADIUS_BUCKETS, ETA_BUCKETS,
    PROVIDER_AVAILABILITY, RESOURCES, RESOURCE_BY_BIT, RESOURCE_BY_KEY
)


def decode_provider_payload(payload_str: str) -> Dict[str, Any]:
    """
    Decodes the 9-character Base-36 provider offer string.
    Pos 0: Version ('2')
    Pos 1: Org Type
    Pos 2-4: Resource Bitfield (12 bits, 3 chars base36)
    Pos 5: Capacity Bucket
    Pos 6: Radius Bucket
    Pos 7: ETA Bucket
    Pos 8: Availability Status (A/L/U)
    """
    p = payload_str.strip().upper()
    if len(p) < 9:
        raise ValueError(f"Provider payload must be 9 characters, got '{p}' ({len(p)})")

    version = p[0]
    org_type_char = p[1]
    res_str = p[2:5]
    cap_char = p[5]
    rad_char = p[6]
    eta_char = p[7]
    avail_char = p[8]

    org_info = PROVIDER_ORG_TYPES.get(org_type_char, {"code": "NGO", "label": "Non-Governmental Org", "fleet_type": "vans"})
    capacity_units = CAPACITY_BUCKETS.get(cap_char, 100)
    radius_km = RADIUS_BUCKETS.get(rad_char, 25)
    eta_hours = ETA_BUCKETS.get(eta_char, 2.0)
    availability = PROVIDER_AVAILABILITY.get(avail_char, "available")

    res_int = base36_decode(res_str)
    offered_resources: List[Dict[str, Any]] = []
    for bit in range(12):
        if (res_int >> bit) & 1:
            if bit in RESOURCE_BY_BIT:
                offered_resources.append(RESOURCE_BY_BIT[bit])

    return {
        "schema_version": version,
        "org_type_code": org_type_char,
        "org_info": org_info,
        "resource_bitfield": res_int,
        "offered_resources": offered_resources,
        "capacity_code": cap_char,
        "capacity_units": capacity_units,
        "radius_code": rad_char,
        "radius_km": radius_km,
        "eta_code": eta_char,
        "eta_hours": eta_hours,
        "availability_code": avail_char,
        "availability": availability,
        "raw_payload": p,
    }


def encode_provider_payload(
    org_type_code: str = "N",
    resource_keys_or_bits: Optional[List[Any]] = None,
    capacity_code: str = "2",
    radius_code: str = "2",
    eta_code: str = "2",
    availability_code: str = "A",
    version: str = "2"
) -> str:
    """
    Encodes provider parameters into a 9-character Base-36 string.
    """
    res_int = 0
    if resource_keys_or_bits:
        for item in resource_keys_or_bits:
            if isinstance(item, int):
                res_int |= (1 << item)
            elif isinstance(item, str) and item in RESOURCE_BY_KEY:
                res_int |= (1 << RESOURCE_BY_KEY[item]["bit"])

    res_str = base36_encode(res_int, min_length=3)
    payload = f"{version}{org_type_code}{res_str}{capacity_code}{radius_code}{eta_code}{availability_code}"
    return payload[:9]


def decode_g_frame(frame: str) -> Dict[str, Any]:
    """
    Decodes full G-frame: G|SEQ|ORG|PAYLOAD|GEO|CRC
    """
    parts = [p.strip() for p in frame.strip().split("|")]
    if len(parts) < 6:
        raise ValueError(f"Invalid G frame, expected at least 6 parts: '{frame}'")

    msg_type, seq, org_id, payload_str, geo_str, crc = parts[0], parts[1], parts[2], parts[3], parts[4], parts[5]
    if msg_type != "G":
        raise ValueError(f"Expected message type 'G', got '{msg_type}'")

    body = "|".join(parts[:5])
    computed_crc = calculate_xor_checksum(body)
    crc_valid = (computed_crc.upper() == crc.upper())

    lat, lon, accuracy_m = decode_pack10(geo_str)
    parsed_payload = decode_provider_payload(payload_str)

    return {
        "type": "provider_offer",
        "message_type": "G",
        "seq": seq,
        "organization_id": org_id,
        "payload": parsed_payload,
        "geo": {
            "latitude": lat,
            "longitude": lon,
            "accuracy_m": accuracy_m,
            "pack10": geo_str,
            "coordinates": [lon, lat]
        },
        "checksum": crc,
        "checksum_valid": crc_valid,
        "raw_frame": frame,
        "source": "sms"
    }


def encode_g_frame(
    seq: str,
    org_id: str,
    payload_str: str,
    lat: float,
    lon: float
) -> str:
    """
    Constructs a complete G frame with PACK10 geolocation and XOR checksum.
    """
    geo_str = encode_pack10(lat, lon)
    body = f"G|{seq}|{org_id}|{payload_str}|{geo_str}"
    crc = calculate_xor_checksum(body)
    return f"{body}|{crc}"
