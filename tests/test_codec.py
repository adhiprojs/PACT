"""
Tests for PACT Base-36 Codec, PACK10 Geolocation, XOR Checksum, and Message Frames.
"""

import pytest
from app.codec.base36 import base36_encode, base36_decode
from app.codec.checksum import calculate_xor_checksum, verify_checksum, append_checksum
from app.codec.pack10 import encode_pack10, decode_pack10
from app.codec.requester_codec import (
    decode_requester_payload, encode_requester_payload,
    decode_q_frame, encode_q_frame
)
from app.codec.provider_codec import (
    decode_provider_payload, encode_provider_payload,
    decode_g_frame, encode_g_frame
)
from app.codec.canonical_codec import parse_sms
from app.codec.fanout import q_to_n_fanout


def test_base36_roundtrip():
    values = [0, 1, 35, 36, 100, 4095, 11325991, 25741263, 60466175]
    for v in values:
        encoded = base36_encode(v)
        decoded = base36_decode(encoded)
        assert decoded == v, f"Failed for {v}"


def test_xor_checksum_worked_example():
    frame_body = "Q|001|7F3K|15223C03Q0|6QR6VFBQ33"
    crc = calculate_xor_checksum(frame_body)
    assert crc == "7F", f"Expected '7F', got '{crc}'"

    full_frame = f"{frame_body}|7F"
    assert verify_checksum(full_frame) is True
    assert verify_checksum(f"{frame_body}|00") is False


def test_pack10_worked_example():
    # Lat: 23.25991 -> 6QR6V, Lon: 77.41263 -> FBQ33
    lat = 23.25991
    lon = 77.41263
    pack10 = encode_pack10(lat, lon)
    assert pack10 == "6QR6VFBQ33", f"Expected '6QR6VFBQ33', got '{pack10}'"

    dec_lat, dec_lon, acc = decode_pack10(pack10)
    assert abs(dec_lat - lat) < 0.0001
    assert abs(dec_lon - lon) < 0.0001


def test_decode_q_frame():
    raw_frame = "Q|001|7F3K|15223C03Q0|6QR6VFBQ33|7F"
    decoded = decode_q_frame(raw_frame)

    assert decoded["type"] == "individual_request"
    assert decoded["message_type"] == "Q"
    assert decoded["seq"] == "001"
    assert decoded["uid"] == "7F3K"
    assert decoded["checksum_valid"] is True

    payload = decoded["payload"]
    assert payload["schema_version"] == "1"
    assert payload["people_estimate"] == 3
    assert payload["urgency_code"] == "C"

    # Needs: Water (bit 1), Medical (bit 2), Evac transport (bit 7) -> 2 + 4 + 128 = 134 -> "03Q"
    needed_keys = [r["key"] for r in payload["needed_resources"]]
    assert "water_kits" in needed_keys
    assert "medical_kits" in needed_keys
    assert "evac_transport" in needed_keys

    # Coordinates
    geo = decoded["geo"]
    assert abs(geo["latitude"] - 23.25991) < 0.0001
    assert abs(geo["longitude"] - 77.41263) < 0.0001


def test_q_fanout():
    raw_frame = "Q|001|7F3K|15223C03Q0|6QR6VFBQ33|7F"
    decoded = decode_q_frame(raw_frame)
    needs = q_to_n_fanout(decoded)

    assert len(needs) == 3
    keys = {n["resource_key"]: n["quantity"] for n in needs}
    assert keys["water_kits"] >= 6  # 3 people * 2.0
    assert keys["medical_kits"] >= 1
    assert keys["evac_transport"] >= 1


def test_provider_offer_codec():
    # Org type 'N' (NGO), Food + Water (bits 0,1 -> 3 -> "003"), cap 4 (500), rad 3 (50km), eta 2 (2h), avail 'A'
    payload = encode_provider_payload(
        org_type_code="N",
        resource_keys_or_bits=["food_kits", "water_kits"],
        capacity_code="4",
        radius_code="3",
        eta_code="2",
        availability_code="A"
    )
    assert len(payload) == 9

    g_frame = encode_g_frame("001", "NGO01", payload, 23.2650, 77.4050)
    decoded_g = decode_g_frame(g_frame)

    assert decoded_g["message_type"] == "G"
    assert decoded_g["organization_id"] == "NGO01"
    assert decoded_g["checksum_valid"] is True
    assert decoded_g["payload"]["org_info"]["code"] == "NGO"


def test_canonical_sms_parser_all_types():
    # 1. Need Request
    n_sms = "N|001|NGO01|RA|F|300|H|B3"
    parsed_n = parse_sms(n_sms)
    assert parsed_n["type"] == "need"
    assert parsed_n["quantity"] == 300
    assert parsed_n["organization_id"] == "NGO01"

    # 2. Resource Offer
    r_sms = "R|002|CSR02|RA|F|200|A|7C"
    parsed_r = parse_sms(r_sms)
    assert parsed_r["type"] == "resource"
    assert parsed_r["quantity"] == 200

    # 3. Status Update
    s_sms = "S|004|PLAN101|3|A1"
    parsed_s = parse_sms(s_sms)
    assert parsed_s["type"] == "status"
    assert parsed_s["status"] == "delivered"

    # 4. Confirmation / Ack
    c_sms = "C|001|7F3K|PLAN101|OK|4|7F"
    parsed_c = parse_sms(c_sms)
    assert parsed_c["type"] == "citizen_confirmation"
    assert parsed_c["reference"] == "PLAN101"

    # 5. Legacy delivery format
    legacy = "DELIVERED RegionA food 200"
    parsed_leg = parse_sms(legacy)
    assert parsed_leg["status"] == "delivered"
    assert parsed_leg["quantity"] == 200
