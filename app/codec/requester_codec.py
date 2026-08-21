"""
Requester frame and payload codec (Message Type 'Q').
Encodes/decodes the 10-character Base-36 state string and full Q-frame.
"""

from typing import Dict, Any, List, Optional
from app.codec.base36 import base36_encode, base36_decode
from app.codec.pack10 import encode_pack10, decode_pack10
from app.codec.checksum import calculate_xor_checksum, verify_checksum
from app.codec.taxonomy import (
    SITUATIONS, HEADCOUNTS, INJURIES, MOBILITY, URGENCY,
    RESOURCES, RESOURCE_BY_BIT, RESOURCE_BY_KEY, VULNERABILITIES
)


def decode_requester_payload(payload_str: str) -> Dict[str, Any]:
    """
    Decodes the 10-character Base-36 requester state string.
    Pos 0: Version ('1')
    Pos 1: Situation Type
    Pos 2: Headcount Bucket
    Pos 3: Injury Severity
    Pos 4: Mobility
    Pos 5: Urgency (L/M/H/C)
    Pos 6-8: Needs Bitfield (12 bits, 3 chars base36)
    Pos 9: Vulnerability Bitfield (5 bits, 1 char base36)
    """
    p = payload_str.strip().upper()
    if len(p) < 10:
        raise ValueError(f"Requester payload must be 10 characters, got '{p}' ({len(p)})")

    version = p[0]
    sit_char = p[1]
    hc_char = p[2]
    inj_char = p[3]
    mob_char = p[4]
    urg_char = p[5]
    needs_str = p[6:9]
    vuln_char = p[9]

    situation = SITUATIONS.get(sit_char, {"code": "GEN", "name": "General Emergency", "icon": "⚠️", "severity_base": 5})
    headcount = HEADCOUNTS.get(hc_char, {"label": "1 person", "min": 1, "max": 1, "est": 1})
    injury = INJURIES.get(inj_char, {"code": "NONE", "label": "Uninjured", "score": 0})
    mobility = MOBILITY.get(mob_char, {"code": "MOB", "label": "Fully Mobile", "score": 0})
    urgency = URGENCY.get(urg_char, {"label": "Medium", "rank": 2, "color": "#F59E0B"})

    # Needs bitfield
    needs_int = base36_decode(needs_str)
    needed_resources: List[Dict[str, Any]] = []
    for bit in range(12):
        if (needs_int >> bit) & 1:
            if bit in RESOURCE_BY_BIT:
                needed_resources.append(RESOURCE_BY_BIT[bit])

    # Vulnerabilities bitfield
    vuln_int = base36_decode(vuln_char)
    vulnerabilities: List[Dict[str, Any]] = []
    for v in VULNERABILITIES:
        if (vuln_int >> v["bit"]) & 1:
            vulnerabilities.append(v)

    return {
        "schema_version": version,
        "situation_code": sit_char,
        "situation": situation,
        "headcount_code": hc_char,
        "headcount": headcount,
        "people_estimate": headcount["est"],
        "injury_code": inj_char,
        "injury": injury,
        "mobility_code": mob_char,
        "mobility": mobility,
        "urgency_code": urg_char,
        "urgency": urgency,
        "needs_bitfield": needs_int,
        "needed_resources": needed_resources,
        "vulnerability_bitfield": vuln_int,
        "vulnerabilities": vulnerabilities,
        "raw_payload": p,
    }


def encode_requester_payload(
    situation_code: str = "0",
    headcount_code: str = "0",
    injury_code: str = "0",
    mobility_code: str = "0",
    urgency_code: str = "M",
    needs_keys_or_bits: Optional[List[Any]] = None,
    vulnerability_bits: Optional[List[int]] = None,
    version: str = "1"
) -> str:
    """
    Encodes requester selections into a 10-character Base-36 string.
    """
    needs_int = 0
    if needs_keys_or_bits:
        for item in needs_keys_or_bits:
            if isinstance(item, int):
                needs_int |= (1 << item)
            elif isinstance(item, str) and item in RESOURCE_BY_KEY:
                needs_int |= (1 << RESOURCE_BY_KEY[item]["bit"])

    vuln_int = 0
    if vulnerability_bits:
        for bit in vulnerability_bits:
            vuln_int |= (1 << bit)

    needs_str = base36_encode(needs_int, min_length=3)
    vuln_str = base36_encode(vuln_int, min_length=1)

    payload = f"{version}{situation_code}{headcount_code}{injury_code}{mobility_code}{urgency_code}{needs_str}{vuln_str}"
    return payload[:10]


def decode_q_frame(frame: str) -> Dict[str, Any]:
    """
    Decodes full Q-frame: Q|SEQ|UID|PAYLOAD|GEO|CRC
    """
    parts = [p.strip() for p in frame.strip().split("|")]
    if len(parts) < 6:
        raise ValueError(f"Invalid Q frame, expected at least 6 parts: '{frame}'")

    msg_type, seq, uid, payload_str, geo_str, crc = parts[0], parts[1], parts[2], parts[3], parts[4], parts[5]
    if msg_type != "Q":
        raise ValueError(f"Expected message type 'Q', got '{msg_type}'")

    # Verify checksum
    body = "|".join(parts[:5])
    computed_crc = calculate_xor_checksum(body)
    crc_valid = (computed_crc.upper() == crc.upper())

    lat, lon, accuracy_m = decode_pack10(geo_str)
    parsed_payload = decode_requester_payload(payload_str)

    return {
        "type": "individual_request",
        "message_type": "Q",
        "seq": seq,
        "uid": uid,
        "payload": parsed_payload,
        "geo": {
            "latitude": lat,
            "longitude": lon,
            "accuracy_m": accuracy_m,
            "pack10": geo_str,
            "coordinates": [lon, lat]  # GeoJSON [lng, lat]
        },
        "checksum": crc,
        "checksum_valid": crc_valid,
        "raw_frame": frame,
        "source": "sms"
    }


def encode_q_frame(
    seq: str,
    uid: str,
    payload_str: str,
    lat: float,
    lon: float
) -> str:
    """
    Constructs a complete Q frame with PACK10 geolocation and XOR checksum.
    """
    geo_str = encode_pack10(lat, lon)
    body = f"Q|{seq}|{uid}|{payload_str}|{geo_str}"
    crc = calculate_xor_checksum(body)
    return f"{body}|{crc}"
