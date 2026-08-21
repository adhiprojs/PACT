"""
PACK10 Geolocation Codec.
Encodes global GPS coordinates into 10 characters (Base-36) at ~1.1m precision
without any external heavy geohash dependencies.

Formula:
  lat_offset = round((lat + 90.0) * 100000)   # 0 to 18,000,000  (max 36^5 = 60,466,176)
  lon_offset = round((lon + 180.0) * 100000)  # 0 to 36,000,000
  lat_token = base36(lat_offset) padded to 5 chars
  lon_token = base36(lon_offset) padded to 5 chars
  PACK10 = lat_token + lon_token
"""

from typing import Tuple, Optional
from app.codec.base36 import base36_encode, base36_decode

ACCURACY_BUCKETS = {
    "0": 1,     # <1m
    "1": 3,     # 3m
    "2": 5,     # 5m
    "3": 10,    # 10m
    "4": 25,    # 25m
    "5": 50,    # 50m
    "6": 100,   # 100m
    "7": 250,   # 250m
    "8": 500,   # 500m
    "9": 1000,  # 1000m / approximate
}


def encode_pack10(lat: float, lon: float, accuracy_bucket: Optional[str] = None) -> str:
    """
    Encodes lat/lon into a 10-character Base-36 string (or 11 chars if accuracy_bucket provided).
    """
    # Clamp bounds
    lat = max(-90.0, min(90.0, lat))
    lon = max(-180.0, min(180.0, lon))

    lat_offset = round((lat + 90.0) * 100000)
    lon_offset = round((lon + 180.0) * 100000)

    lat_token = base36_encode(lat_offset, min_length=5)
    lon_token = base36_encode(lon_offset, min_length=5)

    res = lat_token + lon_token
    if accuracy_bucket and accuracy_bucket in ACCURACY_BUCKETS:
        res += accuracy_bucket
    return res


def decode_pack10(pack10_str: str) -> Tuple[float, float, int]:
    """
    Decodes a 10 (or 11) character Base-36 string into (lat, lon, accuracy_meters).
    """
    s = pack10_str.strip().upper()
    if len(s) < 10:
        raise ValueError(f"PACK10 string must be at least 10 characters: '{pack10_str}'")

    lat_token = s[0:5]
    lon_token = s[5:10]

    lat_offset = base36_decode(lat_token)
    lon_offset = base36_decode(lon_token)

    lat = round((lat_offset / 100000.0) - 90.0, 5)
    lon = round((lon_offset / 100000.0) - 180.0, 5)

    accuracy_m = 5
    if len(s) >= 11 and s[10] in ACCURACY_BUCKETS:
        accuracy_m = ACCURACY_BUCKETS[s[10]]

    return lat, lon, accuracy_m
