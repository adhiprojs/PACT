# PACT: Privacy-Preserving Multi-Agent Autonomous Crisis Coordination Platform
## Full Project Source Code & Technical Architecture Extract

## Table of Contents

1. [`README.md`](#file-readme-md)
2. [`sms.md`](#file-sms-md)
3. [`requirements.txt`](#file-requirements-txt)
4. [`start_server.sh`](#file-start_server-sh)
5. [`run_server.py`](#file-run_server-py)
6. [`app/config.py`](#file-app-config-py)
7. [`app/main.py`](#file-app-main-py)
8. [`app/codec/base36.py`](#file-app-codec-base36-py)
9. [`app/codec/pack10.py`](#file-app-codec-pack10-py)
10. [`app/codec/checksum.py`](#file-app-codec-checksum-py)
11. [`app/codec/taxonomy.py`](#file-app-codec-taxonomy-py)
12. [`app/codec/canonical_codec.py`](#file-app-codec-canonical_codec-py)
13. [`app/codec/requester_codec.py`](#file-app-codec-requester_codec-py)
14. [`app/codec/provider_codec.py`](#file-app-codec-provider_codec-py)
15. [`app/codec/fanout.py`](#file-app-codec-fanout-py)
16. [`app/db/models.py`](#file-app-db-models-py)
17. [`app/db/mongo.py`](#file-app-db-mongo-py)
18. [`app/db/indexes.py`](#file-app-db-indexes-py)
19. [`app/db/seed.py`](#file-app-db-seed-py)
20. [`app/bus/eventbus.py`](#file-app-bus-eventbus-py)
21. [`app/agents/tools.py`](#file-app-agents-tools-py)
22. [`app/agents/llm_client.py`](#file-app-agents-llm_client-py)
23. [`app/agents/pipeline.py`](#file-app-agents-pipeline-py)
24. [`app/agents/a0_intake.py`](#file-app-agents-a0_intake-py)
25. [`app/agents/a1_dedupe.py`](#file-app-agents-a1_dedupe-py)
26. [`app/agents/a2_triage.py`](#file-app-agents-a2_triage-py)
27. [`app/agents/a3_geo_matcher.py`](#file-app-agents-a3_geo_matcher-py)
28. [`app/agents/a4_advocates.py`](#file-app-agents-a4_advocates-py)
29. [`app/agents/a5_solver.py`](#file-app-agents-a5_solver-py)
30. [`app/agents/a6_arbiter.py`](#file-app-agents-a6_arbiter-py)
31. [`app/agents/a7_redactor.py`](#file-app-agents-a7_redactor-py)
32. [`app/agents/a8_admin_gate.py`](#file-app-agents-a8_admin_gate-py)
33. [`app/agents/a9_narrator.py`](#file-app-agents-a9_narrator-py)
34. [`app/agents/a10_verify.py`](#file-app-agents-a10_verify-py)
35. [`app/agents/a11_replan.py`](#file-app-agents-a11_replan-py)
36. [`app/api/ingest.py`](#file-app-api-ingest-py)
37. [`app/api/requests.py`](#file-app-api-requests-py)
38. [`app/api/offers.py`](#file-app-api-offers-py)
39. [`app/api/matches.py`](#file-app-api-matches-py)
40. [`app/api/admin.py`](#file-app-api-admin-py)
41. [`app/api/simulator.py`](#file-app-api-simulator-py)
42. [`app/api/ws.py`](#file-app-api-ws-py)
43. [`gateway/termux_gateway.py`](#file-gateway-termux_gateway-py)
44. [`android/app/src/main/java/org/humanitarian/fieldapp/MainActivity.kt`](#file-android-app-src-main-java-org-humanitarian-fieldapp-mainactivity-kt)
45. [`android/app/src/main/java/org/humanitarian/fieldapp/sms/Base36.kt`](#file-android-app-src-main-java-org-humanitarian-fieldapp-sms-base36-kt)
46. [`android/app/src/main/java/org/humanitarian/fieldapp/sms/Pack10.kt`](#file-android-app-src-main-java-org-humanitarian-fieldapp-sms-pack10-kt)
47. [`android/app/src/main/java/org/humanitarian/fieldapp/sms/Checksum.kt`](#file-android-app-src-main-java-org-humanitarian-fieldapp-sms-checksum-kt)
48. [`android/app/src/main/java/org/humanitarian/fieldapp/sms/SmsCodes.kt`](#file-android-app-src-main-java-org-humanitarian-fieldapp-sms-smscodes-kt)
49. [`android/app/src/main/java/org/humanitarian/fieldapp/sms/SmsEncoder.kt`](#file-android-app-src-main-java-org-humanitarian-fieldapp-sms-smsencoder-kt)
50. [`android/app/src/main/java/org/humanitarian/fieldapp/sms/SmsDecoder.kt`](#file-android-app-src-main-java-org-humanitarian-fieldapp-sms-smsdecoder-kt)
51. [`android/app/src/main/java/org/humanitarian/fieldapp/sms/DirectSmsSender.kt`](#file-android-app-src-main-java-org-humanitarian-fieldapp-sms-directsmssender-kt)
52. [`android/app/src/main/java/org/humanitarian/fieldapp/network/ApiClient.kt`](#file-android-app-src-main-java-org-humanitarian-fieldapp-network-apiclient-kt)
53. [`android/app/src/main/java/org/humanitarian/fieldapp/offline/OfflineQueue.kt`](#file-android-app-src-main-java-org-humanitarian-fieldapp-offline-offlinequeue-kt)
54. [`android/app/src/main/java/org/humanitarian/fieldapp/ui/FieldReportScreen.kt`](#file-android-app-src-main-java-org-humanitarian-fieldapp-ui-fieldreportscreen-kt)
55. [`android/app/src/main/java/org/humanitarian/fieldapp/ui/SmsDecoderScreen.kt`](#file-android-app-src-main-java-org-humanitarian-fieldapp-ui-smsdecoderscreen-kt)
56. [`android/app/src/main/java/org/humanitarian/fieldapp/ui/SmsFallbackScreen.kt`](#file-android-app-src-main-java-org-humanitarian-fieldapp-ui-smsfallbackscreen-kt)
57. [`android/app/src/main/java/org/humanitarian/fieldapp/ui/HomeScreen.kt`](#file-android-app-src-main-java-org-humanitarian-fieldapp-ui-homescreen-kt)
58. [`app/static/index.html`](#file-app-static-index-html)
59. [`app/static/css/styles.css`](#file-app-static-css-styles-css)
60. [`app/static/js/map.js`](#file-app-static-js-map-js)
61. [`app/static/js/app.js`](#file-app-static-js-app-js)
62. [`tests/test_codec.py`](#file-tests-test_codec-py)
63. [`tests/test_pipeline.py`](#file-tests-test_pipeline-py)
64. [`tests/test_api.py`](#file-tests-test_api-py)

---

<a id="file-readme-md"></a>
## File: `README.md`

```markdown
# PACT — Privacy-Preserving Multi-Agent Humanitarian Coordination Platform

> **"Zero-connectivity resilience, zero hallucinated aid, zero-knowledge privacy."**

PACT is an emergency humanitarian dispatch platform built for rapid coordination during infrastructure blackouts, disasters, and telecommunications collapse.

---

## ⚡ Key Capabilities & Architecture

1. **Ultra-Compressed Base-36 & PACK10 Geolocation Codec**:
   - Compresses complete multi-parameter citizen emergency requests into **35 GSM-7 characters** (`Q|001|7F3K|15223C03Q0|6QR6VFBQ33|7F`), leaving 125 characters spare in standard SMS.
   - Encodes global GPS coordinates down to **~1.1-meter precision** in 10 characters (`PACK10`) without external heavy geohash dependencies.
   - Dynamic 2-digit uppercase hexadecimal **XOR Checksum** validation on every frame.
2. **Dual-Channel Ingestion (SMS & HTTP REST)**:
   - `POST /api/v1/pact/ingest`: Unified wire format endpoint for mobile apps and field gateways.
   - `POST /api/v1/sms/webhook`: Adapter endpoint for Termux rootless SMS gateways and cellular modems.
   - Complete canonical SMS registry (`Q`, `G`, `N`, `R`, `A`, `S`, `C`, `X`, `M`, `P`, `RT`, `E`) + legacy demo fallback.
3. **12-Stage Multi-Agent Reasoning Pipeline & Hallucination Firewall**:
   - **A0 Intake**: Python frame parsing & XOR checksum validation.
   - **A1 Dedupe**: Compound deduplication check on `(uid, seq)`.
   - **A2 Triage**: Groq `llama-3.3-70b-versatile` (with deterministic fallback) situational triage & risk scoring.
   - **A3 Geo Matcher**: MongoDB `$geoNear` 2dsphere spatial index cascading search rings (`10km -> 25km -> 60km -> 150km`).
   - **A4 Advocates**: Groq parallel deliberation simulating provider stances & operational constraints.
   - **A5 Allocation Solver**: Pure Python deterministic mathematical optimizer producing 3 fixed options: `fastest`, `max_coverage`, `least_depleting`.
   - **A6 Arbiter**: Groq `llama-3.3-70b-versatile` with strict Pydantic validation selecting an `option_id` (**firewalled from inventing numbers**).
   - **A7 Privacy Redactor**: Zero-knowledge identity and GPS masking.
   - **A8 Admin Gate**: `asyncio.Future` interrupt with configurable Autopilot timer.
   - **A9 Narrator**: Groq plain-English operational bulletin generator.
   - **A10 Verification**: Field handshake validation and automated SMS acknowledgement generation (`C|001|7F3K|PLAN101|OK|4|7F`).
   - **A11 Replanner**: Pure Python re-entry trigger on delivery failure or rejection.
4. **Real-Time Admin Command Portal & Ingress Simulator**:
   - Live WebSocket stream (`/ws/agents`) with token streaming.
   - Interactive Crisis Map visualizer with `$geoNear` radius search rings.
   - One-click SMS Ingress Simulator with pre-loaded disaster scenarios.

---

## 🚀 Quickstart

### 1. Launch the Server
```bash
./start_server.sh
# or manually:
./venv/bin/python3 run_server.py
```
- **Admin Command Portal**: [http://localhost:8000](http://localhost:8000)
- **Interactive OpenAPI Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Live WebSocket Stream**: `ws://localhost:8000/ws/agents`

### 2. Environment Variables (Optional)
```bash
export GROQ_API_KEY="your_groq_api_key"        # Optional: Groq Llama-3.3-70B (auto-falls back to deterministic engine if unset)
export MONGODB_URI="mongodb://localhost:27017"  # Optional: live Mongo (auto-falls back to in-memory mock engine)
export AUTOPILOT_ENABLED="true"                # Autopilot auto-dispatch mode (default: true)
export AUTOPILOT_TIMEOUT_SECONDS="3.0"         # Autopilot decision timer
```

### 3. Run Test Suite
```bash
./venv/bin/pytest -v
```
All 16 unit and integration tests verify PACK10 round-tripping, XOR checksum arithmetic, deterministic solver math, and API endpoints.

---

## 📱 Termux Rootless SMS Gateway

Turn any Android phone with a SIM card into an automated SMS gateway without root access:

1. Install **Termux** and **Termux:API** from F-Droid.
2. Grant SMS and Phone permissions in Android settings; disable battery optimization.
3. Inside Termux:
```bash
pkg update -y && pkg install termux-api python -y
pip install requests
termux-wake-lock
python gateway/termux_gateway.py
```
Incoming emergency SMS frames are automatically forwarded to `http://<laptop-ip>:8000/api/v1/sms/webhook`.

---

## 📂 Project Structure

```
PACT project/
├── app/
│   ├── codec/                  # Base-36, PACK10, XOR Checksum, Q/G/N/R codecs & taxonomy
│   ├── db/                     # MongoDB client, models, geospatial indexes & seed data
│   ├── bus/                    # In-process asyncio Pub/Sub event bus with '?since=<seq>' replay
│   ├── agents/                 # A0 to A11 agents & pipeline orchestrator
│   ├── api/                    # Ingest, requests, offers, matches, admin & simulator REST endpoints
│   ├── static/                 # Real-time Admin Command Portal & Crisis Map UI
│   ├── config.py               # Settings & environment variables
│   └── main.py                 # FastAPI application
├── gateway/
│   └── termux_gateway.py       # Rootless Android SMS gateway script
├── tests/                      # Pytest automated test suite
├── start_server.sh             # Startup script
├── run_server.py               # Direct runner
├── requirements.txt            # Python dependencies
└── README.md                   # Documentation
```
```

---

<a id="file-sms-md"></a>
## File: `sms.md`

```markdown
# SMS_PROTOCOL.md

This document defines the SMS fallback protocol for the Privacy-Preserving Multi-Agent Humanitarian Coordination Platform.

SMS is used as an emergency data-transfer channel when internet connectivity is unavailable or unstable.

---

## 1. Purpose

The SMS protocol allows field workers, organizations, and coordination systems to exchange small emergency messages.

SMS is used for:

- Need requests
- Resource availability
- Allocation updates
- Status updates
- Confirmations
- Dispatch updates
- Delivery confirmations
- Cancellations
- Map marker updates
- Polygon chunks
- Route updates
- Error reporting

SMS is not used for:

- Full database synchronization
- Images
- Videos
- Map tiles
- Large inventory transfers
- Real-time tracking streams
- Sensitive personal data

---

## 2. Core Design Rules

1. Use plain ASCII text only.
2. Use `|` as the main field delimiter.
3. Keep messages under 160 characters where possible.
4. Use short codes instead of long words.
5. Use predefined location codes whenever possible.
6. Use coordinates only when a location code is unavailable.
7. Include a checksum for integrity checking.
8. Include a sequence number for duplicate detection.
9. Do not include sensitive or private data.
10. Convert SMS messages into structured JSON before pushing to Redis.

---

## 3. Protocol Modes

The system supports two modes:

### 3.1 Legacy Demo Mode

Legacy demo mode is simple and readable. It is useful for quick demonstration.

Example:

```text
N|NGO01|RegionA|food|300|H
```

Legacy messages may omit:

- Sequence number
- Checksum
- Compact resource codes
- Location codes

The backend should accept legacy messages for demo compatibility when possible.

### 3.2 Canonical Protocol Mode

Canonical mode is recommended for implementation.

Example:

```text
N|001|NGO01|RA|F|300|H|B3
```

Canonical messages include:

- Message type
- Sequence number
- Organization ID
- Short location code
- Short resource code
- Quantity
- Urgency/status code
- Checksum

---

## 4. Canonical Message Format

Most canonical messages use this structure:

```text
TYPE|SEQ|ORG|BODY|CRC
```

Fields:

| Field | Meaning |
|---|---|
| TYPE | Message type code |
| SEQ | Sequence number |
| ORG | Organization ID |
| BODY | Message-specific fields |
| CRC | Checksum |

Some message types expand the body into fixed fields.

---

## 5. Message Types

| Code | Meaning |
|---|---|
| N | Need request |
| R | Resource availability |
| A | Allocation / plan assignment |
| S | Status update |
| C | Confirmation |
| D | Dispatch |
| V | Delivered |
| X | Cancel |
| M | Map marker |
| P | Polygon chunk |
| ROUTE | Route update |
| RT | Compact route update alias |
| E | Error |

For MVP, prefer:

```text
N, R, A, S, M, P, RT, C, E
```

Legacy shortcuts `D` and `V` may be supported for demo compatibility.

---

## 6. Resource Codes

Use short resource codes.

| Code | Resource |
|---|---|
| F | Food kits |
| W | Water kits |
| M | Medical kits |
| T | Tents |
| B | Blankets |
| H | Hygiene kits |
| D | Medical teams |
| U | Unknown |

Examples:

```text
F = Food kits
M = Medical kits
T = Tents
```

The decoder should also accept common full words for demo compatibility:

```text
food = F
water = W
medical = M
medicine = M
tents = T
tent = T
blankets = B
blanket = B
```

---

## 7. Urgency Codes

| Code | Meaning |
|---|---|
| L | Low |
| M | Medium |
| H | High |
| C | Critical |

Example:

```text
H = High urgency
C = Critical urgency
```

---

## 8. Status Codes

| Code | Meaning |
|---|---|
| 0 | Assigned |
| 1 | Dispatched |
| 2 | In transit |
| 3 | Delivered |
| 4 | Blocked |
| 5 | Cancelled |

Example:

```text
S|004|PLAN101|3|A1
```

Meaning:

```text
Plan PLAN101 is delivered.
```

---

## 9. Resource Availability Status Codes

| Code | Meaning |
|---|---|
| A | Available |
| L | Limited |
| U | Unavailable |

Example:

```text
R|002|CSR02|RA|F|200|A|7C
```

Meaning:

```text
CSR02 has 200 food kits available in Region A.
```

---

## 10. Location Handling

Preferred location format is a predefined location code.

Example location code table:

| Code | Actual Location |
|---|---|
| RA | Region A |
| RB | Region B |
| RC | Region C |
| D1 | District North |
| D2 | District South |

Example:

```text
RA
```

If no location code exists, use decimal coordinates:

```text
23.2599,77.4126
```

Coordinate rules:

- Latitude first, longitude second.
- Use maximum 4 decimal places.
- No spaces.
- Use `-` for negative coordinates.

Example:

```text
23.2599,77.4126
```

For approximate locations, geohash may be used with prefix `GEO:`.

Example:

```text
GEO:te7u2f
```

---

## 11. Need Request

### Legacy Format

```text
N|NGO01|RegionA|food|300|H
```

Meaning:

```text
Need
Organization: NGO01
Location: RegionA
Resource: food
Quantity: 300
Urgency: High
```

### Canonical Format

```text
N|SEQ|ORG|LOC|RESOURCE|QTY|URGENCY|CRC
```

Example:

```text
N|001|NGO01|RA|F|300|H|B3
```

Meaning:

```text
Need request
Sequence: 001
Organization: NGO01
Location: Region A
Resource: Food kits
Quantity: 300
Urgency: High
Checksum: B3
```

Decoded JSON:

```json
{
  "type": "need",
  "seq": "001",
  "organization_id": "NGO01",
  "location_code": "RA",
  "location_name": "Region A",
  "resource": "food_kits",
  "quantity": 300,
  "urgency": "high",
  "checksum": "B3",
  "source": "sms"
}
```

---

## 12. Resource Availability

### Legacy Format

```text
R|CSR02|food|200|A
```

Meaning:

```text
Resource update
Organization: CSR02
Resource: food
Quantity: 200
Status: Available
```

### Canonical Format

```text
R|SEQ|ORG|LOC|RESOURCE|QTY|STATUS|CRC
```

Example:

```text
R|002|CSR02|RA|F|200|A|7C
```

Meaning:

```text
Resource availability
Sequence: 002
Organization: CSR02
Location: Region A
Resource: Food kits
Quantity: 200
Status: Available
Checksum: 7C
```

Decoded JSON:

```json
{
  "type": "resource",
  "seq": "002",
  "organization_id": "CSR02",
  "location_code": "RA",
  "location_name": "Region A",
  "resource": "food_kits",
  "quantity": 200,
  "status": "available",
  "checksum": "7C",
  "source": "sms"
}
```

---

## 13. Allocation / Plan Assignment

### Legacy Format

```text
PLAN001|CSR02|food|200|RegionA|ETA4
```

Meaning:

```text
Plan ID: PLAN001
Assigned organization: CSR02
Resource: food
Quantity: 200
Destination: RegionA
ETA: 4 hours
```

### Canonical Format

```text
A|SEQ|PLAN|ORG|RESOURCE|QTY|LOC|ETA|CRC
```

Example:

```text
A|003|PLAN001|CSR02|F|200|RA|4|D2
```

Meaning:

```text
Allocation message
Sequence: 003
Plan ID: PLAN001
Assigned organization: CSR02
Resource: Food kits
Quantity: 200
Destination: Region A
ETA: 4 hours
Checksum: D2
```

Decoded JSON:

```json
{
  "type": "allocation",
  "seq": "003",
  "plan_id": "PLAN001",
  "organization_id": "CSR02",
  "resource": "food_kits",
  "quantity": 200,
  "destination_code": "RA",
  "destination_name": "Region A",
  "eta_hours": 4,
  "checksum": "D2",
  "source": "sms"
}
```

---

## 14. Status Update

### Canonical Format

```text
S|SEQ|PLAN|STATUS|CRC
```

Example:

```text
S|004|PLAN101|3|A1
```

Meaning:

```text
Status update
Sequence: 004
Plan ID: PLAN101
Status: Delivered
Checksum: A1
```

Decoded JSON:

```json
{
  "type": "status",
  "seq": "004",
  "plan_id": "PLAN101",
  "status": "delivered",
  "checksum": "A1",
  "source": "sms"
}
```

Status examples:

```text
S|005|PLAN101|1|B2
S|006|PLAN101|2|C3
S|007|PLAN101|3|D4
S|008|PLAN101|4|E5
```

Meaning:

```text
Dispatched
In transit
Delivered
Blocked
```

---

## 15. Legacy Delivery Confirmation

Legacy free-text format:

```text
DELIVERED RegionA food 200
```

Meaning:

```text
Delivery confirmation
Location: Region A
Resource: food
Quantity: 200
```

Canonical replacement:

```text
S|009|PLAN101|3|A1
```

If plan ID is unknown, use:

```text
S|009|RA|F|200|3|A1
```

Decoder output:

```json
{
  "type": "status",
  "seq": "009",
  "location_code": "RA",
  "location_name": "Region A",
  "resource": "food_kits",
  "quantity": 200,
  "status": "delivered",
  "checksum": "A1",
  "source": "sms"
}
```

---

## 16. Confirmation

Format:

```text
C|SEQ|REF|RESULT|CRC
```

Example:

```text
C|010|PLAN101|OK|F1
```

Meaning:

```text
Confirmation
Sequence: 010
Reference: PLAN101
Result: OK
Checksum: F1
```

Result codes:

| Code | Meaning |
|---|---|
| OK | Accepted |
| ERR | Rejected |
| DUP | Duplicate ignored |

Decoded JSON:

```json
{
  "type": "confirmation",
  "seq": "010",
  "reference": "PLAN101",
  "result": "ok",
  "checksum": "F1",
  "source": "sms"
}
```

---

## 17. Cancel

Format:

```text
X|SEQ|REF|REASON|CRC
```

Example:

```text
X|011|PLAN101|BLK|A2
```

Meaning:

```text
Cancel message
Sequence: 011
Reference: PLAN101
Reason: Blocked
Checksum: A2
```

Common reason codes:

| Code | Meaning |
|---|---|
| BLK | Blocked |
| NOSTK | No stock |
| RISK | Security risk |
| ROAD | Road issue |
| OTHER | Other |

Decoded JSON:

```json
{
  "type": "cancel",
  "seq": "011",
  "reference": "PLAN101",
  "reason": "blocked",
  "checksum": "A2",
  "source": "sms"
}
```

---

## 18. Map Marker Update

### Legacy Format

```text
M|RA|CRISIS|23.2599,77.4126|SEV9,F300|a1b2
```

Meaning:

```text
Marker message
Region: RA
Type: CRISIS
Coordinates: 23.2599,77.4126
Severity: 9
Need: 300 food kits
Checksum/signature: a1b2
```

### Canonical Format

```text
M|SEQ|LOC|MARKER_TYPE|SEVERITY|DATA|CRC
```

Example using location code:

```text
M|012|RA|CR|9|F300|A1
```

Example using coordinates:

```text
M|013|23.2599,77.4126|CR|9|F300|B4
```

Decoded JSON:

```json
{
  "type": "marker",
  "seq": "013",
  "latitude": 23.2599,
  "longitude": 77.4126,
  "marker_type": "crisis",
  "severity": 9,
  "data": {
    "resource": "food_kits",
    "quantity": 300
  },
  "checksum": "B4",
  "source": "sms"
}
```

---

## 19. Marker Type Codes

| Code | Meaning |
|---|---|
| CR | Crisis zone |
| ND | Need reported |
| RS | Resource point |
| DL | Delivery location |
| BL | Blocked route |
| SH | Shelter |
| MD | Medical point |

Example:

```text
CR = Crisis zone
ND = Need reported
RS = Resource point
```

---

## 20. Marker Data Field

The marker `DATA` field should remain compact.

Examples:

```text
F300
W150
M200
T120
```

Meaning:

```text
F300 = 300 food kits
W150 = 150 water kits
M200 = 200 medical kits
T120 = 120 tents
```

Multiple data items can be separated by `;`.

Example:

```text
F300;W150
```

Full marker example:

```text
M|014|RA|CR|9|F300;W150|C2
```

---

## 21. Polygon Chunk Messages

Use polygon chunks to transmit small crisis zone boundaries.

### Legacy Format

```text
P1/2|RA|FLOOD|23.250,77.400|23.270,77.420|23.260,77.440|e5f6
P2/2|RA|FLOOD|23.240,77.430|END|e7f8
```

### Canonical Format

```text
P|CHUNK/TOTAL|SEQ|LOC|ZONE_TYPE|POINTS|END|CRC
```

Example chunk 1:

```text
P|1/2|015|RA|FLOOD|23.250,77.400;23.270,77.420;23.260,77.440|N|E5
```

Example chunk 2:

```text
P|2/2|016|RA|FLOOD|23.240,77.430|Y|F6
```

Meaning:

```text
Polygon message
Chunk 1 of 2
Chunk 2 of 2, final chunk
END = Y means polygon is complete
```

Polygon rules:

- Use `;` to separate coordinate pairs.
- Use `,` to separate latitude and longitude.
- Use `END=Y` only for the final chunk.
- Use `END=N` for non-final chunks.
- Store chunks in buffer until the final chunk arrives.
- After final chunk, combine all points and draw polygon on offline map.

Decoded polygon JSON:

```json
{
  "type": "polygon",
  "seq": "016",
  "chunk": 2,
  "total_chunks": 2,
  "location_code": "RA",
  "location_name": "Region A",
  "zone_type": "flood",
  "points": [
    [77.400, 23.250],
    [77.420, 23.270],
    [77.440, 23.260],
    [77.430, 23.240]
  ],
  "complete": true,
  "checksum": "F6",
  "source": "sms"
}
```

Important:

For GeoJSON compatibility, store coordinates as:

```text
[longitude, latitude]
```

But in SMS text, keep:

```text
latitude,longitude
```

The decoder should convert to GeoJSON order.

---

## 22. Route Update

### Canonical Format

```text
RT|SEQ|ORG|ROUTE_ID|POINTS|CRC
```

Example:

```text
RT|017|NGO01|RT1|23.250,77.400;23.260,77.410;23.270,77.420|A3
```

Meaning:

```text
Route update
Sequence: 017
Organization: NGO01
Route ID: RT1
Waypoints: three coordinate points
Checksum: A3
```

Alternative route type:

```text
ROUTE|017|NGO01|RT1|23.250,77.400;23.260,77.410;23.270,77.420|A3
```

Decoded JSON:

```json
{
  "type": "route",
  "seq": "017",
  "organization_id": "NGO01",
  "route_id": "RT1",
  "points": [
    [77.400, 23.250],
    [77.410, 23.260],
    [77.420, 23.270]
  ],
  "checksum": "A3",
  "source": "sms"
}
```

Route rules:

- Use `;` to separate waypoints.
- Use latitude,longitude order in SMS.
- Convert to GeoJSON `[longitude, latitude]` after decoding.
- Keep routes small.
- Do not send full navigation paths over SMS.

---

## 23. Error Message

Format:

```text
E|SEQ|CODE|MSG|CRC
```

Example:

```text
E|018|BAD_CRC|INVALID_CHECKSUM|F1
```

Meaning:

```text
Error message
Sequence: 018
Error code: BAD_CRC
Message: Invalid checksum
Checksum: F1
```

Common error codes:

| Code | Meaning |
|---|---|
| BAD_CRC | Checksum failed |
| BAD_FMT | Invalid format |
| UNKNOWN_TYPE | Unknown message type |
| UNKNOWN_RES | Unknown resource code |
| UNKNOWN_LOC | Unknown location code |
| DUP | Duplicate message |
| TOO_LONG | Message too long |
| PRIVACY | Sensitive content rejected |

---

## 24. Checksum Rule

Every canonical SMS message should include a checksum.

The checksum is the last field.

Example message before checksum:

```text
N|001|NGO01|RA|F|300|H
```

Final message:

```text
N|001|NGO01|RA|F|300|H|B3
```

Checksum rules:

- Use 2 uppercase hex characters.
- Calculate checksum over the message before the final checksum field.
- If checksum validation fails, reject the message.
- Do not push rejected messages into the agent queue.

For hackathon MVP, use a simple XOR checksum.

Example:

```python
def xor_checksum(text: str) -> str:
    value = 0
    for char in text:
        value ^= ord(char)
    return format(value, "02X")
```

Example usage:

```python
message = "N|001|NGO01|RA|F|300|H"
checksum = xor_checksum(message)
final_message = f"{message}|{checksum}"
```

Note:

Example checksums in this document may be illustrative. The implementation should calculate checksums dynamically.

---

## 25. Sequence Numbers

Every canonical message must contain a sequence number.

Recommended format:

```text
001
002
003
...
999
```

If more messages are needed, use 4 digits:

```text
0001
0002
```

Duplicate protection rule:

Store:

```text
organization_id + sequence_number
```

If the same combination is received again, ignore it.

Optional confirmation for duplicate:

```text
C|019|001|DUP|B2
```

Meaning:

```text
Message 001 was already processed.
```

---

## 26. Decoder Validation Rules

When an SMS is received, the decoder must:

1. Trim whitespace.
2. Split by `|`.
3. Detect legacy or canonical format.
4. Check minimum field count.
5. Validate checksum if present.
6. Validate message type.
7. Map short codes to full values.
8. Convert quantity to integer.
9. Convert severity to integer.
10. Parse location code or coordinates.
11. Reject invalid messages.
12. Ignore duplicates.
13. Push valid message to Redis queue.

---

## 27. Decoder Output Format

The SMS decoder must convert SMS into structured JSON before pushing to Redis.

Example SMS:

```text
N|001|NGO01|RA|F|300|H|B3
```

Decoder output:

```json
{
  "type": "need",
  "seq": "001",
  "organization_id": "NGO01",
  "location_code": "RA",
  "location_name": "Region A",
  "resource": "food_kits",
  "quantity": 300,
  "urgency": "high",
  "checksum": "B3",
  "source": "sms"
}
```

All decoded SMS messages must include:

```json
"source": "sms"
```

This helps the backend distinguish SMS inputs from web dashboard inputs.

---

## 28. Encoder Rules

The encoder must:

1. Accept structured JSON.
2. Replace long values with mapped codes.
3. Reduce location names to location codes.
4. Reduce resource names to resource codes.
5. Reduce urgency values to urgency codes.
6. Build pipe-delimited string.
7. Calculate checksum.
8. Return final SMS string.

Example input:

```json
{
  "type": "need",
  "organization_id": "NGO01",
  "location": "Region A",
  "resource": "food_kits",
  "quantity": 300,
  "urgency": "high"
}
```

Encoded output:

```text
N|001|NGO01|RA|F|300|H|B3
```

---

## 29. Coordinate Encoding Policy

Use this priority order.

### Priority 1: Location Code

```text
RA
```

Best for demo and shortest message size.

### Priority 2: Decimal Coordinates

```text
23.2599,77.4126
```

Best when an exact point is needed and location code is unavailable.

Recommended for hackathon MVP.

### Priority 3: Geohash

```text
GEO:te7u2f
```

Use only if approximate location is acceptable.

Example:

```text
M|020|GEO:te7u2f|CR|8|F200|C3
```

### Priority 4: Hex Coordinates

Hex coordinates are optional and not recommended by default.

Use hex only if:

- Binary SMS is available.
- Both encoder and decoder support it.
- Message size must be aggressively minimized.
- Debugging complexity is acceptable.

---

## 30. Optional Hex Coordinate Format

Hex coordinate format is optional.

Format:

```text
M|SEQ|HX:HEXCOORD|MARKER_TYPE|SEVERITY|DATA|CRC
```

Example:

```text
M|021|HX:0DDBF6D82E22A1B0|CR|9|F300|A1
```

Encoding rule:

```text
lat_int = round(latitude * 10000000)
lon_int = round(longitude * 10000000)

lat_hex = 8 uppercase hex characters
lon_hex = 8 uppercase hex characters

hex_coord = lat_hex + lon_hex
```

Example:

```text
latitude = 23.2599
longitude = 77.4126

lat_int = 232599000
lon_int = 774126000

lat_hex = 0DDBF6D8
lon_hex = 2E22A1B0

hex_coord = 0DDBF6D82E22A1B0
```

Decoding rule:

```text
lat_hex = first 8 characters
lon_hex = next 8 characters

latitude = int(lat_hex, 16) / 10000000
longitude = int(lon_hex, 16) / 10000000
```

Hex coordinate policy:

- Do not use hex coordinates in the main demo unless necessary.
- Use decimal coordinates for readability.
- Use hex only as an optional advanced mode.

---

## 31. Privacy Rules for SMS

SMS messages must not contain sensitive data.

Do not send:

- Donor names
- Funding details
- Staff names
- Volunteer names
- Beneficiary personal data
- Exact warehouse locations if sensitive
- Private logistics routes
- Internal operational plans
- Full inventory data
- Security-sensitive details

Only send:

- Organization ID
- Resource type
- Approximate quantity
- Location code or approximate coordinates
- Urgency
- Status
- Plan ID
- Checksum

Safe example:

```text
N|001|NGO01|RA|F|300|H|B3
```

Unsafe example:

```text
N|NGO01|John Smith|Warehouse 5|Donor XYZ|food|300|H
```

Reject unsafe SMS content if detected.

---

## 32. SMS Size Rules

Target message size:

```text
< 160 characters
```

Hard limit for hackathon MVP:

```text
160 characters
```

If message exceeds limit:

1. Split polygon messages into chunks.
2. Reduce coordinate precision.
3. Use location codes.
4. Remove optional fields.
5. Reject overly large messages.

Do not send multi-part SMS unless required for polygon chunks.

---

## 33. Recommended Message Examples

### Need request

```text
N|001|NGO01|RA|F|300|H|B3
```

### Resource availability

```text
R|002|CSR02|RA|F|200|A|7C
```

### Allocation

```text
A|003|PLAN101|CSR02|F|200|RA|4|D2
```

### Status update

```text
S|004|PLAN101|3|A1
```

### Confirmation

```text
C|005|PLAN101|OK|F1
```

### Cancel

```text
X|006|PLAN101|BLK|A2
```

### Marker using location code

```text
M|007|RA|CR|9|F300|A1
```

### Marker using coordinates

```text
M|008|23.2599,77.4126|CR|9|F300|B4
```

### Polygon chunk 1

```text
P|1/2|009|RA|FLOOD|23.250,77.400;23.270,77.420;23.260,77.440|N|E5
```

### Polygon chunk 2

```text
P|2/2|010|RA|FLOOD|23.240,77.430|Y|F6
```

### Route update

```text
RT|011|NGO01|RT1|23.250,77.400;23.260,77.410;23.270,77.420|A3
```

### Error

```text
E|012|BAD_CRC|INVALID_CHECKSUM|F1
```

---

## 34. SMS Simulator Requirements

The web dashboard should include an SMS simulator panel.

The simulator should allow users to:

1. Enter an SMS payload.
2. Send it to the backend.
3. View decoded JSON.
4. View validation errors.
5. View agent response.
6. Update dashboard state.
7. Update map markers if applicable.

Example simulator input:

```text
N|001|NGO01|RA|F|300|H|B3
```

Expected simulator result:

```text
SMS accepted
Decoded as need request
Pushed to Redis queue
Need Assessment Agent processing
```

Legacy simulator input:

```text
N|NGO01|RegionA|food|300|H
```

Expected backend behavior:

```text
Accept legacy demo format
Normalize to canonical JSON
Push to Redis queue
```

---

## 35. Android App SMS Behavior

The Android app should:

1. Detect internet availability.
2. If internet is available, send data to FastAPI backend.
3. If internet is unavailable, convert message to SMS payload.
4. Queue SMS locally if sending fails.
5. Parse received SMS payloads.
6. Update offline UI.
7. Update cached MapLibre map.
8. Sync local queue when internet returns.

Important:

Android is required because Android allows programmatic SMS sending and receiving. iOS has strong SMS restrictions.

---

## 36. Offline Map Behavior

SMS cannot send map tiles.

Map tiles or vector tiles must be pre-cached inside the app.

Offline map flow:

```text
App uses cached map tiles
        |
        v
App receives SMS coordinate update
        |
        v
App parses SMS
        |
        v
App adds marker, polygon, or route
        |
        v
App updates cached map view
```

SMS can update:

- Single point coordinates
- Marker type
- Severity
- Small status codes
- Polygon chunks
- Route waypoints

SMS cannot update:

- Map tiles
- Large GeoJSON files
- High-resolution imagery
- Full map packages

---

## 37. Redis Integration

Valid decoded SMS messages should be pushed to Redis queues.

Example queues:

```text
sms_incoming_queue
need_assessment_queue
resource_matching_queue
coordination_queue
replanning_queue
sms_outgoing_queue
```

Example flow:

```text
SMS received
    |
    v
SMS parser validates message
    |
    v
Decoder converts SMS to JSON
    |
    v
Message pushed to sms_incoming_queue
    |
    v
Need Assessment Agent consumes message
    |
    v
Resource Matching Agent processes need
    |
    v
Coordination Agent creates plan
    |
    v
Backend sends SMS response if required
```

---

## 38. MVP Implementation Order

Implement in this order:

1. Need request encoding/decoding
2. Resource availability encoding/decoding
3. Allocation encoding/decoding
4. Status update encoding/decoding
5. Marker update encoding/decoding
6. XOR checksum
7. SMS simulator panel
8. Decoder to JSON
9. Push decoded message to Redis queue
10. Offline map marker update from decoded SMS

Do not prioritize these first:

- Full binary SMS
- Hex coordinate encoding
- Advanced cryptography
- Complex multi-part reconstruction
- Production telecom gateway integration
- Full routing engine

---

## 39. Final SMS Strategy

Use:

```text
Short text protocol + mapped codes + pipe delimiter + checksum
```

Use coordinate strategy:

```text
Location code first, decimal coordinates second, geohash optional, hex not default
```

Recommended demo need message:

```text
N|001|NGO01|RA|F|300|H|B3
```

Recommended demo marker message:

```text
M|008|23.2599,77.4126|CR|9|F300|B4
```

This keeps the SMS fallback simple, privacy-aware, demo-friendly, and feasible within a 24-hour hackathon.
```

---

<a id="file-requirements-txt"></a>
## File: `requirements.txt`

```text
fastapi>=0.115.0
uvicorn>=0.30.0
pydantic>=2.8.0
websockets>=12.0
groq>=0.9.0
motor>=3.5.0
pymongo>=4.8.0
mongomock>=4.1.2
httpx>=0.27.0
pytest>=8.0.0
pytest-asyncio>=0.23.0
python-multipart>=0.0.9
requests>=2.31.0
```

---

<a id="file-start_server-sh"></a>
## File: `start_server.sh`

```bash
#!/usr/bin/env bash
set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

if [ ! -d "venv" ]; then
    echo "[*] Creating virtual environment..."
    python3 -m venv venv
    ./venv/bin/pip install -r requirements.txt
fi

echo "[*] Starting PACT Server on port 8000..."
exec ./venv/bin/python3 run_server.py
```

---

<a id="file-run_server-py"></a>
## File: `run_server.py`

```python
#!/usr/bin/env python3
"""
PACT Platform Server Launcher.
Runs the FastAPI application on Uvicorn.
"""

import uvicorn
import os
from app.config import HOST, PORT

if __name__ == "__main__":
    print("=" * 65)
    print("PACT: PRIVACY-PRESERVING MULTI-AGENT COORDINATION PLATFORM")
    print(f"Server starting on http://{HOST}:{PORT}")
    print(f"Admin Command Portal: http://localhost:{PORT}")
    print(f"Interactive API Docs: http://localhost:{PORT}/docs")
    print(f"WebSocket Live Stream: ws://localhost:{PORT}/ws/agents")
    print("=" * 65)
    uvicorn.run("app.main:app", host=HOST, port=PORT, reload=False, log_level="info")
```

---

<a id="file-app-config-py"></a>
## File: `app/config.py`

```python
"""
PACT Configuration Module.
Loads environment settings with sensible defaults for 24-hr hackathon resilience.
Automatically loads key-value pairs from .env if present.
"""

import os
from pathlib import Path


def load_dotenv():
    """Simple built-in .env file loader without external dependencies."""
    env_path = Path(__file__).resolve().parent.parent / ".env"
    if env_path.exists():
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                k = k.strip()
                v = v.strip().strip("'\"")
                if k and k not in os.environ:
                    os.environ[k] = v


load_dotenv()

GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL: str = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")

MONGODB_URI: str = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
DATABASE_NAME: str = os.getenv("DATABASE_NAME", "pact_db")

# Autopilot settings
AUTOPILOT_ENABLED: bool = os.getenv("AUTOPILOT_ENABLED", "true").lower() in ("true", "1", "yes")
AUTOPILOT_TIMEOUT_SECONDS: float = float(os.getenv("AUTOPILOT_TIMEOUT_SECONDS", "3.0"))

# Network & Server
HOST: str = os.getenv("HOST", "0.0.0.0")
PORT: int = int(os.getenv("PORT", "8000"))
DEBUG: bool = os.getenv("DEBUG", "true").lower() in ("true", "1", "yes")
```

---

<a id="file-app-main-py"></a>
## File: `app/main.py`

```python
"""
PACT: Privacy-Preserving Multi-Agent Humanitarian Coordination Platform.
FastAPI Server Entry Point.
"""

from contextlib import asynccontextmanager
import os
import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse

from app.config import HOST, PORT, DEBUG
from app.db.mongo import db_manager
from app.db.indexes import ensure_indexes
from app.db.seed import seed_database
from app.api import api_router, ws_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("pact.main")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Initializing PACT Multi-Agent Coordination Server...")
    await db_manager.connect()
    await ensure_indexes()
    await seed_database(force=True)
    logger.info("PACT server initialization complete. Ready for live emergency traffic.")
    yield
    # Shutdown
    logger.info("Shutting down PACT server...")


app = FastAPI(
    title="PACT Humanitarian Coordination Platform",
    description="Privacy-Preserving Multi-Agent Emergency Dispatch & GSM-7 SMS Protocol Server",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API and WebSocket routers
app.include_router(api_router)
app.include_router(ws_router)

# Mount Static Files
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get("/api/v1/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "pact-coordination-server",
        "version": "1.0.0",
        "is_mock_db": db_manager.is_mock()
    }


@app.get("/", include_in_schema=False)
async def serve_index():
    """Serves the Admin Command Portal single-page application."""
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return JSONResponse({
        "service": "PACT Humanitarian Coordination Server",
        "docs": "/docs",
        "websocket": "/ws/agents",
        "ingest": "/api/v1/pact/ingest"
    })
```

---

<a id="file-app-codec-base36-py"></a>
## File: `app/codec/base36.py`

```python
"""
Base-36 encoding and decoding utilities for compact integer token serialization.
Standard uppercase alphabet: 0-9, A-Z (radix 36).
"""

BASE36_ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
BASE36_MAP = {char: idx for idx, char in enumerate(BASE36_ALPHABET)}


def base36_encode(number: int, min_length: int = 0) -> str:
    """
    Encodes a non-negative integer into a Base-36 uppercase string.
    Optional min_length pads with leading zeros.
    """
    if number < 0:
        raise ValueError(f"Cannot encode negative integer {number} in base36")
    if number == 0:
        encoded = "0"
    else:
        chars = []
        n = number
        while n > 0:
            n, rem = divmod(n, 36)
            chars.append(BASE36_ALPHABET[rem])
        encoded = "".join(reversed(chars))

    if min_length > 0 and len(encoded) < min_length:
        encoded = encoded.zfill(min_length)
    return encoded


def base36_decode(s: str) -> int:
    """
    Decodes a Base-36 string (case-insensitive) into an integer.
    """
    if not s:
        raise ValueError("Cannot decode empty string in base36")
    s_upper = s.upper()
    val = 0
    for char in s_upper:
        if char not in BASE36_MAP:
            raise ValueError(f"Invalid Base-36 character '{char}' in '{s}'")
        val = val * 36 + BASE36_MAP[char]
    return val
```

---

<a id="file-app-codec-pack10-py"></a>
## File: `app/codec/pack10.py`

```python
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
```

---

<a id="file-app-codec-checksum-py"></a>
## File: `app/codec/checksum.py`

```python
"""
XOR Checksum algorithm for the PACT protocol.
Calculates 2-character uppercase hexadecimal XOR checksum over ASCII characters.
"""

def calculate_xor_checksum(text: str) -> str:
    """
    Calculates 2-digit uppercase hex XOR checksum over raw ASCII frame.
    Example:
        calculate_xor_checksum("Q|001|7F3K|15223C03Q0|6QR6VFBQ33") -> "7F"
    """
    val = 0
    for char in text:
        val ^= ord(char)
    return format(val, "02X")


def verify_checksum(full_frame: str) -> bool:
    """
    Verifies the trailing 2-digit checksum in a pipe-delimited frame.
    Returns True if valid, False if invalid or corrupt.
    """
    trimmed = full_frame.strip()
    if "|" not in trimmed:
        return False
    parts = trimmed.rsplit("|", 1)
    if len(parts) != 2:
        return False
    body, expected_crc = parts[0], parts[1].strip()
    computed_crc = calculate_xor_checksum(body)
    return computed_crc.upper() == expected_crc.upper()


def append_checksum(body: str) -> str:
    """
    Computes XOR checksum for body and returns 'body|CRC'.
    """
    crc = calculate_xor_checksum(body)
    return f"{body}|{crc}"
```

---

<a id="file-app-codec-taxonomy-py"></a>
## File: `app/codec/taxonomy.py`

```python
"""
Taxonomy and bitfield definitions for PACT Base-36 Codec and SMS Protocol.
Governs requester situations, headcount estimations, injuries, mobility,
12-bit resources bitfield, 5-bit vulnerability bitfield, and provider metadata.
"""

from typing import Dict, List, Any

# Situation Types (pos 1 of Requester Frame)
SITUATIONS: Dict[str, Dict[str, Any]] = {
    "0": {"code": "GEN", "name": "General Emergency", "icon": "⚠️", "severity_base": 5},
    "1": {"code": "FLD", "name": "Flood / Rising Water", "icon": "🌊", "severity_base": 7},
    "2": {"code": "EQK", "name": "Earthquake / Tremor", "icon": "🏚️", "severity_base": 8},
    "3": {"code": "COL", "name": "Building Collapse", "icon": "🏢", "severity_base": 9},
    "4": {"code": "FIR", "name": "Fire / Explosion", "icon": "🔥", "severity_base": 8},
    "5": {"code": "LND", "name": "Landslide / Mudslide", "icon": "⛰️", "severity_base": 7},
    "6": {"code": "CYC", "name": "Cyclone / Hurricane", "icon": "🌀", "severity_base": 8},
    "7": {"code": "MED", "name": "Medical Outbreak / Epidemic", "icon": "🏥", "severity_base": 7},
    "8": {"code": "PWR", "name": "Severe Infrastructure Outage", "icon": "🔌", "severity_base": 5},
    "9": {"code": "CHM", "name": "Chemical / Gas Leak", "icon": "☣️", "severity_base": 9},
    "A": {"code": "TSU", "name": "Tsunami", "icon": "🌊", "severity_base": 10},
    "B": {"code": "WNT", "name": "Severe Winter Storm / Cold", "icon": "❄️", "severity_base": 6},
}

# Headcount Buckets (pos 2 of Requester Frame)
HEADCOUNTS: Dict[str, Dict[str, Any]] = {
    "0": {"label": "1 person", "min": 1, "max": 1, "est": 1},
    "1": {"label": "2 people", "min": 2, "max": 2, "est": 2},
    "2": {"label": "3-4 people", "min": 3, "max": 4, "est": 3},
    "3": {"label": "5-8 people", "min": 5, "max": 8, "est": 6},
    "4": {"label": "9-15 people", "min": 9, "max": 15, "est": 12},
    "5": {"label": "16-30 people", "min": 16, "max": 30, "est": 23},
    "6": {"label": "31-50 people", "min": 31, "max": 50, "est": 40},
    "7": {"label": "51-100 people", "min": 51, "max": 100, "est": 75},
    "8": {"label": "101-200 people", "min": 101, "max": 200, "est": 150},
    "9": {"label": "201-500 people", "min": 201, "max": 500, "est": 350},
    "A": {"label": "500+ people", "min": 500, "max": 2000, "est": 600},
}

# Injury Severity (pos 3 of Requester Frame)
INJURIES: Dict[str, Dict[str, Any]] = {
    "0": {"code": "NONE", "label": "No Injuries / Uninjured", "score": 0},
    "1": {"code": "MIN", "label": "Minor / Ambulatory", "score": 2},
    "2": {"code": "SER", "label": "Serious / Non-ambulatory", "score": 6},
    "3": {"code": "CRT", "label": "Critical / Life-Threatening", "score": 9},
    "4": {"code": "FAT", "label": "Fatalities Present", "score": 10},
}

# Mobility / Entrapment (pos 4 of Requester Frame)
MOBILITY: Dict[str, Dict[str, Any]] = {
    "0": {"code": "MOB", "label": "Fully Mobile", "score": 0},
    "1": {"code": "IMP", "label": "Impeded / Blocked Routes", "score": 3},
    "2": {"code": "TRP", "label": "Trapped in Structure / Rubble", "score": 8},
    "3": {"code": "WTR", "label": "Waterbound / Isolated", "score": 7},
    "4": {"code": "ROF", "label": "Rooftop / Elevated", "score": 6},
    "5": {"code": "BSM", "label": "Underground / Basement", "score": 8},
}

# Urgency Codes (pos 5 of Requester Frame)
URGENCY: Dict[str, Dict[str, Any]] = {
    "L": {"label": "Low", "rank": 1, "color": "#10B981"},
    "M": {"label": "Medium", "rank": 2, "color": "#F59E0B"},
    "H": {"label": "High", "rank": 3, "color": "#F97316"},
    "C": {"label": "Critical", "rank": 4, "color": "#EF4444"},
}

# 12-Bit Resources Taxonomy (Shared across Needs and Provider Inventory)
RESOURCES: List[Dict[str, Any]] = [
    {"bit": 0, "code": "F", "key": "food_kits", "label": "Food Kits", "unit": "kits", "per_person_ratio": 1.0},
    {"bit": 1, "code": "W", "key": "water_kits", "label": "Water Kits", "unit": "liters/kits", "per_person_ratio": 2.0},
    {"bit": 2, "code": "M", "key": "medical_kits", "label": "Medical Kits", "unit": "kits", "per_person_ratio": 0.5},
    {"bit": 3, "code": "T", "key": "tents", "label": "Tents / Shelter", "unit": "units", "per_person_ratio": 0.25},
    {"bit": 4, "code": "B", "key": "blankets", "label": "Blankets / Warmth", "unit": "units", "per_person_ratio": 1.0},
    {"bit": 5, "code": "H", "key": "hygiene_kits", "label": "Hygiene Kits", "unit": "kits", "per_person_ratio": 0.5},
    {"bit": 6, "code": "X", "key": "rescue_team", "label": "Search & Rescue Squad", "unit": "teams", "per_person_ratio": 0.1},
    {"bit": 7, "code": "V", "key": "evac_transport", "label": "Evacuation Transport", "unit": "vehicles", "per_person_ratio": 0.2},
    {"bit": 8, "code": "P", "key": "power_kits", "label": "Power / Generator Kits", "unit": "generators", "per_person_ratio": 0.05},
    {"bit": 9, "code": "I", "key": "infant_kits", "label": "Infant & Baby Kits", "unit": "kits", "per_person_ratio": 0.3},
    {"bit": 10, "code": "D", "key": "medical_team", "label": "Doctor / Medical Field Team", "unit": "teams", "per_person_ratio": 0.1},
    {"bit": 11, "code": "E", "key": "heavy_equipment", "label": "Heavy Clearance Equipment", "unit": "machines", "per_person_ratio": 0.05},
]

RESOURCE_BY_CODE = {r["code"]: r for r in RESOURCES}
RESOURCE_BY_KEY = {r["key"]: r for r in RESOURCES}
RESOURCE_BY_BIT = {r["bit"]: r for r in RESOURCES}

# 5-Bit Vulnerability Bitfield (pos 9 of Requester Frame)
VULNERABILITIES: List[Dict[str, Any]] = [
    {"bit": 0, "code": "INF", "label": "Infants / Children under 5", "weight": 2.0},
    {"bit": 1, "code": "ELD", "label": "Elderly (65+)", "weight": 1.5},
    {"bit": 2, "code": "PRG", "label": "Pregnant Women", "weight": 2.0},
    {"bit": 3, "code": "DIS", "label": "Disabled / Mobility Impaired", "weight": 1.5},
    {"bit": 4, "code": "CHR", "label": "Chronic Condition / Dialysis / O2", "weight": 2.5},
]

# Provider Metadata Lookups
PROVIDER_ORG_TYPES: Dict[str, Dict[str, Any]] = {
    "N": {"code": "NGO", "label": "Non-Governmental Org (NGO)", "fleet_type": "all-terrain vans"},
    "G": {"code": "GOV", "label": "Government Agency / NDRF", "fleet_type": "heavy rescue trucks"},
    "C": {"code": "CSR", "label": "Corporate CSR Fleet", "fleet_type": "commercial logistics"},
    "V": {"code": "VOL", "label": "Local Community Volunteers", "fleet_type": "4x4 light vehicles"},
    "M": {"code": "MIL", "label": "Military / Civil Defense", "fleet_type": "amphibious / helicopters"},
    "P": {"code": "HOS", "label": "Private Hospital / Clinic", "fleet_type": "ambulances"},
    "I": {"code": "INT", "label": "International Aid Agency", "fleet_type": "container transports"},
    "R": {"code": "RED", "label": "Red Cross / Red Crescent", "fleet_type": "mobile emergency units"},
}

CAPACITY_BUCKETS: Dict[str, int] = {
    "0": 10,
    "1": 50,
    "2": 100,
    "3": 250,
    "4": 500,
    "5": 1000,
    "6": 2500,
    "7": 5000,
    "8": 10000,
}

RADIUS_BUCKETS: Dict[str, int] = {
    "0": 5,
    "1": 10,
    "2": 25,
    "3": 50,
    "4": 100,
    "5": 150,
    "6": 250,
    "7": 500,
}

ETA_BUCKETS: Dict[str, float] = {
    "0": 0.5,
    "1": 1.0,
    "2": 2.0,
    "3": 4.0,
    "4": 8.0,
    "5": 12.0,
    "6": 24.0,
    "7": 48.0,
}

PROVIDER_AVAILABILITY: Dict[str, str] = {
    "A": "available",
    "L": "limited",
    "U": "unavailable",
}

STATUS_CODES: Dict[str, str] = {
    "0": "assigned",
    "1": "dispatched",
    "2": "in_transit",
    "3": "delivered",
    "4": "blocked",
    "5": "cancelled",
    "6": "self_resolved",
    "7": "still_waiting",
}
```

---

<a id="file-app-codec-canonical_codec-py"></a>
## File: `app/codec/canonical_codec.py`

```python
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
```

---

<a id="file-app-codec-requester_codec-py"></a>
## File: `app/codec/requester_codec.py`

```python
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
```

---

<a id="file-app-codec-provider_codec-py"></a>
## File: `app/codec/provider_codec.py`

```python
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
```

---

<a id="file-app-codec-fanout-py"></a>
## File: `app/codec/fanout.py`

```python
"""
Q -> N Fan-out Converter.
Converts a citizen emergency request (Q) into discrete need items (N),
computing resource kit quantities based on headcount estimates and vulnerability weights.
"""

import math
from typing import Dict, Any, List
from app.codec.taxonomy import RESOURCES, RESOURCE_BY_KEY


def q_to_n_fanout(decoded_q: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Fans out a single decoded Q request into a list of normalized Need records.
    Each set need bit produces one need item with estimated quantity.
    """
    payload = decoded_q.get("payload", {})
    headcount_est = payload.get("people_estimate", 1)
    needed_resources = payload.get("needed_resources", [])
    urgency_label = payload.get("urgency", {}).get("label", "Medium")
    urgency_code = payload.get("urgency_code", "M")
    uid = decoded_q.get("uid", "CIT00")
    geo = decoded_q.get("geo", {})
    coords = geo.get("coordinates", [77.4126, 23.2599])

    # Vulnerability multipliers
    vulnerabilities = payload.get("vulnerabilities", [])
    has_infants = any(v.get("code") == "INF" for v in vulnerabilities)
    has_elderly = any(v.get("code") == "ELD" for v in vulnerabilities)

    need_items = []

    for res in needed_resources:
        key = res["key"]
        code = res["code"]
        ratio = res.get("per_person_ratio", 1.0)

        # Quantity calculation based on resource type
        if key == "food_kits":
            qty = max(1, math.ceil(headcount_est * ratio))
        elif key == "water_kits":
            qty = max(2, math.ceil(headcount_est * ratio))
        elif key == "medical_kits":
            qty = max(1, math.ceil(headcount_est * ratio))
        elif key == "tents":
            qty = max(1, math.ceil(headcount_est * ratio))
        elif key == "blankets":
            qty = max(1, math.ceil(headcount_est * ratio * (1.5 if has_elderly else 1.0)))
        elif key == "hygiene_kits":
            qty = max(1, math.ceil(headcount_est * ratio))
        elif key == "infant_kits":
            qty = max(1, 2 if has_infants else 1)
        elif key in ("rescue_team", "medical_team", "heavy_equipment", "power_kits"):
            qty = 1
        elif key == "evac_transport":
            qty = max(1, math.ceil(headcount_est / 4.0))
        else:
            qty = max(1, math.ceil(headcount_est * ratio))

        need_items.append({
            "need_id": f"ND_{uid}_{code}",
            "uid": uid,
            "organization_id": f"CITIZEN_{uid}",
            "resource_code": code,
            "resource_key": key,
            "resource_label": res["label"],
            "unit": res["unit"],
            "quantity": qty,
            "urgency": urgency_label.lower(),
            "urgency_code": urgency_code,
            "location_coordinates": coords,
            "source": "q_fanout",
            "people_count": headcount_est,
            "situation": payload.get("situation", {}).get("name", "Emergency")
        })

    return need_items
```

---

<a id="file-app-db-models-py"></a>
## File: `app/db/models.py`

```python
"""
Pydantic Schemas and DB Models for PACT Platform.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
import time


class GeoLocation(BaseModel):
    type: str = "Point"
    coordinates: List[float] = Field(..., description="[longitude, latitude]")
    accuracy_m: Optional[int] = 5
    pack10: Optional[str] = None
    location_code: Optional[str] = None
    location_name: Optional[str] = None


class CitizenRequestCreate(BaseModel):
    uid: str
    seq: str = "001"
    raw_frame: Optional[str] = None
    situation_code: str = "3"
    headcount_code: str = "2"
    injury_code: str = "2"
    mobility_code: str = "2"
    urgency_code: str = "C"
    needs_keys: List[str] = ["water_kits", "medical_kits", "evac_transport"]
    vulnerability_bits: List[int] = []
    latitude: float = 23.25991
    longitude: float = 77.41263


class ProviderOfferCreate(BaseModel):
    provider_id: str
    organization_name: str
    org_type_code: str = "N"
    offered_resource_keys: List[str] = ["food_kits", "water_kits", "medical_kits", "evac_transport"]
    capacity_code: str = "4"
    radius_code: str = "3"
    eta_code: str = "2"
    availability_code: str = "A"
    latitude: float = 23.2650
    longitude: float = 77.4050
    stock: Dict[str, int] = Field(default_factory=dict)
    contact_phone: Optional[str] = "+919876543210"


class IngestWirePayload(BaseModel):
    text: Optional[str] = None
    body: Optional[str] = None
    Body: Optional[str] = None
    sender: Optional[str] = None
    From: Optional[str] = None
    from_: Optional[str] = Field(default=None, alias="from")
    transport: str = "http"


class AdminActionRequest(BaseModel):
    decision_id: str
    action: str = Field(..., description="approve | override | reject")
    override_option_id: Optional[str] = None
    pinned_provider_id: Optional[str] = None
    reject_reason: Optional[str] = None
    dispatcher_notes: Optional[str] = None


class DecisionOption(BaseModel):
    option_id: str  # fastest | max_coverage | least_depleting
    title: str
    description: str
    allocations: List[Dict[str, Any]]
    total_fulfilled: Dict[str, int]
    coverage_ratio: float
    max_eta_hours: float
    depletion_impact: str


class MatchRecord(BaseModel):
    match_id: str
    request_id: str
    run_id: str
    status: str = "committed"  # pending_admin, approved, committed, dispatched, delivered, rejected
    selected_option_id: str
    chosen_option: Dict[str, Any]
    triage_info: Dict[str, Any]
    created_at: float = Field(default_factory=time.time)
    masked: bool = True
    revealed: bool = False
    sms_ack_sent: Optional[str] = None
    provider_allocations: List[Dict[str, Any]] = Field(default_factory=list)
```

---

<a id="file-app-db-mongo-py"></a>
## File: `app/db/mongo.py`

```python
"""
MongoDB Database Client with Seamless In-Memory Mock Fallback.
Provides async collection access, 2dsphere indexing, and $geoNear simulation.
"""

import math
import time
import logging
from typing import Dict, Any, List, Optional
from app.config import MONGODB_URI, DATABASE_NAME

logger = logging.getLogger("pact.db")


def haversine_distance_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculates great-circle distance between two points in meters."""
    R = 6371000.0  # Earth radius in meters
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2.0) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0) ** 2
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return R * c


class MockCursor:
    """Async cursor wrapper for in-memory collections."""
    def __init__(self, items: List[Dict[str, Any]]):
        self._items = list(items)

    def sort(self, key_or_list, direction=1):
        if isinstance(key_or_list, list):
            for k, d in reversed(key_or_list):
                self._items.sort(key=lambda x: x.get(k, 0), reverse=(d == -1))
        elif isinstance(key_or_list, str):
            self._items.sort(key=lambda x: x.get(key_or_list, 0), reverse=(direction == -1))
        return self

    def limit(self, n: int):
        self._items = self._items[:n]
        return self

    async def to_list(self, length: Optional[int] = None) -> List[Dict[str, Any]]:
        if length is not None:
            return self._items[:length]
        return self._items

    def __aiter__(self):
        self._iter = iter(self._items)
        return self

    async def __anext__(self):
        try:
            return next(self._iter)
        except StopIteration:
            raise StopAsyncIteration


class MockCollection:
    """Thread-safe and async-compatible in-memory MongoDB collection mock."""
    def __init__(self, name: str):
        self.name = name
        self.docs: List[Dict[str, Any]] = []

    def _matches(self, doc: Dict[str, Any], query: Dict[str, Any]) -> bool:
        for k, v in query.items():
            if k == "$or" and isinstance(v, list):
                if not any(self._matches(doc, q) for q in v):
                    return False
                continue
            if isinstance(v, dict):
                doc_val = doc.get(k)
                for op, target in v.items():
                    if op == "$in" and doc_val not in target:
                        return False
                    if op == "$ne" and doc_val == target:
                        return False
                    if op == "$gte" and (doc_val is None or doc_val < target):
                        return False
                    if op == "$lte" and (doc_val is None or doc_val > target):
                        return False
            else:
                if doc.get(k) != v:
                    return False
        return True

    async def insert_one(self, doc: Dict[str, Any]):
        d = dict(doc)
        if "_id" not in d:
            d["_id"] = f"{self.name}_{len(self.docs)+1}_{int(time.time()*1000)}"
        self.docs.append(d)
        return type("InsertResult", (), {"inserted_id": d["_id"]})()

    async def insert_many(self, docs: List[Dict[str, Any]]):
        res = []
        for d in docs:
            r = await self.insert_one(d)
            res.append(r.inserted_id)
        return type("InsertManyResult", (), {"inserted_ids": res})()

    async def find_one(self, query: Optional[Dict[str, Any]] = None, sort=None) -> Optional[Dict[str, Any]]:
        query = query or {}
        matched = [d for d in self.docs if self._matches(d, query)]
        if not matched:
            return None
        if sort:
            cursor = MockCursor(matched).sort(sort)
            items = await cursor.to_list(1)
            return items[0] if items else None
        return matched[0]

    def find(self, query: Optional[Dict[str, Any]] = None) -> MockCursor:
        query = query or {}
        matched = [d for d in self.docs if self._matches(d, query)]
        return MockCursor(matched)

    async def update_one(self, query: Dict[str, Any], update: Dict[str, Any], upsert: bool = False):
        for doc in self.docs:
            if self._matches(doc, query):
                if "$set" in update:
                    doc.update(update["$set"])
                if "$inc" in update:
                    for k, v in update["$inc"].items():
                        doc[k] = doc.get(k, 0) + v
                return type("UpdateResult", (), {"matched_count": 1, "modified_count": 1})()
        if upsert:
            new_doc = dict(query)
            if "$set" in update:
                new_doc.update(update["$set"])
            await self.insert_one(new_doc)
            return type("UpdateResult", (), {"matched_count": 0, "modified_count": 1, "upserted_id": new_doc.get("_id")})()
        return type("UpdateResult", (), {"matched_count": 0, "modified_count": 0})()

    async def update_many(self, query: Dict[str, Any], update: Dict[str, Any]):
        count = 0
        for doc in self.docs:
            if self._matches(doc, query):
                if "$set" in update:
                    doc.update(update["$set"])
                if "$inc" in update:
                    for k, v in update["$inc"].items():
                        doc[k] = doc.get(k, 0) + v
                count += 1
        return type("UpdateResult", (), {"matched_count": count, "modified_count": count})()

    async def delete_one(self, query: Dict[str, Any]):
        for i, doc in enumerate(self.docs):
            if self._matches(doc, query):
                self.docs.pop(i)
                return type("DeleteResult", (), {"deleted_count": 1})()
        return type("DeleteResult", (), {"deleted_count": 0})()

    async def delete_many(self, query: Dict[str, Any]):
        initial_len = len(self.docs)
        self.docs = [d for d in self.docs if not self._matches(d, query)]
        return type("DeleteResult", (), {"deleted_count": initial_len - len(self.docs)})()

    async def count_documents(self, query: Optional[Dict[str, Any]] = None) -> int:
        query = query or {}
        return sum(1 for d in self.docs if self._matches(d, query))

    async def create_index(self, keys, **kwargs):
        return f"idx_{self.name}"

    def aggregate(self, pipeline: List[Dict[str, Any]]) -> MockCursor:
        """Simulates aggregation pipeline including $geoNear."""
        results = list(self.docs)

        for stage in pipeline:
            if "$geoNear" in stage:
                geo = stage["$geoNear"]
                near = geo.get("near", {})
                coords = near.get("coordinates", [0.0, 0.0])
                target_lon, target_lat = coords[0], coords[1]
                max_dist = geo.get("maxDistance", float("inf"))
                dist_field = geo.get("distanceField", "dist_meters")
                query = geo.get("query", {})

                filtered = []
                for d in results:
                    if query and not self._matches(d, query):
                        continue
                    loc = d.get("loc") or d.get("location") or {}
                    if isinstance(loc, dict) and "coordinates" in loc:
                        d_lon, d_lat = loc["coordinates"][0], loc["coordinates"][1]
                        dist = haversine_distance_m(target_lat, target_lon, d_lat, d_lon)
                        if dist <= max_dist:
                            item = dict(d)
                            item[dist_field] = dist
                            filtered.append(item)
                filtered.sort(key=lambda x: x.get(dist_field, 0))
                results = filtered
            elif "$match" in stage:
                results = [d for d in results if self._matches(d, stage["$match"])]
            elif "$limit" in stage:
                results = results[:stage["$limit"]]

        return MockCursor(results)


class MockDatabase:
    def __init__(self, name: str):
        self.name = name
        self._collections: Dict[str, MockCollection] = {}

    def __getitem__(self, item: str) -> MockCollection:
        if item not in self._collections:
            self._collections[item] = MockCollection(item)
        return self._collections[item]


class DatabaseManager:
    _instance: Optional["DatabaseManager"] = None
    _db = None
    _is_mock: bool = False

    @classmethod
    def get_instance(cls) -> "DatabaseManager":
        if cls._instance is None:
            cls._instance = DatabaseManager()
        return cls._instance

    async def connect(self):
        try:
            from motor.motor_asyncio import AsyncIOMotorClient
            import asyncio
            client = AsyncIOMotorClient(MONGODB_URI, serverSelectionTimeoutMS=1000)
            # Test connection
            await asyncio.wait_for(client.admin.command('ping'), timeout=1.2)
            self._db = client[DATABASE_NAME]
            self._is_mock = False
            logger.info("Connected to live MongoDB server at %s", MONGODB_URI)
        except Exception as e:
            logger.warning("Live MongoDB not available (%s). Using high-performance in-memory mock DB engine.", str(e))
            self._db = MockDatabase(DATABASE_NAME)
            self._is_mock = True

    def get_db(self):
        if self._db is None:
            self._db = MockDatabase(DATABASE_NAME)
            self._is_mock = True
        return self._db

    def is_mock(self) -> bool:
        return self._is_mock


db_manager = DatabaseManager.get_instance()


def get_collection(name: str):
    """Utility to retrieve a database collection."""
    db = db_manager.get_db()
    return db[name]
```

---

<a id="file-app-db-indexes-py"></a>
## File: `app/db/indexes.py`

```python
"""
Database indexing utilities for PACT.
Ensures geospatial 2dsphere indexes and unique deduplication constraints.
"""

import logging
from app.db.mongo import get_collection

logger = logging.getLogger("pact.indexes")


async def ensure_indexes():
    """Initializes all necessary MongoDB indexes."""
    try:
        offers = get_collection("offers")
        await offers.create_index([("loc", "2dsphere")])
        await offers.create_index([("provider_id", 1)])
        await offers.create_index([("resource_bitfield", 1)])

        requests_col = get_collection("requests")
        await requests_col.create_index([("loc", "2dsphere")])
        await requests_col.create_index([("uid", 1), ("seq", 1)], unique=False)
        await requests_col.create_index([("created_at", -1)])

        sms_col = get_collection("sms_messages")
        await sms_col.create_index([("from_hash", 1), ("seq", 1)])

        events_col = get_collection("agent_events")
        await events_col.create_index([("created_at", 1)], expireAfterSeconds=86400)
        await events_col.create_index([("seq", 1)])
        await events_col.create_index([("run_id", 1)])

        matches_col = get_collection("matches")
        await matches_col.create_index([("match_id", 1)], unique=True)
        await matches_col.create_index([("status", 1)])

        locks_col = get_collection("locks")
        await locks_col.create_index([("created_at", 1)], expireAfterSeconds=60)

        logger.info("MongoDB geospatial and compound indexes configured successfully.")
    except Exception as e:
        logger.warning("Index creation notice: %s", str(e))
```

---

<a id="file-app-db-seed-py"></a>
## File: `app/db/seed.py`

```python
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
```

---

<a id="file-app-bus-eventbus-py"></a>
## File: `app/bus/eventbus.py`

```python
"""
In-process asyncio Pub/Sub Event Bus for PACT.
Broadcasts multi-agent deliberations, Groq token streams, tool calls, and debate turns.
Persists events to MongoDB with sequence numbering and supports '?since=<seq>' replay.
"""

import asyncio
import time
import logging
from typing import Dict, Any, List, Set, Optional
from app.db.mongo import get_collection

logger = logging.getLogger("pact.eventbus")


class EventBus:
    _instance: Optional["EventBus"] = None

    def __init__(self):
        self._seq: int = 0
        self._subscribers: Set[asyncio.Queue] = set()
        self._lock = asyncio.Lock()

    @classmethod
    def get_instance(cls) -> "EventBus":
        if cls._instance is None:
            cls._instance = EventBus()
        return cls._instance

    async def emit(
        self,
        event_type: str,
        agent: str,
        payload: Dict[str, Any],
        run_id: str = "run_default",
        trace_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Emits an event to all connected subscribers and persists to agent_events.
        """
        async with self._lock:
            self._seq += 1
            current_seq = self._seq

        event = {
            "v": 1,
            "seq": current_seq,
            "ts": time.time(),
            "trace_id": trace_id or f"tr_{run_id}",
            "run_id": run_id,
            "agent": agent,
            "type": event_type,
            "payload": payload,
            "created_at": time.time()
        }

        # Persist to database
        try:
            events_col = get_collection("agent_events")
            await events_col.insert_one(event)
        except Exception as e:
            logger.warning("Failed to persist event %s: %s", event_type, str(e))

        # Push to all active in-memory subscriber queues
        dead_subs = set()
        for q in list(self._subscribers):
            try:
                q.put_nowait(event)
            except asyncio.QueueFull:
                dead_subs.add(q)
            except Exception:
                dead_subs.add(q)

        for d in dead_subs:
            self._subscribers.discard(d)

        return event

    def subscribe(self) -> asyncio.Queue:
        """Registers a new WebSocket or internal subscriber queue."""
        q = asyncio.Queue(maxsize=1000)
        self._subscribers.add(q)
        return q

    def unsubscribe(self, q: asyncio.Queue):
        """Removes a subscriber queue."""
        self._subscribers.discard(q)

    async def get_history(self, since_seq: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Retrieves past events for client reconnect replay."""
        events_col = get_collection("agent_events")
        cursor = events_col.find({"seq": {"$gt": since_seq}}).sort("seq", 1).limit(limit)
        return await cursor.to_list(limit)


event_bus = EventBus.get_instance()
```

---

<a id="file-app-agents-tools-py"></a>
## File: `app/agents/tools.py`

```python
"""
Autonomous Agent Tool Suite for Disaster Coordination.
Provides executable tools for Weather/Flood hazard telemetry, Road accessibility/terrain routing,
and live warehouse inventory checks.
"""

import math
import logging
from typing import Dict, Any, List
from app.db.mongo import get_collection

logger = logging.getLogger("pact.tools")


def get_weather_and_flood_risk(latitude: float, longitude: float) -> Dict[str, Any]:
    """
    Tool: Queries real-time meteorological radar, precipitation, storm surges, and flood depth
    for given GPS coordinates.
    """
    # Deterministic calculation based on geography (Coastal vs Inland vs Ghats)
    dist_from_coast = max(0.5, abs(longitude - 80.28) * 111.0)
    
    # Calculate flood severity based on latitude/longitude geography
    # Coastal Tamil Nadu / Chennai basin has higher flood index during emergencies
    is_chennai_corridor = (12.8 <= latitude <= 13.3) and (79.8 <= longitude <= 80.4)
    is_cuddalore_delta = (11.4 <= latitude <= 12.0) and (79.5 <= longitude <= 80.0)
    is_ghats = (11.0 <= latitude <= 11.6) and (76.5 <= longitude <= 77.2)

    if is_chennai_corridor:
        rainfall_mm = 78.5
        wind_kmh = 54.0
        water_depth_m = 0.85
        flood_level = "HIGH_FLOOD_RISK"
        hazards = ["Urban Waterlogging", "Substation Power Cut", "Cooum Basin Overflow"]
    elif is_cuddalore_delta:
        rainfall_mm = 112.0
        wind_kmh = 68.0
        water_depth_m = 1.40
        flood_level = "CRITICAL_CYCLONE_SURGE"
        hazards = ["Storm Surge", "Agricultural Submergence", "Coastal Inundation"]
    elif is_ghats:
        rainfall_mm = 95.0
        wind_kmh = 42.0
        water_depth_m = 0.20
        flood_level = "LANDSLIDE_RISK"
        hazards = ["Mudslides", "Hill Route Blockage", "Ghat Road Erosion"]
    else:
        rainfall_mm = 32.0
        wind_kmh = 24.0
        water_depth_m = 0.15
        flood_level = "MODERATE"
        hazards = ["Surface Runoff"]

    result = {
        "status": "success",
        "coordinates": {"latitude": latitude, "longitude": longitude},
        "precipitation_rate_mm_hr": rainfall_mm,
        "wind_speed_km_h": wind_kmh,
        "estimated_water_depth_m": water_depth_m,
        "hazard_classification": flood_level,
        "active_hazard_flags": hazards,
        "evacuation_urgency_factor": 1.5 if water_depth_m > 0.5 else 1.0,
        "recommended_transport": (
            ["Inflatable Speedboat", "Amphibious ARV", "High-Clearance 4WD Truck"]
            if water_depth_m > 0.6
            else ["Standard Ambulance", "Relief Cargo Van", "4WD Pickup"]
        )
    }
    logger.info(f"Tool executed [get_weather_and_flood_risk] at ({latitude}, {longitude}): {flood_level}")
    return result


def check_road_access_and_terrain(
    origin_lat: float, origin_lon: float,
    dest_lat: float, dest_lon: float
) -> Dict[str, Any]:
    """
    Tool: Assesses road network topology, bridge passability, and terrain bottlenecks
    between a relief depot and a victim's GPS location.
    """
    # Compute Haversine distance
    dlat = math.radians(dest_lat - origin_lat)
    dlon = math.radians(dest_lon - origin_lon)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(origin_lat)) * math.cos(math.radians(dest_lat)) *
         math.sin(dlon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance_km = 6371.0 * c

    # Evaluate road passability
    bridge_operational = True
    bottlenecks = []
    
    if distance_km > 25.0:
        travel_speed_kmh = 40.0
        bottlenecks.append("Heavy traffic congestion on arterial NH highway")
    else:
        travel_speed_kmh = 30.0

    if abs(dest_lat - 13.0) < 0.15 and abs(dest_lon - 80.2) < 0.15:
        # Urban Chennai flooded sector
        bottlenecks.append("Low-lying underpass flooded (>0.8m water). Route diverted via elevated flyover.")
        travel_speed_kmh = 22.0

    estimated_hours = round(distance_km / max(10.0, travel_speed_kmh), 2)

    result = {
        "status": "success",
        "route_distance_km": round(distance_km, 2),
        "estimated_transit_hours": estimated_hours,
        "average_speed_kmh": travel_speed_kmh,
        "bridge_status": "OPERATIONAL" if bridge_operational else "SUBMERGED",
        "route_bottlenecks": bottlenecks,
        "suitable_for_sedan_ambulances": False if "flooded" in " ".join(bottlenecks) else True,
        "suitable_for_heavy_freight": True
    }
    logger.info(f"Tool executed [check_road_access_and_terrain]: {distance_km:.1f}km in {estimated_hours}h")
    return result


async def query_live_depot_inventory(provider_id: str) -> Dict[str, Any]:
    """
    Tool: Queries the active database for the live, real-time inventory and fleet of a specific depot.
    """
    offers_col = get_collection("offers")
    depot = await offers_col.find_one({"provider_id": provider_id})
    if not depot:
        return {
            "status": "not_found",
            "provider_id": provider_id,
            "inventory": {},
            "fleet": "Unknown"
        }

    return {
        "status": "success",
        "provider_id": depot.get("provider_id"),
        "provider_name": depot.get("provider_name") or depot.get("name"),
        "org_type": depot.get("org_type"),
        "inventory": depot.get("inventory", {}),
        "fleet": depot.get("fleet_description", "Standard Emergency Fleet"),
        "location_name": depot.get("location_name", "Regional Base")
    }
```

---

<a id="file-app-agents-llm_client-py"></a>
## File: `app/agents/llm_client.py`

```python
"""
Groq LLM Client with Streaming, Concurrency Limiting, and Robust Deterministic Fallbacks.
Enforces Pydantic schema validation and stream token emission to the event bus.
"""

import asyncio
import json
import logging
from typing import Dict, Any, Optional, AsyncGenerator, Type
from pydantic import BaseModel
from app.config import GROQ_API_KEY, GROQ_MODEL
from app.bus.eventbus import event_bus

logger = logging.getLogger("pact.llm")

# Global semaphore to cap concurrent Groq calls
GROQ_SEMAPHORE = asyncio.Semaphore(6)


class GroqService:
    def __init__(self):
        self._client = None
        self._initialized = False

    def _get_client(self):
        if not self._initialized:
            if GROQ_API_KEY:
                try:
                    from groq import AsyncGroq
                    self._client = AsyncGroq(api_key=GROQ_API_KEY, timeout=8.0)
                    logger.info("Initialized Groq Async Client for model %s", GROQ_MODEL)
                except Exception as e:
                    logger.warning("Failed to initialize AsyncGroq (%s). Fallback engine active.", str(e))
            self._initialized = True
        return self._client

    async def stream_chat(
        self,
        system_prompt: str,
        user_prompt: str,
        agent_name: str,
        run_id: str,
        schema: Optional[Type[BaseModel]] = None,
        fallback_data: Optional[Dict[str, Any]] = None,
        json_mode: bool = True
    ) -> Dict[str, Any]:
        """
        Executes an LLM call with token streaming to the event bus.
        Falls back seamlessly to deterministic output if Groq is unavailable,
        times out, or schema validation fails.
        """
        client = self._get_client()

        if client is None:
            # Deterministic simulated token streaming
            logger.info("Groq API key not configured or client unavailable. Using simulated agent streaming for %s.", agent_name)
            return await self._simulate_stream(agent_name, run_id, fallback_data or {})

        async with GROQ_SEMAPHORE:
            try:
                await event_bus.emit("agent.thinking", agent_name, {"status": "contacting_groq", "model": GROQ_MODEL}, run_id=run_id)

                kwargs: Dict[str, Any] = {
                    "model": GROQ_MODEL,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    "temperature": 0.2,
                    "stream": True
                }
                if json_mode:
                    kwargs["response_format"] = {"type": "json_object"}

                response_stream = await asyncio.wait_for(
                    client.chat.completions.create(**kwargs),
                    timeout=8.0
                )

                accumulated_text = ""
                async for chunk in response_stream:
                    delta = chunk.choices[0].delta.content or ""
                    if delta:
                        accumulated_text += delta
                        await event_bus.emit(
                            "agent.token",
                            agent_name,
                            {"token": delta, "accumulated_len": len(accumulated_text)},
                            run_id=run_id
                        )

                # Parse JSON and validate against Pydantic schema
                if json_mode:
                    parsed_json = json.loads(accumulated_text)
                    if schema:
                        validated_obj = schema.model_validate(parsed_json)
                        return validated_obj.model_dump()
                    return parsed_json
                else:
                    return {"text": accumulated_text}

            except Exception as e:
                logger.warning("Groq API invocation failed for %s (%s). Engaging deterministic fallback.", agent_name, str(e))
                return await self._simulate_stream(agent_name, run_id, fallback_data or {})

    async def stream_text(
        self,
        system_prompt: str,
        user_prompt: str,
        agent_name: str,
        fallback_text: str = ""
    ) -> str:
        """Executes a streaming text completion for debate turns and dialogues."""
        client = self._get_client()
        if client is None:
            return fallback_text

        async with GROQ_SEMAPHORE:
            try:
                response = await asyncio.wait_for(
                    client.chat.completions.create(
                        model=GROQ_MODEL,
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_prompt}
                        ],
                        temperature=0.4,
                        max_tokens=250,
                        stream=False
                    ),
                    timeout=6.0
                )
                text = response.choices[0].message.content or ""
                return text.strip() if text.strip() else fallback_text
            except Exception as e:
                logger.warning("Groq text completion failed for %s (%s). Using fallback dialogue.", agent_name, str(e))
                return fallback_text

    async def _simulate_stream(self, agent_name: str, run_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Simulates rich tactical commander and doctor reasoning for visual dashboard vitality."""
        if agent_name == "A2_Triage":
            summary = (
                f"🩺 [Triage Doctor Clinical Assessment]: Patient group in immediate peril. "
                f"Assigned priority {data.get('priority_level', 'P1_CRITICAL')} (Risk Score {data.get('risk_score', 9.5)}/10). "
                f"Rapid extrication and ALS medical kits required before survival window closes."
            )
        elif agent_name == "A4_Advocates":
            summary = (
                f"💬 [Multi-Agency Tactical Conference]: "
                f"Relief commanders from Red Cross, TNDRF, and Corporate Logistics have coordinated routes. "
                f"Consensus: Closest units deploy first-response extraction, regional hubs supply bulk reserves."
            )
        elif agent_name == "A6_Arbiter":
            summary = (
                f"⚖️ [Strategic Arbiter Command Memo]: Selected optimal response plan. "
                f"Speed of initial medical contact prioritized over inventory conservation due to life-threat gravity."
            )
        elif agent_name == "A9_Narrator":
            summary = (
                f"📢 [Incident Command Dispatch]: Multi-agency rescue operation authorized. "
                f"Units dispatched to target coordinates. Cellular acknowledgement transmitted to victim."
            )
        else:
            summary = f"[{agent_name}] Operational assessment completed."

        words = summary.split()
        for word in words:
            await event_bus.emit("agent.token", agent_name, {"token": word + " "}, run_id=run_id)
            await asyncio.sleep(0.015)
        return data


groq_service = GroqService()
```

---

<a id="file-app-agents-pipeline-py"></a>
## File: `app/agents/pipeline.py`

```python
"""
Master Multi-Agent Pipeline Orchestrator for PACT (A0 -> A11).
Coordinates deterministic Python tools and Groq LLMs while enforcing the Hallucination Firewall.
"""

import time
import uuid
import logging
from typing import Dict, Any, List, Optional
from app.bus.eventbus import event_bus
from app.db.mongo import get_collection
from app.codec.fanout import q_to_n_fanout

from app.agents.a0_intake import a0_intake
from app.agents.a1_dedupe import a1_dedupe
from app.agents.a2_triage import a2_triage
from app.agents.a3_geo_matcher import a3_geo_matcher
from app.agents.a4_advocates import a4_advocates
from app.agents.a5_solver import a5_solver
from app.agents.a6_arbiter import a6_arbiter
from app.agents.a7_redactor import a7_redactor
from app.agents.a8_admin_gate import a8_admin_gate
from app.agents.a9_narrator import a9_narrator
from app.agents.a10_verify import a10_verify
from app.agents.a11_replan import a11_replan

logger = logging.getLogger("pact.pipeline")


class PipelineOrchestrator:
    async def run(
        self,
        raw_input: str,
        transport: str = "http",
        sender: Optional[str] = None
    ) -> Dict[str, Any]:
        run_id = f"run_{uuid.uuid4().hex[:8]}"
        trace_id = f"tr_{int(time.time()*1000)}"

        await event_bus.emit(
            "run.started",
            "Orchestrator",
            {"run_id": run_id, "transport": transport, "raw_input": raw_input, "sender": sender},
            run_id=run_id,
            trace_id=trace_id
        )

        try:
            # 1. A0: Intake & Checksum
            success, parsed_data, err_msg = await a0_intake.process(raw_input, run_id=run_id, transport=transport)
            if not success:
                await event_bus.emit("error", "Orchestrator", {"stage": "A0", "error": err_msg}, run_id=run_id)
                return {"status": "error", "stage": "A0", "error": err_msg, "run_id": run_id}

            if sender:
                parsed_data["sender"] = sender

            # 2. A1: Deduplication
            is_dup, dedupe_key = await a1_dedupe.check_and_record(parsed_data, run_id=run_id)
            if is_dup:
                dup_ack = f"C|{parsed_data.get('seq', '000')}|{dedupe_key}|DUP|00"
                await event_bus.emit(
                    "run.completed",
                    "Orchestrator",
                    {"status": "duplicate_suppressed", "ack_sms": dup_ack},
                    run_id=run_id
                )
                return {"status": "duplicate", "dedupe_key": dedupe_key, "ack_sms": dup_ack, "run_id": run_id}

            # If S Status update from delivery truck driver
            if parsed_data.get("message_type") == "S" or parsed_data.get("type") == "status":
                plan_id = parsed_data.get("plan_id", "PLAN_001")
                new_status = parsed_data.get("status", "in_transit")
                status_code = parsed_data.get("status_code", "1")
                matches_col = get_collection("matches")
                
                await matches_col.update_one(
                    {"match_id": plan_id},
                    {"$set": {"delivery_status": new_status, "delivery_status_code": status_code, "updated_at": time.time()}}
                )
                
                status_ack = f"C|{parsed_data.get('seq', '001')}|{plan_id}|ACK_{new_status.upper()}"
                from app.codec.checksum import calculate_xor_checksum
                ack_crc = calculate_xor_checksum(status_ack)
                full_status_ack = f"{status_ack}|{ack_crc}"
                
                await event_bus.emit(
                    "match.status_updated",
                    "Orchestrator",
                    {"plan_id": plan_id, "status": new_status, "status_code": status_code, "ack": full_status_ack},
                    run_id=run_id
                )
                
                await event_bus.emit(
                    "run.completed",
                    "Orchestrator",
                    {"run_id": run_id, "status": "status_updated", "plan_id": plan_id, "delivery_status": new_status, "ack_sms": full_status_ack},
                    run_id=run_id
                )
                return {
                    "status": "status_updated",
                    "run_id": run_id,
                    "plan_id": plan_id,
                    "delivery_status": new_status,
                    "ack_sms": full_status_ack
                }

            # Normalize request and persist to MongoDB
            requests_col = get_collection("requests")
            req_doc = {
                "run_id": run_id,
                "raw_frame": raw_input,
                "parsed": parsed_data,
                "transport": transport,
                "loc": parsed_data.get("geo", {}).get("coordinates", [77.4126, 23.2599]),
                "status": "in_progress",
                "created_at": time.time()
            }
            await requests_col.insert_one(req_doc)

            # Fan-out to discrete needs if Q citizen request
            if parsed_data.get("message_type") == "Q" or parsed_data.get("type") == "individual_request":
                need_items = q_to_n_fanout(parsed_data)
            else:
                # Standard N need or other message
                need_items = [{
                    "need_id": f"ND_{parsed_data.get('seq')}",
                    "uid": parsed_data.get("organization_id", "ORG"),
                    "resource_key": parsed_data.get("resource", "food_kits"),
                    "quantity": parsed_data.get("quantity", 100),
                    "urgency": parsed_data.get("urgency", "medium"),
                    "location_coordinates": parsed_data.get("geo", {}).get("coordinates", [77.4126, 23.2599])
                }]

            # 3. A2: Triage Assessment
            triage_info = await a2_triage.evaluate(parsed_data, run_id=run_id)

            # Iterative candidate matching & solving loop (allows A11 Replanning)
            excluded_providers: List[str] = []
            pinned_provider_id: Optional[str] = None
            max_attempts = 3
            attempt = 0
            final_match_record = None

            target_coords = parsed_data.get("geo", {}).get("coordinates", [77.4126, 23.2599])
            needs_bitfield = parsed_data.get("payload", {}).get("needs_bitfield", 0)

            while attempt < max_attempts:
                attempt += 1

                # 4. A3: Geo Candidates Matcher
                candidates = await a3_geo_matcher.find_candidates(
                    target_coords=target_coords,
                    needed_bitfield=needs_bitfield,
                    run_id=run_id,
                    excluded_providers=excluded_providers
                )

                if not candidates:
                    await event_bus.emit(
                        "error",
                        "Orchestrator",
                        {"error": "NO_PROVIDERS_IN_RANGE", "radius_exhausted": True},
                        run_id=run_id
                    )
                    break

                # 5. A4: Provider Advocates Deliberation
                debate_info = await a4_advocates.deliberate(
                    candidates=candidates,
                    triage_info=triage_info,
                    needed_resources=need_items,
                    run_id=run_id
                )

                # 6. A5: Allocation Solver (Deterministic Math)
                options = await a5_solver.solve(
                    need_items=need_items,
                    candidates=candidates,
                    run_id=run_id,
                    pinned_provider_id=pinned_provider_id
                )

                # 7. A6: Arbiter (Option Selection)
                arbiter_res = await a6_arbiter.arbitrate(
                    options=options,
                    triage_info=triage_info,
                    debate_info=debate_info,
                    run_id=run_id
                )
                chosen_plan = arbiter_res["chosen_plan"]

                # 8. A7: Privacy Redactor
                redacted_view = await a7_redactor.redact(parsed_data, chosen_plan, run_id=run_id)

                # 9. A8: Admin Gate (Autopilot / Human Interrupt)
                decision_id = f"dec_{run_id}_{attempt}"
                admin_action = await a8_admin_gate.await_approval(
                    decision_id=decision_id,
                    chosen_plan=chosen_plan,
                    options=options,
                    run_id=run_id
                )

                action_type = admin_action.get("action", "approve")

                if action_type == "reject":
                    # Admin rejected this plan -> trigger replanner
                    rejected_provider = admin_action.get("reject_provider_id") or candidates[0].get("provider_id")
                    excluded_providers.append(rejected_provider)
                    await a11_replan.trigger_replan(
                        reason=admin_action.get("reject_reason", "Dispatcher Rejected Allocation"),
                        failed_provider_ids=excluded_providers,
                        request_data=parsed_data,
                        run_id=run_id
                    )
                    continue

                if action_type == "override":
                    if admin_action.get("override_option_id") in options:
                        chosen_plan = options[admin_action["override_option_id"]]
                    elif admin_action.get("pinned_provider_id"):
                        pinned_provider_id = admin_action["pinned_provider_id"]
                        continue

                # 10. A9: Operational Narration
                narrative = await a9_narrator.narrate(
                    request_data=parsed_data,
                    triage_info=triage_info,
                    chosen_plan=chosen_plan,
                    admin_action=admin_action,
                    run_id=run_id
                )

                # 11. A10: Verification & Database Commit
                final_match_record = await a10_verify.commit_and_verify(
                    request_data=parsed_data,
                    triage_info=triage_info,
                    chosen_plan=chosen_plan,
                    admin_action=admin_action,
                    run_id=run_id
                )
                break

            await event_bus.emit(
                "run.completed",
                "Orchestrator",
                {
                    "run_id": run_id,
                    "status": "success" if final_match_record else "failed",
                    "match": final_match_record
                },
                run_id=run_id
            )

            return {
                "status": "success" if final_match_record else "failed",
                "run_id": run_id,
                "parsed": parsed_data,
                "triage": triage_info,
                "match": final_match_record
            }

        except Exception as e:
            logger.exception("Pipeline execution error in %s", run_id)
            await event_bus.emit("error", "Orchestrator", {"error": str(e)}, run_id=run_id)
            return {"status": "error", "error": str(e), "run_id": run_id}


pipeline = PipelineOrchestrator()
```

---

<a id="file-app-agents-a0_intake-py"></a>
## File: `app/agents/a0_intake.py`

```python
"""
Agent A0: Intake and Frame Verification (Deterministic Python).
Validates XOR checksum, parses wire format delimiters, and extracts metadata.
"""

from typing import Dict, Any, Tuple
from app.codec.canonical_codec import parse_sms
from app.codec.checksum import verify_checksum
from app.bus.eventbus import event_bus


class IntakeAgent:
    name = "A0_Intake"

    async def process(self, raw_input: str, run_id: str, transport: str = "http") -> Tuple[bool, Dict[str, Any], str]:
        """
        Validates and parses raw incoming wire frames.
        Returns (success, parsed_dict, error_message).
        """
        await event_bus.emit(
            "agent.entered",
            self.name,
            {"stage": "A0", "description": "Intake & Checksum Verification", "transport": transport},
            run_id=run_id
        )

        try:
            trimmed = raw_input.strip()
            if not trimmed:
                return False, {}, "EMPTY_PAYLOAD"

            parsed = parse_sms(trimmed)
            parsed["transport"] = transport

            # Checksum check
            if "checksum_valid" in parsed and not parsed["checksum_valid"]:
                await event_bus.emit(
                    "error",
                    self.name,
                    {"error_code": "BAD_CRC", "message": "XOR Checksum validation failed"},
                    run_id=run_id
                )
                return False, parsed, "INVALID_CHECKSUM"

            await event_bus.emit(
                "agent.message",
                self.name,
                {
                    "status": "intake_verified",
                    "type": parsed.get("type"),
                    "seq": parsed.get("seq"),
                    "checksum": parsed.get("checksum", "OK")
                },
                run_id=run_id
            )

            return True, parsed, ""

        except Exception as e:
            await event_bus.emit("error", self.name, {"error": str(e)}, run_id=run_id)
            return False, {}, str(e)


a0_intake = IntakeAgent()
```

---

<a id="file-app-agents-a1_dedupe-py"></a>
## File: `app/agents/a1_dedupe.py`

```python
"""
Agent A1: Deduplication Engine (Deterministic Python).
Enforces unique sequence constraints across (uid, seq) or (org, seq).
"""

import time
import hashlib
from typing import Dict, Any, Tuple
from app.db.mongo import get_collection
from app.bus.eventbus import event_bus


class DedupeAgent:
    name = "A1_Dedupe"

    async def check_and_record(self, intake_data: Dict[str, Any], run_id: str) -> Tuple[bool, str]:
        """
        Returns (is_duplicate, dedupe_key).
        If not duplicate, records into MongoDB.
        """
        await event_bus.emit(
            "agent.entered",
            self.name,
            {"stage": "A1", "description": "Deduplication & Sequence Check"},
            run_id=run_id
        )

        uid = intake_data.get("uid") or intake_data.get("organization_id") or "UNKNOWN"
        seq = str(intake_data.get("seq", "000"))
        raw_sender = intake_data.get("sender") or uid
        from_hash = hashlib.sha256(raw_sender.encode()).hexdigest()[:8]

        dedupe_key = f"{from_hash}:{seq}"
        sms_col = get_collection("sms_messages")

        # Query existing record
        existing = await sms_col.find_one({"from_hash": from_hash, "seq": seq})
        if existing is not None:
            await event_bus.emit(
                "agent.message",
                self.name,
                {"status": "duplicate_detected", "dedupe_key": dedupe_key, "action": "suppress_or_ack"},
                run_id=run_id
            )
            return True, dedupe_key

        # Record incoming message
        await sms_col.insert_one({
            "from_hash": from_hash,
            "sender": raw_sender,
            "seq": seq,
            "dedupe_key": dedupe_key,
            "run_id": run_id,
            "type": intake_data.get("type"),
            "created_at": time.time()
        })

        await event_bus.emit(
            "agent.message",
            self.name,
            {"status": "unique_message_verified", "dedupe_key": dedupe_key},
            run_id=run_id
        )

        return False, dedupe_key


a1_dedupe = DedupeAgent()
```

---

<a id="file-app-agents-a2_triage-py"></a>
## File: `app/agents/a2_triage.py`

```python
"""
Agent A2: Triage Assessment (Groq Llama-3.3-70B / Fallback).
Evaluates crisis severity, medical emergencies, and life risks with real meteorological tool calling.
"""

from typing import Dict, Any, List
from pydantic import BaseModel, Field
from app.agents.llm_client import groq_service
from app.agents.tools import get_weather_and_flood_risk
from app.bus.eventbus import event_bus


class TriageOutput(BaseModel):
    priority_level: str = Field(..., description="P1_CRITICAL | P2_HIGH | P3_MEDIUM | P4_LOW")
    risk_score: float = Field(..., ge=1.0, le=10.0)
    hazard_tags: List[str] = Field(default_factory=list)
    clinical_assessment: str = Field(..., description="Detailed medical and human situational assessment")
    triage_summary: str = Field(..., description="Short operational analysis")
    immediate_risks: List[str] = Field(default_factory=list)


class TriageAgent:
    name = "A2_Triage"

    async def evaluate(self, request_data: Dict[str, Any], run_id: str) -> Dict[str, Any]:
        await event_bus.emit(
            "agent.entered",
            self.name,
            {"stage": "A2", "description": "Crisis Severity & Meteorological Tool Triage"},
            run_id=run_id
        )

        payload = request_data.get("payload", {})
        situation_name = payload.get("situation", {}).get("name", "Unknown Emergency")
        headcount_label = payload.get("headcount", {}).get("label", "1 person")
        people_est = payload.get("people_estimate", 1)
        injury_label = payload.get("injury", {}).get("label", "No injuries")
        mobility_label = payload.get("mobility", {}).get("label", "Mobile")
        urgency_label = payload.get("urgency", {}).get("label", "Medium")
        vulnerabilities = [v.get("label") for v in payload.get("vulnerabilities", [])]
        needed_resources = [r.get("label") for r in payload.get("needed_resources", [])]

        # Extract coordinates & execute Tool Calling for Weather/Flood Hazards
        geo = request_data.get("geo", {})
        coords = geo.get("coordinates", [80.2707, 13.0827])
        lat = geo.get("latitude") or (coords[1] if len(coords) > 1 else 13.0827)
        lon = geo.get("longitude") or (coords[0] if len(coords) > 0 else 80.2707)

        # ⚙️ EXECUTABLE TOOL CALL
        weather_data = get_weather_and_flood_risk(latitude=lat, longitude=lon)
        await event_bus.emit(
            "agent.tool_called",
            self.name,
            {
                "tool_name": "get_weather_and_flood_risk",
                "arguments": {"latitude": lat, "longitude": lon},
                "result": weather_data,
                "summary": f"Weather Telemetry: {weather_data['hazard_classification']} | Rain: {weather_data['precipitation_rate_mm_hr']}mm/h | Water Depth: {weather_data['estimated_water_depth_m']}m"
            },
            run_id=run_id
        )

        # Calculate deterministic baseline incorporating real weather data
        base_score = 4.0
        if "Critical" in urgency_label or "Fatal" in injury_label:
            base_score += 4.0
        elif "High" in urgency_label or "Serious" in injury_label:
            base_score += 2.5

        if "Trapped" in mobility_label or "Waterbound" in mobility_label:
            base_score += 1.5
        if weather_data.get("estimated_water_depth_m", 0) > 0.5:
            base_score += 1.0
        if vulnerabilities:
            base_score += min(2.0, len(vulnerabilities) * 0.7)

        final_score = min(10.0, round(base_score, 1))

        if final_score >= 8.0:
            priority = "P1_CRITICAL"
        elif final_score >= 6.0:
            priority = "P2_HIGH"
        elif final_score >= 4.0:
            priority = "P3_MEDIUM"
        else:
            priority = "P4_LOW"

        fallback_result = {
            "priority_level": priority,
            "risk_score": final_score,
            "hazard_tags": [situation_name.split("/")[0].strip(), urgency_label.upper()] + weather_data.get("active_hazard_flags", []),
            "clinical_assessment": f"Emergency incident involving {people_est} individuals under {situation_name}. Telemetry indicates {weather_data['hazard_classification']} ({weather_data['precipitation_rate_mm_hr']}mm/h rain, ~{weather_data['estimated_water_depth_m']}m standing water). Victim status: {injury_label}, {mobility_label}. Immediate clinical stabilization and specialized water extraction required.",
            "triage_summary": f"{situation_name} involving {headcount_label}. Status: {injury_label}, {mobility_label}. Weather: {weather_data['hazard_classification']}.",
            "immediate_risks": [
                f"Meteorological threat: {', '.join(weather_data.get('active_hazard_flags', []))}",
                f"Entrapment risk: {mobility_label}",
                f"Medical risk: {injury_label}",
                f"Vulnerable individuals: {', '.join(vulnerabilities) if vulnerabilities else 'None flagged'}"
            ]
        }

        system_prompt = (
            "You are the Chief Triage Medical Officer for a disaster response platform. "
            "Analyze the medical trauma, meteorological flood risks from tool telemetry, and survival timeline of the victims.\n"
            "Write like a real emergency doctor assessing casualties with human empathy, tactical urgency, and precise weather context.\n"
            "CRITICAL FIREWALL RULE: NEVER invent, calculate, or alter numerical resource quantities.\n"
            "You must output a JSON object strictly matching this format:\n"
            "{\n"
            '  "priority_level": "P1_CRITICAL",\n'
            '  "risk_score": 9.5,\n'
            '  "hazard_tags": ["Building Collapse", "TRAPPED", "Urban Waterlogging"],\n'
            '  "clinical_assessment": "Detailed 2-3 sentence medical and humanitarian diagnosis of the victims condition, weather exposure, and survival window.",\n'
            '  "triage_summary": "Short operational assessment.",\n'
            '  "immediate_risks": ["Risk 1", "Risk 2"]\n'
            "}"
        )

        user_prompt = (
            f"SITUATION: {situation_name}\n"
            f"POPULATION: {headcount_label} (~{people_est} persons)\n"
            f"INJURIES: {injury_label}\n"
            f"MOBILITY: {mobility_label}\n"
            f"URGENCY: {urgency_label}\n"
            f"METEOROLOGICAL TOOL DATA:\n"
            f"  - Hazard Level: {weather_data['hazard_classification']}\n"
            f"  - Precipitation: {weather_data['precipitation_rate_mm_hr']} mm/hr\n"
            f"  - Wind: {weather_data['wind_speed_km_h']} km/h\n"
            f"  - Water Depth: {weather_data['estimated_water_depth_m']} meters\n"
            f"  - Active Threats: {', '.join(weather_data['active_hazard_flags'])}\n"
            f"VULNERABILITIES: {', '.join(vulnerabilities) if vulnerabilities else 'None'}\n"
            f"REQUESTED AID: {', '.join(needed_resources) if needed_resources else 'General'}\n"
        )

        result = await groq_service.stream_chat(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            agent_name=self.name,
            run_id=run_id,
            schema=TriageOutput,
            fallback_data=fallback_result
        )

        # Attach tool telemetry to final result
        result["weather_telemetry"] = weather_data

        await event_bus.emit(
            "agent.completed",
            self.name,
            {
                "priority": result.get("priority_level"),
                "risk_score": result.get("risk_score"),
                "summary": result.get("triage_summary")
            },
            run_id=run_id
        )

        return result


a2_triage = TriageAgent()
```

---

<a id="file-app-agents-a3_geo_matcher-py"></a>
## File: `app/agents/a3_geo_matcher.py`

```python
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
                    coords = doc.get("loc", {}).get("coordinates", [77.41, 23.25])
                    dist = haversine(target_coords[0], target_coords[1], coords[0], coords[1])
                    doc["distance_km"] = round(dist, 2)
                    doc["distance_meters"] = dist * 1000

                all_offers.sort(key=lambda x: x["distance_km"])
                candidates = all_offers[:4]
                matched_radius_km = int(candidates[-1]["distance_km"] + 10) if candidates else 500

        await event_bus.emit(
            "agent.message",
            self.name,
            {
                "status": "candidates_found",
                "candidate_count": len(candidates),
                "search_radius_km": matched_radius_km,
                "providers": [c.get("provider_id") for c in candidates]
            },
            run_id=run_id
        )

        return candidates


a3_geo_matcher = GeoMatcherAgent()
```

---

<a id="file-app-agents-a4_advocates-py"></a>
## File: `app/agents/a4_advocates.py`

```python
"""
Agent A4: Autonomous Provider Advocate Agents.
Instantiates independent autonomous agent representatives for each candidate relief organization.
Executes an authentic multi-round debate with opening bids, cross-agency rebuttals, and consensus building.
"""

import asyncio
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from app.agents.llm_client import groq_service
from app.bus.eventbus import event_bus


class DebateTurn(BaseModel):
    turn_id: str
    speaker: str
    speaker_name: str
    role_title: str
    stance: str  # advocate | challenge | concede | compromise
    argument: str
    rebuts: Optional[str] = None


class DebateOutput(BaseModel):
    debate_topic: str
    turns: List[DebateTurn]
    consensus_summary: str


class ProviderAdvocate:
    """Independent autonomous agent representative for a specific relief provider."""

    def __init__(self, candidate: Dict[str, Any]):
        self.provider_id = candidate.get("provider_id", "DEPOT")
        self.name = candidate.get("name") or candidate.get("provider_name", "Relief Depot")
        self.org_type = candidate.get("org_type", "NGO")
        self.distance_km = candidate.get("distance_km", 15.0)
        self.eta_hours = candidate.get("eta_hours", 1.0)
        self.inventory = candidate.get("inventory", {})
        self.fleet = candidate.get("fleet_description", "Logistics vehicles")
        self.contact_person = candidate.get("contact_person", "Logistics Officer")

        # Persona customization based on organization profile
        if "HOSP" in self.provider_id or "MEDICAL" in self.provider_id:
            self.role_title = "Chief Medical & Trauma Liaison"
            self.core_priority = "Urgent clinical stabilization, ALS trauma transport, and securing medical supplies."
        elif "TNDRF" in self.provider_id or "RESCUE" in self.provider_id or "NDRF" in self.provider_id:
            self.role_title = "Disaster Rescue Operations Commander"
            self.core_priority = "Rapid physical extraction, water rescue using amphibious boats, and life-safety."
        elif "CSR" in self.provider_id or "TATA" in self.provider_id:
            self.role_title = "Corporate Bulk Supply Chain Director"
            self.core_priority = "Bulk food/water replenishment, power generation, and preserving forward clinic stocks."
        else:
            self.role_title = "Humanitarian Field Aid Coordinator"
            self.core_priority = "Essential family sustenance, hygiene kits, and protecting community reserves."

    async def generate_opening_bid(
        self,
        triage_info: Dict[str, Any],
        weather_info: Dict[str, Any],
        needed_resources: List[str]
    ) -> str:
        """Round 1: Advocate presents capabilities, travel viability, and tactical value."""
        stock_summary = ", ".join([f"{k.replace('_', ' ').title()}: {v}" for k, v in self.inventory.items() if v > 0])
        
        system_prompt = (
            f"You are {self.contact_person}, {self.role_title} representing {self.name}.\n"
            f"Your Core Mission: {self.core_priority}\n"
            f"Your Location: {self.distance_km} km away (ETA ~{self.eta_hours}h). Fleet: {self.fleet}.\n"
            f"Your Live Stock: {stock_summary or 'General Supplies'}.\n"
            "Argue in 2-3 assertive, professional first-person sentences why your organization is best suited to deploy, "
            "taking into account the weather hazards and victim triage urgency."
        )

        user_prompt = (
            f"Incident Priority: {triage_info.get('priority_level', 'P1_CRITICAL')}\n"
            f"Casualty Status: {triage_info.get('clinical_assessment', 'Victims in need')}\n"
            f"Weather Telemetry: {weather_info.get('hazard_classification', 'FLOOD')} "
            f"(Water Depth: {weather_info.get('estimated_water_depth_m', 0.5)}m, Rain: {weather_info.get('precipitation_rate_mm_hr', 50)}mm/h)\n"
            f"Requested Aid: {', '.join(needed_resources) if needed_resources else 'Emergency Aid'}\n"
            "State your opening deployment bid."
        )

        fallback = (
            f"[{self.name}] We are {self.distance_km} km out with an ETA of {self.eta_hours}h. "
            f"With our fleet of {self.fleet} and stock of {stock_summary}, we are ready for immediate dispatch to fulfill critical demand."
        )

        try:
            return await groq_service.stream_text(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                agent_name=f"Advocate_{self.provider_id}",
                fallback_text=fallback
            )
        except Exception:
            return fallback

    async def generate_rebuttal(
        self,
        triage_info: Dict[str, Any],
        competitor_bids: List[Dict[str, str]]
    ) -> str:
        """Round 2: Reviews competitors' arguments, challenges bottlenecks, and proposes a consensus compromise."""
        other_bids_text = "\n".join([f"- {b['name']} ({b['role']}): \"{b['bid']}\"" for b in competitor_bids if b['provider_id'] != self.provider_id])
        
        system_prompt = (
            f"You are {self.contact_person}, {self.role_title} for {self.name}.\n"
            "Review the competing deployment bids from other relief agencies below. "
            "In 2 sentences, either challenge their logistical bottlenecks (e.g. vehicle access, inventory depletion) "
            "or propose a collaborative split (e.g. one team extracts while your team supplies kits)."
        )

        user_prompt = (
            f"Incident: {triage_info.get('triage_summary', 'Emergency Response')}\n"
            f"Competitor Bids:\n{other_bids_text or 'None'}\n"
            "State your tactical rebuttal or collaborative compromise."
        )

        fallback = f"[{self.name}] We support prioritizing frontline extraction from closest units, while our depot stands ready to supply bulk replenishment to avoid local stock depletion."

        try:
            return await groq_service.stream_text(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                agent_name=f"Rebuttal_{self.provider_id}",
                fallback_text=fallback
            )
        except Exception:
            return fallback


class AdvocatesAgent:
    name = "A4_Advocates"

    async def deliberate(
        self,
        candidates: List[Dict[str, Any]],
        triage_info: Dict[str, Any],
        needed_resources: List[Dict[str, Any]],
        run_id: str
    ) -> Dict[str, Any]:
        await event_bus.emit(
            "agent.entered",
            self.name,
            {"stage": "A4", "description": "Autonomous Multi-Agent Provider Deliberation"},
            run_id=run_id
        )

        await event_bus.emit("debate.opened", self.name, {"candidate_count": len(candidates)}, run_id=run_id)

        if not candidates:
            return {
                "debate_topic": "No candidate depots within search perimeter",
                "turns": [],
                "consensus_summary": "No candidate facilities available for deliberation."
            }

        # Instantiate independent agent representatives (top 4 candidate depots)
        top_candidates = candidates[:4]
        advocates = [ProviderAdvocate(c) for c in top_candidates]
        needed_labels = [r.get("label", "Aid") for r in needed_resources]
        weather_info = triage_info.get("weather_telemetry", {})

        turns: List[DebateTurn] = []

        # =========================================================================
        # ROUND 1: OPENING BIDS & CLAIMS
        # =========================================================================
        round1_bids = []
        for adv in advocates:
            argument = await adv.generate_opening_bid(
                triage_info=triage_info,
                weather_info=weather_info,
                needed_resources=needed_labels
            )
            turn = DebateTurn(
                turn_id=f"r1_{adv.provider_id}",
                speaker=adv.provider_id,
                speaker_name=adv.name,
                role_title=adv.role_title,
                stance="advocate",
                argument=argument,
                rebuts=None
            )
            turns.append(turn)
            round1_bids.append({
                "provider_id": adv.provider_id,
                "name": adv.name,
                "role": adv.role_title,
                "bid": argument
            })

            # Stream real-time debate turn to live terminal UI
            await event_bus.emit(
                "debate.turn",
                self.name,
                {
                    "speaker": adv.name,
                    "role": adv.role_title,
                    "stance": "Opening Proposal",
                    "argument": argument
                },
                run_id=run_id
            )
            await asyncio.sleep(0.05)

        # =========================================================================
        # ROUND 2: CROSS-AGENCY REBUTTALS & COLLABORATIVE COMPROMISE
        # =========================================================================
        for adv in advocates:
            rebuttal = await adv.generate_rebuttal(
                triage_info=triage_info,
                competitor_bids=round1_bids
            )
            turn = DebateTurn(
                turn_id=f"r2_{adv.provider_id}",
                speaker=adv.provider_id,
                speaker_name=adv.name,
                role_title=adv.role_title,
                stance="compromise",
                argument=rebuttal,
                rebuts="Round 1 Proposals"
            )
            turns.append(turn)

            await event_bus.emit(
                "debate.turn",
                self.name,
                {
                    "speaker": adv.name,
                    "role": adv.role_title,
                    "stance": "Tactical Rebuttal & Consensus",
                    "argument": rebuttal
                },
                run_id=run_id
            )
            await asyncio.sleep(0.05)

        consensus = (
            f"Multi-agency consensus reached among {len(advocates)} organizations. "
            "Frontline rapid extraction is allocated to the closest specialized units, while regional warehouses maintain supply chain buffers."
        )

        debate_result = {
            "debate_topic": f"Multi-Agency Response Allocation for {triage_info.get('priority_level', 'P1_CRITICAL')} incident",
            "turns": [t.model_dump() for t in turns],
            "consensus_summary": consensus
        }

        await event_bus.emit(
            "agent.completed",
            self.name,
            {
                "turns_count": len(turns),
                "consensus": consensus
            },
            run_id=run_id
        )

        return debate_result


a4_advocates = AdvocatesAgent()
```

---

<a id="file-app-agents-a5_solver-py"></a>
## File: `app/agents/a5_solver.py`

```python
"""
Agent A5: Allocation Solver (Pure Python Deterministic Optimizer).
Calculates exact mathematically verified resource allocations without any LLM hallucination.
Emits exactly 3 fixed candidate plans: [1] fastest, [2] max_coverage, [3] least_depleting.
"""

from typing import Dict, Any, List
import copy
from app.bus.eventbus import event_bus


class AllocationSolverAgent:
    name = "A5_Solver"

    async def solve(
        self,
        need_items: List[Dict[str, Any]],
        candidates: List[Dict[str, Any]],
        run_id: str,
        pinned_provider_id: str = None
    ) -> Dict[str, Any]:
        """
        Solves allocation arithmetic deterministically.
        Generates 3 named candidate options.
        """
        await event_bus.emit(
            "agent.entered",
            self.name,
            {"stage": "A5", "description": "Deterministic Allocation Optimization (Python Math)"},
            run_id=run_id
        )

        # Build demand dictionary
        demand: Dict[str, int] = {}
        for item in need_items:
            key = item.get("resource_key")
            qty = item.get("quantity", 1)
            demand[key] = demand.get(key, 0) + qty

        # Sort candidate list for the 3 distinct strategies
        # 1. Fastest: Sorted by distance / ETA ascending
        cand_fastest = sorted(candidates, key=lambda c: (c.get("distance_km", 999), c.get("eta_hours", 999)))

        # 2. Max Coverage: Sorted by total matching stock descending
        def total_matching_stock(c):
            inv = c.get("inventory", {})
            return sum(inv.get(k, 0) for k in demand)
        cand_coverage = sorted(candidates, key=total_matching_stock, reverse=True)

        # 3. Least Depleting: Sorted by total inventory volume descending (largest hubs first)
        cand_least_depleting = sorted(candidates, key=lambda c: sum(c.get("inventory", {}).values()), reverse=True)

        # If admin pinned a provider, prioritize them at the front
        if pinned_provider_id:
            def pin_filter(lst):
                pinned = [c for c in lst if c.get("provider_id") == pinned_provider_id]
                rest = [c for c in lst if c.get("provider_id") != pinned_provider_id]
                return pinned + rest
            cand_fastest = pin_filter(cand_fastest)
            cand_coverage = pin_filter(cand_coverage)
            cand_least_depleting = pin_filter(cand_least_depleting)

        option_fastest = self._build_plan("fastest", "Rapid Response (Fastest Arrival)", "Minimizes travel time by deploying closest available response squads.", demand, cand_fastest)
        option_coverage = self._build_plan("max_coverage", "Maximum Coverage Plan", "Fulfills the highest possible percentage of total relief items.", demand, cand_coverage)
        option_least_depleting = self._build_plan("least_depleting", "Depletion-Balanced Plan", "Draws stock from large regional distribution centers to protect forward clinic reserves.", demand, cand_least_depleting)

        options = {
            "fastest": option_fastest,
            "max_coverage": option_coverage,
            "least_depleting": option_least_depleting
        }

        await event_bus.emit(
            "options.proposed",
            self.name,
            {
                "option_count": 3,
                "options": options
            },
            run_id=run_id
        )

        return options

    def _build_plan(
        self,
        opt_id: str,
        title: str,
        desc: str,
        demand: Dict[str, int],
        sorted_candidates: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Greedy allocation against candidate inventory."""
        rem_demand = dict(demand)
        allocations = []
        total_fulfilled = {k: 0 for k in demand}
        max_eta = 0.0

        for cand in sorted_candidates:
            p_id = cand.get("provider_id")
            p_name = cand.get("provider_name") or cand.get("name")
            p_inv = cand.get("inventory", {})
            dist_km = cand.get("distance_km", 5.0)
            eta_h = cand.get("eta_hours", 1.0)

            allocated_from_cand = {}
            for res_key, req_qty in list(rem_demand.items()):
                if req_qty <= 0:
                    continue
                avail = p_inv.get(res_key, 0)
                if avail > 0:
                    give = min(avail, req_qty)
                    allocated_from_cand[res_key] = give
                    rem_demand[res_key] -= give
                    total_fulfilled[res_key] += give

            if allocated_from_cand:
                max_eta = max(max_eta, eta_h)
                allocations.append({
                    "provider_id": p_id,
                    "provider_name": p_name,
                    "distance_km": dist_km,
                    "eta_hours": eta_h,
                    "items": allocated_from_cand
                })

        total_req = sum(demand.values())
        total_got = sum(total_fulfilled.values())
        coverage_ratio = round(total_got / total_req, 2) if total_req > 0 else 1.0

        if opt_id == "least_depleting":
            depletion = "low"
        elif opt_id == "fastest":
            depletion = "medium"
        else:
            depletion = "medium-high"

        return {
            "option_id": opt_id,
            "title": title,
            "description": desc,
            "allocations": allocations,
            "total_fulfilled": total_fulfilled,
            "demand": demand,
            "coverage_ratio": coverage_ratio,
            "max_eta_hours": max_eta or 1.0,
            "depletion_impact": depletion
        }


a5_solver = AllocationSolverAgent()
```

---

<a id="file-app-agents-a6_arbiter-py"></a>
## File: `app/agents/a6_arbiter.py`

```python
"""
Agent A6: Arbiter (Groq LLM with Strict Pydantic Validation & Hallucination Firewall).
Selects a single pre-calculated option_id from the A5 Solver based on the A4 debate.
Enforces the Hallucination Firewall: Strictly prohibited from modifying numbers.
"""

from typing import Dict, Any
from pydantic import BaseModel, Field
from app.agents.llm_client import groq_service
from app.bus.eventbus import event_bus


class ArbiterDecision(BaseModel):
    selected_option_id: str = Field(..., description="Must be one of: fastest | max_coverage | least_depleting")
    reasoning: str = Field(..., description="Tactical justification for the chosen allocation plan")
    confidence_score: float = Field(..., ge=0.0, le=1.0)


class ArbiterAgent:
    name = "A6_Arbiter"

    async def arbitrate(
        self,
        options: Dict[str, Any],
        triage_info: Dict[str, Any],
        debate_info: Dict[str, Any],
        run_id: str
    ) -> Dict[str, Any]:
        await event_bus.emit(
            "agent.entered",
            self.name,
            {"stage": "A6", "description": "Plan Arbitration & Selection (Hallucination Firewalled)"},
            run_id=run_id
        )

        priority = triage_info.get("priority_level", "P2_HIGH")

        # Deterministic fallback decision
        if priority == "P1_CRITICAL":
            fallback_id = "fastest"
            fallback_reason = "Critical life-safety threat mandates fastest physical arrival time over secondary stock considerations."
        elif options.get("max_coverage", {}).get("coverage_ratio", 0) > options.get("fastest", {}).get("coverage_ratio", 0):
            fallback_id = "max_coverage"
            fallback_reason = "Maximizing total supply coverage provides highest overall relief for the affected group."
        else:
            fallback_id = "least_depleting"
            fallback_reason = "Depletion balancing protects forward medical outposts while fulfilling requested quota."

        fallback_decision = {
            "selected_option_id": fallback_id,
            "reasoning": fallback_reason,
            "confidence_score": 0.95
        }

        system_prompt = (
            "You are the PACT Arbiter Agent. Evaluate the multi-agent debate and triage urgency to select "
            "the single best allocation plan among the 3 provided solver options.\n"
            "HALLUCINATION FIREWALL MANDATE: You are strictly prohibited from generating numbers, modifying stock, "
            "or creating new allocations. You MUST select an existing 'selected_option_id' from ['fastest', 'max_coverage', 'least_depleting'].\n"
            "You must output a JSON object strictly matching this format:\n"
            "{\n"
            '  "selected_option_id": "fastest",\n'
            '  "reasoning": "Tactical justification for this choice.",\n'
            '  "confidence_score": 0.95\n'
            "}"
        )

        options_summary = []
        for opt_id, opt in options.items():
            cov = opt.get("coverage_ratio", 1.0) * 100
            eta = opt.get("max_eta_hours", 1.0)
            dep = opt.get("depletion_impact", "low")
            title = opt.get("title", opt_id)
            options_summary.append(
                f"Option '{opt_id}': {title} - Coverage: {cov}%, Max ETA: {eta}h, Depletion: {dep}"
            )

        # Extract key debate dialogue turns
        debate_turns = debate_info.get("turns", [])
        debate_dialogue = []
        for t in debate_turns[:6]:
            debate_dialogue.append(f"• [{t.get('speaker_name', 'Advocate')}]: \"{t.get('argument')}\"")

        user_prompt = (
            f"TRIAGE PRIORITY: {priority}\n"
            f"MULTI-AGENT DEBATE TRANSCRIPT:\n" + ("\n".join(debate_dialogue) if debate_dialogue else debate_info.get('consensus_summary', 'None')) + "\n\n"
            f"DEBATE CONSENSUS: {debate_info.get('consensus_summary')}\n\n"
            f"AVAILABLE PRE-SOLVED OPTIONS:\n" + "\n".join(options_summary) + "\n\n"
            "As Chief Incident Arbiter, judge the arguments and choose the single winning option."
        )

        result = await groq_service.stream_chat(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            agent_name=self.name,
            run_id=run_id,
            schema=ArbiterDecision,
            fallback_data=fallback_decision
        )

        # Enforce Hallucination Firewall validation
        chosen_id = result.get("selected_option_id")
        if chosen_id not in options:
            await event_bus.emit(
                "error",
                self.name,
                {"warning": f"LLM proposed invalid option_id '{chosen_id}'. Firewalled to fallback '{fallback_id}'."},
                run_id=run_id
            )
            result["selected_option_id"] = fallback_id
            chosen_id = fallback_id

        selected_plan = options[chosen_id]

        await event_bus.emit(
            "decision.proposed",
            self.name,
            {
                "selected_option_id": chosen_id,
                "reasoning": result.get("reasoning"),
                "chosen_plan": selected_plan
            },
            run_id=run_id
        )

        return {
            "decision": result,
            "chosen_plan": selected_plan
        }


a6_arbiter = ArbiterAgent()
```

---

<a id="file-app-agents-a7_redactor-py"></a>
## File: `app/agents/a7_redactor.py`

```python
"""
Agent A7: Privacy Redactor (Deterministic Zero-Knowledge Masking).
Strips exact GPS, MSISDN, and personal identifiers to protect vulnerable disaster victims.
Reveals details only upon mutual plan commitment.
"""

from typing import Dict, Any
from app.bus.eventbus import event_bus


class PrivacyRedactorAgent:
    name = "A7_Redactor"

    async def redact(self, request_data: Dict[str, Any], match_data: Dict[str, Any], run_id: str) -> Dict[str, Any]:
        """
        Creates a masked privacy projection for public/preview consumption.
        """
        await event_bus.emit(
            "agent.entered",
            self.name,
            {"stage": "A7", "description": "Zero-Knowledge Privacy Projection & Identity Masking"},
            run_id=run_id
        )

        geo = request_data.get("geo", {})
        exact_lat = geo.get("latitude", 23.2599)
        exact_lon = geo.get("longitude", 77.4126)

        # 2km grid fuzzing
        masked_lat = round(exact_lat, 2)
        masked_lon = round(exact_lon, 2)

        raw_phone = request_data.get("sender") or request_data.get("phone", "+919876543210")
        masked_phone = raw_phone[:3] + "******" + raw_phone[-4:] if len(raw_phone) >= 7 else "***"

        redacted_view = {
            "uid": request_data.get("uid", "ANON"),
            "masked_phone": masked_phone,
            "masked_coordinates": [masked_lon, masked_lat],
            "general_area": f"Sector ({masked_lat}, {masked_lon})",
            "privacy_state": "ZERO_KNOWLEDGE_PREVIEW",
            "full_unmask_condition": "MUTUAL_COMMITMENT_AND_ACCEPTANCE"
        }

        await event_bus.emit(
            "privacy.reveal",
            self.name,
            {
                "status": "masked_projection_active",
                "redacted_view": redacted_view
            },
            run_id=run_id
        )

        return redacted_view


a7_redactor = PrivacyRedactorAgent()
```

---

<a id="file-app-agents-a8_admin_gate-py"></a>
## File: `app/agents/a8_admin_gate.py`

```python
"""
Agent A8: Admin Gate (Human-in-the-Loop Interrupt & Autopilot Engine).
Parks pipeline on an asyncio.Future keyed by decision_id.
Enables instant dispatcher Approve, Override, or Reject, or automated dispatch via Autopilot timer.
"""

import asyncio
import time
import logging
from typing import Dict, Any, Optional
from app.config import AUTOPILOT_ENABLED, AUTOPILOT_TIMEOUT_SECONDS
from app.bus.eventbus import event_bus
from app.db.mongo import get_collection

logger = logging.getLogger("pact.admin_gate")


class AdminGateAgent:
    name = "A8_AdminGate"

    def __init__(self):
        self._pending_futures: Dict[str, asyncio.Future] = {}
        self._pending_decisions: Dict[str, Dict[str, Any]] = {}
        self.autopilot_enabled: bool = AUTOPILOT_ENABLED
        self.autopilot_timeout: float = AUTOPILOT_TIMEOUT_SECONDS

    async def await_approval(
        self,
        decision_id: str,
        chosen_plan: Dict[str, Any],
        options: Dict[str, Any],
        run_id: str
    ) -> Dict[str, Any]:
        """
        Pauses execution until admin action is submitted or autopilot timeout expires.
        """
        loop = asyncio.get_running_loop()
        fut = loop.create_future()
        self._pending_futures[decision_id] = fut
        self._pending_decisions[decision_id] = {
            "decision_id": decision_id,
            "run_id": run_id,
            "chosen_plan": chosen_plan,
            "options": options,
            "created_at": time.time(),
            "status": "pending_admin"
        }

        await event_bus.emit(
            "awaiting_admin",
            self.name,
            {
                "decision_id": decision_id,
                "chosen_option_id": chosen_plan.get("option_id"),
                "autopilot_enabled": self.autopilot_enabled,
                "autopilot_timeout_seconds": self.autopilot_timeout,
                "options": options
            },
            run_id=run_id
        )

        try:
            if self.autopilot_enabled:
                # Wait with timeout for human interrupt
                try:
                    result = await asyncio.wait_for(fut, timeout=self.autopilot_timeout)
                except asyncio.TimeoutError:
                    result = {
                        "action": "approve",
                        "auto_approved": True,
                        "dispatcher_notes": f"Auto-approved by Autopilot timer ({self.autopilot_timeout}s timeout)."
                    }
                    await event_bus.emit(
                        "admin.action",
                        self.name,
                        {"decision_id": decision_id, "action": "autopilot_approved", "notes": result["dispatcher_notes"]},
                        run_id=run_id
                    )
            else:
                # Wait indefinitely for admin action
                result = await fut
                await event_bus.emit(
                    "admin.action",
                    self.name,
                    {"decision_id": decision_id, "action": result.get("action"), "details": result},
                    run_id=run_id
                )

            # Record in admin_actions collection (never TTL)
            admin_actions_col = get_collection("admin_actions")
            await admin_actions_col.insert_one({
                "decision_id": decision_id,
                "run_id": run_id,
                "action": result.get("action"),
                "auto_approved": result.get("auto_approved", False),
                "details": result,
                "timestamp": time.time()
            })

            return result

        finally:
            self._pending_futures.pop(decision_id, None)
            self._pending_decisions.pop(decision_id, None)

    def resolve_decision(self, decision_id: str, action_data: Dict[str, Any]) -> bool:
        """Called by HTTP REST admin action endpoint."""
        fut = self._pending_futures.get(decision_id)
        if fut and not fut.done():
            fut.set_result(action_data)
            return True
        return False

    def list_pending(self) -> Dict[str, Any]:
        return self._pending_decisions

    def set_autopilot(self, enabled: bool, timeout_seconds: Optional[float] = None):
        self.autopilot_enabled = enabled
        if timeout_seconds:
            self.autopilot_timeout = timeout_seconds


a8_admin_gate = AdminGateAgent()
```

---

<a id="file-app-agents-a9_narrator-py"></a>
## File: `app/agents/a9_narrator.py`

```python
"""
Agent A9: Narrator (Groq LLM / Fallback).
Generates plain-English situational bulletins and live operational dispatch logs.
"""

from typing import Dict, Any
from pydantic import BaseModel, Field
from app.agents.llm_client import groq_service
from app.bus.eventbus import event_bus


class NarratorOutput(BaseModel):
    operational_bulletin: str = Field(..., description="Clear, professional plain-English dispatch bulletin")
    key_action_items: list[str] = Field(default_factory=list)


class NarratorAgent:
    name = "A9_Narrator"

    async def narrate(
        self,
        request_data: Dict[str, Any],
        triage_info: Dict[str, Any],
        chosen_plan: Dict[str, Any],
        admin_action: Dict[str, Any],
        run_id: str
    ) -> Dict[str, Any]:
        await event_bus.emit(
            "agent.entered",
            self.name,
            {"stage": "A9", "description": "Operational Dispatch Narration"},
            run_id=run_id
        )

        providers = [a.get("provider_name") for a in chosen_plan.get("allocations", [])]
        prov_str = ", ".join(providers) if providers else "Assigned Response Units"
        total_items = chosen_plan.get("total_fulfilled", {})
        item_summary = ", ".join(f"{v} {k}" for k, v in total_items.items() if v > 0)

        fallback_bulletin = (
            f"DISPATCH COMMITTED: Responding to {triage_info.get('priority_level', 'P1')} emergency. "
            f"{prov_str} tasked with immediate transit (ETA: {chosen_plan.get('max_eta_hours')}h). "
            f"Mobilizing {item_summary or 'emergency kits'} under plan '{chosen_plan.get('option_id')}'. "
            f"Action verified by {admin_action.get('dispatcher_notes', 'Admin Gate')}."
        )

        fallback_data = {
            "operational_bulletin": fallback_bulletin,
            "key_action_items": [
                f"Dispatch units: {prov_str}",
                f"Supplies committed: {item_summary}",
                f"Estimated arrival: within {chosen_plan.get('max_eta_hours')} hours"
            ]
        }

        system_prompt = (
            "You are the PACT Operational Narrator. Generate a succinct, high-clarity emergency response bulletin "
            "summarizing the finalized dispatch decision for commanders and field operators.\n"
            "You must output a JSON object strictly matching this format:\n"
            "{\n"
            '  "operational_bulletin": "DISPATCH COMMITTED: Responding to critical emergency...",\n'
            '  "key_action_items": ["Action 1", "Action 2"]\n'
            "}"
        )

        user_prompt = (
            f"PRIORITY: {triage_info.get('priority_level')}\n"
            f"PLAN: {chosen_plan.get('title')} ({chosen_plan.get('option_id')})\n"
            f"PROVIDERS: {prov_str}\n"
            f"FULFILLED SUPPLIES: {item_summary}\n"
            f"MAX ETA: {chosen_plan.get('max_eta_hours')} hours\n"
            f"ADMIN STATUS: {admin_action.get('action')}"
        )

        result = await groq_service.stream_chat(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            agent_name=self.name,
            run_id=run_id,
            schema=NarratorOutput,
            fallback_data=fallback_data
        )

        await event_bus.emit(
            "agent.message",
            self.name,
            {
                "stage": "A9",
                "bulletin": result,
                "text": result.get("operational_bulletin"),
                "action_items": result.get("key_action_items")
            },
            run_id=run_id
        )

        return result


a9_narrator = NarratorAgent()
```

---

<a id="file-app-agents-a10_verify-py"></a>
## File: `app/agents/a10_verify.py`

```python
"""
Agent A10: Verification & Digital Handshake (Deterministic Python).
Commits allocation to MongoDB, deducts provider stock to prevent double-booking,
and generates the canonical GSM-7 confirmation SMS frame.
"""

import time
import uuid
from typing import Dict, Any, List
from app.db.mongo import get_collection
from app.codec.checksum import calculate_xor_checksum
from app.bus.eventbus import event_bus


class VerificationAgent:
    name = "A10_Verification"

    async def commit_and_verify(
        self,
        request_data: Dict[str, Any],
        triage_info: Dict[str, Any],
        chosen_plan: Dict[str, Any],
        admin_action: Dict[str, Any],
        run_id: str
    ) -> Dict[str, Any]:
        await event_bus.emit(
            "agent.entered",
            self.name,
            {"stage": "A10", "description": "Database Allocation Commitment & Stock Update"},
            run_id=run_id
        )

        match_id = f"PLAN_{int(time.time()*1000)%100000:05d}"
        uid = request_data.get("uid", "CIT00")
        seq = str(request_data.get("seq", "001"))

        allocations = chosen_plan.get("allocations", [])
        offers_col = get_collection("offers")
        providers_col = get_collection("providers")
        matches_col = get_collection("matches")

        # Deduct inventory in MongoDB
        for alloc in allocations:
            p_id = alloc.get("provider_id")
            items = alloc.get("items", {})
            for res_key, qty in items.items():
                await offers_col.update_one(
                    {"provider_id": p_id},
                    {"$inc": {f"inventory.{res_key}": -qty}}
                )
                await providers_col.update_one(
                    {"provider_id": p_id},
                    {"$inc": {f"inventory.{res_key}": -qty}}
                )

        # Generate SMS Confirmation frame for Citizen: C|SEQ|UID|REF|STATE|ETA|CRC
        eta_int = int(round(chosen_plan.get("max_eta_hours", 2.0)))
        ack_body = f"C|{seq}|{uid}|{match_id}|OK|{eta_int}"
        ack_crc = calculate_xor_checksum(ack_body)
        full_ack_sms = f"{ack_body}|{ack_crc}"

        # Generate allocation frames for providers
        provider_sms_frames = []
        for alloc in allocations:
            p_id = alloc.get("provider_id")
            for res_key, qty in alloc.get("items", {}).items():
                p_body = f"A|{seq}|{match_id}|{p_id}|{res_key[:1].upper()}|{qty}|{uid}|{eta_int}"
                p_crc = calculate_xor_checksum(p_body)
                provider_sms_frames.append(f"{p_body}|{p_crc}")

        match_record = {
            "match_id": match_id,
            "run_id": run_id,
            "request_id": request_data.get("raw_frame") or uid,
            "uid": uid,
            "status": "committed",
            "selected_option_id": chosen_plan.get("option_id"),
            "chosen_plan": chosen_plan,
            "triage_info": triage_info,
            "admin_action": admin_action,
            "sms_ack_frame": full_ack_sms,
            "provider_sms_frames": provider_sms_frames,
            "masked": True,
            "revealed": False,
            "created_at": time.time()
        }

        await matches_col.insert_one(match_record)

        await event_bus.emit(
            "decision.committed",
            self.name,
            {
                "match_id": match_id,
                "status": "committed",
                "allocations": allocations,
                "inventory_deducted": True
            },
            run_id=run_id
        )

        await event_bus.emit(
            "notify.sent",
            self.name,
            {
                "recipient": uid,
                "transport": "sms",
                "sms_frame": full_ack_sms,
                "message": f"Confirmation dispatched to victim: {full_ack_sms}"
            },
            run_id=run_id
        )

        await event_bus.emit(
            "verify.result",
            self.name,
            {
                "status": "verified_and_committed",
                "match_id": match_id,
                "ack_frame": full_ack_sms
            },
            run_id=run_id
        )

        return match_record


a10_verify = VerificationAgent()
```

---

<a id="file-app-agents-a11_replan-py"></a>
## File: `app/agents/a11_replan.py`

```python
"""
Agent A11: Replanner Trigger (Deterministic Python).
Handles route blockage, provider rejection, or field delivery failure.
Re-enters the reasoning pipeline at A3 Geo Matcher with updated candidate exclusions.
"""

from typing import Dict, Any, List
from app.bus.eventbus import event_bus


class ReplannerAgent:
    name = "A11_Replanner"

    async def trigger_replan(
        self,
        reason: str,
        failed_provider_ids: List[str],
        request_data: Dict[str, Any],
        run_id: str
    ) -> Dict[str, Any]:
        await event_bus.emit(
            "agent.entered",
            self.name,
            {"stage": "A11", "description": "Replanning Trigger & Route Invalidation"},
            run_id=run_id
        )

        await event_bus.emit(
            "replan.triggered",
            self.name,
            {
                "reason": reason,
                "excluded_providers": failed_provider_ids,
                "action": "re-entering pipeline at A3 (Geo Matcher)"
            },
            run_id=run_id
        )

        return {
            "replan_needed": True,
            "reason": reason,
            "excluded_providers": failed_provider_ids
        }


a11_replan = ReplannerAgent()
```

---

<a id="file-app-api-ingest-py"></a>
## File: `app/api/ingest.py`

```python
"""
Unified Ingestion API Endpoints.
Provides /api/v1/pact/ingest (unified wire format) and /api/v1/sms/webhook (gateway adapter).
"""

from fastapi import APIRouter, Request, HTTPException
from app.agents.pipeline import pipeline

router = APIRouter(prefix="/api/v1", tags=["Ingest"])


@router.post("/pact/ingest")
async def ingest_pact_wire(request: Request):
    """
    Unified Ingestion Endpoint.
    Accepts raw GSM-7 wire format string (plain text) or JSON payload.
    Processes frame through the 12-stage multi-agent pipeline.
    """
    content_type = request.headers.get("content-type", "")
    raw_payload = ""
    sender = "UNKNOWN"
    transport = "http"

    if "application/json" in content_type:
        try:
            data = await request.json()
            raw_payload = data.get("text") or data.get("body") or data.get("Body") or data.get("payload") or ""
            sender = data.get("sender") or data.get("From") or data.get("from") or "APP_HTTP"
            transport = data.get("transport", "http")
        except Exception:
            pass
    elif "application/x-www-form-urlencoded" in content_type or "multipart/form-data" in content_type:
        try:
            form = await request.form()
            raw_payload = str(form.get("Body") or form.get("body") or form.get("text") or "")
            sender = str(form.get("From") or form.get("from") or form.get("sender") or "SMS_GATEWAY")
            transport = str(form.get("transport") or "sms")
        except Exception:
            body_bytes = await request.body()
            raw_payload = body_bytes.decode("utf-8", errors="ignore").strip()
    else:
        body_bytes = await request.body()
        raw_payload = body_bytes.decode("utf-8", errors="ignore").strip()

    if not raw_payload:
        raise HTTPException(status_code=400, detail="Empty payload received")

    result = await pipeline.run(raw_input=raw_payload, transport=transport, sender=sender)
    return result


@router.post("/sms/webhook")
async def sms_webhook(request: Request):
    """
    Adapter endpoint compatible with Termux Rootless SMS Gateway, Twilio, and Cellular Gateways.
    Forwards incoming SMS messages to the PACT ingestion pipeline.
    """
    content_type = request.headers.get("content-type", "")
    msg_body = ""
    msg_from = "TERMUX_SMS"

    if "application/json" in content_type:
        try:
            data = await request.json()
            msg_body = data.get("Body") or data.get("body") or data.get("text") or ""
            msg_from = data.get("From") or data.get("from") or data.get("sender") or "TERMUX_SMS"
        except Exception:
            pass
    elif "application/x-www-form-urlencoded" in content_type or "multipart/form-data" in content_type:
        try:
            form = await request.form()
            msg_body = str(form.get("Body") or form.get("body") or form.get("text") or "")
            msg_from = str(form.get("From") or form.get("from") or form.get("sender") or "TERMUX_SMS")
        except Exception:
            body_bytes = await request.body()
            msg_body = body_bytes.decode("utf-8", errors="ignore").strip()
    else:
        body_bytes = await request.body()
        msg_body = body_bytes.decode("utf-8", errors="ignore").strip()

    if not msg_body:
        raise HTTPException(status_code=400, detail="Missing SMS Body")

    result = await pipeline.run(raw_input=msg_body, transport="sms", sender=msg_from)
    return {
        "status": "received",
        "pipeline_result": result
    }
```

---

<a id="file-app-api-requests-py"></a>
## File: `app/api/requests.py`

```python
"""
Emergency Help Requests API Endpoints.
Supports direct JSON request creation, list, and detail queries.
"""

from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.db.mongo import get_collection
from app.db.models import CitizenRequestCreate
from app.codec.requester_codec import encode_requester_payload, encode_q_frame
from app.agents.pipeline import pipeline

router = APIRouter(prefix="/api/v1/requests", tags=["Requests"])


@router.post("")
async def create_request(data: CitizenRequestCreate):
    """
    Creates an emergency request via JSON (used by Android app when online).
    Encodes into compact Base-36 frame and processes through pipeline.
    """
    if data.raw_frame:
        raw_frame = data.raw_frame
    else:
        payload_str = encode_requester_payload(
            situation_code=data.situation_code,
            headcount_code=data.headcount_code,
            injury_code=data.injury_code,
            mobility_code=data.mobility_code,
            urgency_code=data.urgency_code,
            needs_keys_or_bits=data.needs_keys,
            vulnerability_bits=data.vulnerability_bits
        )
        raw_frame = encode_q_frame(
            seq=data.seq,
            uid=data.uid,
            payload_str=payload_str,
            lat=data.latitude,
            lon=data.longitude
        )

    result = await pipeline.run(raw_input=raw_frame, transport="http", sender=data.uid)
    return result


@router.get("")
async def list_requests(limit: int = Query(50, ge=1, le=200)):
    """Lists all incoming emergency requests."""
    requests_col = get_collection("requests")
    cursor = requests_col.find({}).sort("created_at", -1).limit(limit)
    items = await cursor.to_list(limit)
    return {"count": len(items), "requests": items}


@router.get("/{req_id}")
async def get_request(req_id: str):
    """Retrieves a single request by ID or UID."""
    requests_col = get_collection("requests")
    doc = await requests_col.find_one({"$or": [{"_id": req_id}, {"run_id": req_id}, {"parsed.uid": req_id}]})
    if not doc:
        raise HTTPException(status_code=404, detail="Request not found")
    return doc
```

---

<a id="file-app-api-offers-py"></a>
## File: `app/api/offers.py`

```python
"""
Provider Resource Offers API Endpoints.
Allows relief agencies to register, list, get details, and update stockpiles.
"""

from fastapi import APIRouter, HTTPException, Query
import time
from app.db.mongo import get_collection
from app.db.models import ProviderOfferCreate
from app.codec.pack10 import encode_pack10
from app.codec.taxonomy import RESOURCE_BY_KEY

router = APIRouter(prefix="/api/v1/offers", tags=["Offers"])


@router.post("")
async def create_offer(data: ProviderOfferCreate):
    """Registers a new provider resource offer and spatial depot."""
    offers_col = get_collection("offers")
    providers_col = get_collection("providers")

    # Compute resource bitfield
    bitfield = 0
    for key in data.offered_resource_keys:
        if key in RESOURCE_BY_KEY:
            bitfield |= (1 << RESOURCE_BY_KEY[key]["bit"])

    offer_doc = {
        "offer_id": f"OFFER_{data.provider_id}",
        "provider_id": data.provider_id,
        "provider_name": data.organization_name,
        "org_type_code": data.org_type_code,
        "loc": {"type": "Point", "coordinates": [data.longitude, data.latitude]},
        "pack10": encode_pack10(data.latitude, data.longitude),
        "resource_bitfield": bitfield,
        "inventory": data.stock,
        "status": "available",
        "contact_phone": data.contact_phone,
        "created_at": time.time()
    }

    await offers_col.update_one({"provider_id": data.provider_id}, {"$set": offer_doc}, upsert=True)
    await providers_col.update_one({"provider_id": data.provider_id}, {"$set": offer_doc}, upsert=True)

    return {"status": "registered", "offer": offer_doc}


@router.get("")
async def list_offers(limit: int = Query(50, ge=1, le=100)):
    """Lists all active provider offers."""
    offers_col = get_collection("offers")
    cursor = offers_col.find({}).sort("created_at", -1).limit(limit)
    items = await cursor.to_list(limit)
    return {"count": len(items), "offers": items}


@router.get("/{provider_id}")
async def get_provider_profile(provider_id: str):
    """Gets details, inventory, and location for a specific provider depot."""
    offers_col = get_collection("offers")
    depot = await offers_col.find_one({"provider_id": provider_id})
    if not depot:
        raise HTTPException(status_code=404, detail="Provider depot not found")
    return depot
```

---

<a id="file-app-api-matches-py"></a>
## File: `app/api/matches.py`

```python
"""
Matches and Allocation Plans API Endpoints.
Provides match listing, provider filtering, details, and privacy unmask handshake.
"""

from typing import Optional
from fastapi import APIRouter, HTTPException, Query
from app.db.mongo import get_collection

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
        # Match if allocations list contains this provider_id
        query = {
            "$or": [
                {"allocations.provider_id": provider_id},
                {"selected_plan.allocations.provider_id": provider_id},
                {"plan.allocations.provider_id": provider_id}
            ]
        }

    cursor = matches_col.find(query).sort("created_at", -1).limit(limit)
    items = await cursor.to_list(limit)

    # Attach request geo coordinates & details to each match for interactive mapping
    enriched_items = []
    for m in items:
        run_id = m.get("run_id")
        req_doc = await requests_col.find_one({"run_id": run_id}) if run_id else None
        m_copy = dict(m)
        if req_doc:
            m_copy["request_geo"] = req_doc.get("geo") or req_doc.get("loc")
            m_copy["situation"] = req_doc.get("payload", {}).get("situation", {}).get("name", "Emergency")
            m_copy["urgency"] = req_doc.get("payload", {}).get("urgency", {}).get("label", "Medium")
            m_copy["headcount"] = req_doc.get("payload", {}).get("headcount", {}).get("label", "1 person")
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

    run_id = doc.get("run_id")
    req_doc = await requests_col.find_one({"run_id": run_id}) if run_id else None
    doc_copy = dict(doc)
    if req_doc:
        doc_copy["request_geo"] = req_doc.get("geo") or req_doc.get("loc")
        doc_copy["payload"] = req_doc.get("payload", {})
        doc_copy["raw_frame"] = req_doc.get("raw_frame")

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

    # Fetch full request coordinates
    requests_col = get_collection("requests")
    req = await requests_col.find_one({"run_id": match.get("run_id")})

    return {
        "status": "unmasked",
        "match_id": match_id,
        "revealed": True,
        "exact_location": req.get("loc") if req else None,
        "raw_frame": req.get("raw_frame") if req else None
    }
```

---

<a id="file-app-api-admin-py"></a>
## File: `app/api/admin.py`

```python
"""
Admin Command Center API Endpoints.
Provides system metrics, database seeding, live decision resolution, and autopilot configuration.
"""

from fastapi import APIRouter, HTTPException, Body
from typing import Dict, Any, Optional
from app.db.mongo import get_collection, db_manager
from app.db.seed import seed_database
from app.db.models import AdminActionRequest
from app.agents.a8_admin_gate import a8_admin_gate
from app.config import GROQ_MODEL

router = APIRouter(prefix="/api/v1/admin", tags=["Admin"])


@router.get("/stats")
async def get_system_stats():
    """Returns platform operational metrics and live status."""
    requests_col = get_collection("requests")
    offers_col = get_collection("offers")
    matches_col = get_collection("matches")
    events_col = get_collection("agent_events")

    req_count = await requests_col.count_documents({})
    off_count = await offers_col.count_documents({})
    mat_count = await matches_col.count_documents({})
    evt_count = await events_col.count_documents({})

    return {
        "status": "operational",
        "llm_model": GROQ_MODEL,
        "is_mock_db": db_manager.is_mock(),
        "autopilot": {
            "enabled": a8_admin_gate.autopilot_enabled,
            "timeout_seconds": a8_admin_gate.autopilot_timeout,
        },
        "metrics": {
            "total_requests": req_count,
            "active_offers": off_count,
            "committed_matches": mat_count,
            "agent_events_emitted": evt_count
        },
        "pending_decisions_count": len(a8_admin_gate.list_pending())
    }


@router.post("/seed")
async def trigger_seed(force: bool = True):
    """Resets and seeds default disaster relief depots and inventory."""
    await seed_database(force=force)
    return {"status": "seeded", "message": "Relief provider inventory seeded successfully."}


@router.get("/decisions/pending")
async def list_pending_decisions():
    """Lists all decisions waiting for human dispatcher action."""
    return {"pending": a8_admin_gate.list_pending()}


@router.post("/decisions/{decision_id}/action")
async def submit_admin_action(decision_id: str, action: AdminActionRequest):
    """
    Submits an Approve, Override, or Reject action to the A8 Admin Gate.
    Resolves the parked asyncio.Future in the agent pipeline.
    """
    action_data = action.model_dump()
    resolved = a8_admin_gate.resolve_decision(decision_id, action_data)
    if not resolved:
        raise HTTPException(status_code=404, detail=f"Pending decision '{decision_id}' not found or already resolved.")
    return {"status": "resolved", "decision_id": decision_id, "action": action.action}


@router.post("/autopilot")
async def configure_autopilot(
    enabled: bool = Body(..., embed=True),
    timeout_seconds: Optional[float] = Body(None, embed=True)
):
    """Enables/disables Autopilot auto-dispatch timer."""
    a8_admin_gate.set_autopilot(enabled, timeout_seconds)
    return {
        "status": "updated",
        "autopilot_enabled": a8_admin_gate.autopilot_enabled,
        "timeout_seconds": a8_admin_gate.autopilot_timeout
    }
```

---

<a id="file-app-api-simulator-py"></a>
## File: `app/api/simulator.py`

```python
"""
SMS Simulator & Presets API Endpoints.
Allows judges and operators to test raw SMS strings and pre-built disaster scenarios with single clicks.
"""

from fastapi import APIRouter, Body
from typing import Dict, Any, List
from app.codec.checksum import calculate_xor_checksum, append_checksum
from app.agents.pipeline import pipeline

router = APIRouter(prefix="/api/v1/sms", tags=["Simulator"])

PRESETS: List[Dict[str, Any]] = [
    {
        "id": "chennai_velachery_floods",
        "title": "🌊 Chennai Velachery Urban Floods",
        "description": "15 people isolated on rooftop in Velachery, rising water, needs Rescue Boats & Food.",
        "raw_sms": "Q|101|TN01|11414C03L1|64PZKFHQPC|79",
        "category": "tamil_nadu_emergency"
    },
    {
        "id": "chennai_central_collapse",
        "title": "🏢 Chennai Central Building Collapse",
        "description": "4 people trapped under concrete debris near Central, serious trauma, needs Apollo / RG Medical.",
        "raw_sms": "Q|102|TN02|15232C03Q0|64XWUFHUM6|14",
        "category": "tamil_nadu_emergency"
    },
    {
        "id": "ooty_nilgiris_landslide",
        "title": "⛰️ Nilgiris / Ooty Mountain Landslide",
        "description": "25 tourists trapped in vehicles on ghat road, needs 4x4 Mountain Rescue Squad & Blankets.",
        "raw_sms": "Q|103|TN03|15523C0SH0|61CUGFA73K|0C",
        "category": "tamil_nadu_emergency"
    },
    {
        "id": "cuddalore_cyclone_surge",
        "title": "🌀 Cuddalore Coastal Cyclone Surge",
        "description": "65 coastal villagers displaced by high tide surge, needs Emergency Tents & Power Generators.",
        "raw_sms": "Q|104|TN04|10714H07D2|6232WFGRZC|68",
        "category": "tamil_nadu_emergency"
    },
    {
        "id": "coimbatore_industrial_fire",
        "title": "🔥 Coimbatore Factory Fire & Burns",
        "description": "8 workers with burn injuries, needs Medical Team & Burn Kits.",
        "raw_sms": "Q|105|TN05|13322C00I0|60II8FAQU4|78",
        "category": "tamil_nadu_emergency"
    },
    {
        "id": "madurai_heatwave_dehydration",
        "title": "💧 Madurai Dehydration Heatwave",
        "description": "120 elderly & infants dehydrated, needs Clean Water Tankers & Doctors.",
        "raw_sms": "Q|106|TN06|16820H0063|5Y6A0FD8NG|12",
        "category": "tamil_nadu_emergency"
    },
    {
        "id": "building_collapse_sos",
        "title": "🏢 Bhopal Building Collapse (Master Worked Frame)",
        "description": "3-4 people trapped under debris, serious injuries, critical urgency at (23.25991, 77.41263).",
        "raw_sms": "Q|001|7F3K|15223C03Q0|6QR6VFBQ33|7F",
        "category": "citizen_emergency"
    },
    {
        "id": "flood_waterbound_sos",
        "title": "🌊 Flash Flood Waterbound Rescue",
        "description": "16-30 people stranded on rooftop surrounded by rising waters, needs evac transport & food.",
        "raw_sms": "Q|002|9E4F|11504H0810|6QR75FBQ45|4D",
        "category": "citizen_emergency"
    },
    {
        "id": "earthquake_infant_medical",
        "title": "🏚️ Earthquake Trauma with Infants",
        "description": "Family of 4 with infants & elderly, critical trauma injuries, needs doctor & baby care.",
        "raw_sms": "Q|003|2B8M|12230C0243|6QR60FBQ20|1A",
        "category": "citizen_emergency"
    },
    {
        "id": "ngo_bulk_need",
        "title": "📦 NGO Bulk Need Request (N)",
        "description": "Field worker reports need for 300 Food Kits in Region A.",
        "raw_sms": "N|004|NGO01|RA|F|300|H|B3",
        "category": "institutional_need"
    },
    {
        "id": "csr_resource_offer",
        "title": "🚚 CSR Depot Resource Offer (R)",
        "description": "CSR logistics hub announces 200 Food Kits available in Region A.",
        "raw_sms": "R|005|CSR02|RA|F|200|A|7C",
        "category": "provider_offer"
    },
    {
        "id": "delivery_status_delivered",
        "title": "✅ Delivery Completion Status (S)",
        "description": "Driver updates delivery status of Plan PLAN101 to Delivered (3).",
        "raw_sms": "S|006|PLAN101|3|A1",
        "category": "status_update"
    }
]


@router.get("/presets")
async def get_presets():
    """Returns curated disaster demo scenarios for one-click simulation."""
    # Ensure correct dynamic checksums on all presets
    formatted_presets = []
    for p in PRESETS:
        raw = p["raw_sms"]
        if "|" in raw:
            parts = raw.rsplit("|", 1)
            body = parts[0]
            crc = calculate_xor_checksum(body)
            valid_sms = f"{body}|{crc}"
        else:
            valid_sms = raw
        item = dict(p)
        item["raw_sms"] = valid_sms
        formatted_presets.append(item)
    return {"presets": formatted_presets}


@router.post("/simulate")
async def simulate_sms(
    payload: str = Body(..., embed=True),
    sender: str = Body("+919876543210", embed=True)
):
    """
    Simulates sending an emergency SMS to the platform.
    Automatically re-calculates checksum if omitted or incorrect.
    """
    clean = payload.strip()
    if "|" in clean:
        parts = clean.split("|")
        # If user forgot trailing checksum, calculate and append it
        if len(parts) == 5 and parts[0] == "Q":
            clean = append_checksum(clean)
        elif len(parts) >= 2:
            body = clean.rsplit("|", 1)[0]
            crc = calculate_xor_checksum(body)
            clean = f"{body}|{crc}"

    result = await pipeline.run(raw_input=clean, transport="sms_simulator", sender=sender)
    return result
```

---

<a id="file-app-api-ws-py"></a>
## File: `app/api/ws.py`

```python
"""
WebSocket Live Agent Event Streaming Endpoint.
Streams real-time agent deliberations, Groq token emissions, and debate trees to the Admin Portal.
Supports '?since=<seq>' reconnection replay from MongoDB agent_events.
"""

import asyncio
import json
import logging
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from app.bus.eventbus import event_bus

logger = logging.getLogger("pact.ws")
router = APIRouter(tags=["WebSocket"])


@router.websocket("/ws/agents")
async def websocket_agents_endpoint(
    websocket: WebSocket,
    since: int = Query(0, ge=0)
):
    """
    Primary WebSocket Stream for the Admin Command Portal.
    Broadcasts live agent reasoning events, debate trees, tool calls, and LLM tokens.
    """
    await websocket.accept()
    queue = event_bus.subscribe()

    try:
        # Replay history if ?since=<seq> was provided or since=0
        if since > 0:
            history = await event_bus.get_history(since_seq=since, limit=100)
            for event in history:
                await websocket.send_text(json.dumps(event))

        while True:
            event = await queue.get()
            await websocket.send_text(json.dumps(event))

    except (WebSocketDisconnect, asyncio.CancelledError):
        logger.debug("WebSocket client disconnected or connection closed.")
    except Exception as e:
        logger.debug("WebSocket exception: %s", str(e))
    finally:
        event_bus.unsubscribe(queue)
```

---

<a id="file-gateway-termux_gateway-py"></a>
## File: `gateway/termux_gateway.py`

```python
#!/usr/bin/env python3
"""
PACT Termux Rootless SMS Gateway (Clean Upcoming Only).
Silently ignores existing inbox and only triggers on new incoming SMS.
"""

import subprocess
import json
import time
import requests
import re
import sys

BACKEND_URL = "http://localhost:8000/api/v1/sms/webhook"
PACT_PATTERN = re.compile(r'([QGNRASCMPX]|RT)\|\d{3}\|[A-Za-z0-9_]+\|.*')

# Silently snapshot existing inbox so past messages are ignored
processed_ids = set()
try:
    init_res = subprocess.run(["termux-sms-list", "-l", "50"], capture_output=True, text=True)
    if init_res.stdout and init_res.stdout.strip():
        for m in json.loads(init_res.stdout):
            m_id = str(m.get("_id") or m.get("received") or m.get("body"))
            processed_ids.add(m_id)
except Exception:
    pass

print(f"[*] PACT SMS Gateway Online. Waiting for incoming SMS...")

# Live Loop: Only triggers when a new SMS arrives
while True:
    try:
        res = subprocess.run(["termux-sms-list", "-l", "3"], capture_output=True, text=True)
        if res.stdout and res.stdout.strip():
            msgs = json.loads(res.stdout)
            for msg in msgs:
                msg_id = str(msg.get("_id") or msg.get("received") or msg.get("body"))
                raw_body = msg.get("body", "").strip()
                sender = msg.get("number", "UNKNOWN")

                if msg_id not in processed_ids:
                    processed_ids.add(msg_id)
                    match = PACT_PATTERN.search(raw_body)
                    if match:
                        frame = match.group(0).strip()
                        print(f"\n[+] Incoming SOS from {sender}: {frame}")
                        try:
                            r = requests.post(BACKEND_URL, data={"Body": frame, "From": sender, "transport": "sms"}, timeout=8)
                            print(f"[+] Forwarded to laptop (Status {r.status_code})")
                        except Exception as e:
                            print(f"[-] Forward error: {e}", file=sys.stderr)
    except Exception:
        pass

    time.sleep(1.2)
```

---

<a id="file-android-app-src-main-java-org-humanitarian-fieldapp-mainactivity-kt"></a>
## File: `android/app/src/main/java/org/humanitarian/fieldapp/MainActivity.kt`

```kotlin
package org.humanitarian.fieldapp

import android.Manifest
import android.content.pm.PackageManager
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.core.content.ContextCompat
import androidx.lifecycle.lifecycleScope
import com.google.android.gms.location.LocationServices
import com.google.android.gms.location.Priority
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch
import kotlinx.coroutines.suspendCancellableCoroutine
import org.humanitarian.fieldapp.network.ApiClient
import org.humanitarian.fieldapp.ui.FieldReportScreen
import org.humanitarian.fieldapp.ui.HomeScreen
import org.humanitarian.fieldapp.ui.MyRequestsScreen
import org.humanitarian.fieldapp.ui.OfflineMapScreen
import org.humanitarian.fieldapp.ui.SmsDecoderScreen
import org.humanitarian.fieldapp.ui.SmsFallbackScreen
import org.humanitarian.fieldapp.ui.StatusUpdateScreen
import org.humanitarian.fieldapp.ui.theme.PactTheme
import kotlin.coroutines.resume

class MainActivity : ComponentActivity() {

    private val requestPermissionLauncher = registerForActivityResult(
        ActivityResultContracts.RequestMultiplePermissions()
    ) { /* result handled silently for hackathon */ }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        // OSMDroid init
        org.osmdroid.config.Configuration.getInstance().userAgentValue = packageName

        // Request runtime permissions: Location & SMS for direct background dispatch
        val requiredPermissions = arrayOf(
            Manifest.permission.SEND_SMS,
            Manifest.permission.READ_SMS,
            Manifest.permission.RECEIVE_SMS,
            Manifest.permission.ACCESS_FINE_LOCATION,
            Manifest.permission.ACCESS_COARSE_LOCATION
        )
        val missingPermissions = requiredPermissions.filter {
            ContextCompat.checkSelfPermission(this, it) != PackageManager.PERMISSION_GRANTED
        }.toTypedArray()

        if (missingPermissions.isNotEmpty()) {
            requestPermissionLauncher.launch(missingPermissions)
        }

        // START REAL-TIME LOCATION SENDER (every 10 seconds)
        startRealTimeLocationSender()

        setContent {
            PactTheme {
                var currentScreen by remember { mutableStateOf("home") }

                when (currentScreen) {
                    "home" -> HomeScreen(
                        onNavigateToFieldReport = { currentScreen = "field_report" },
                        onNavigateToMyRequests = { currentScreen = "my_requests" },
                        onNavigateToSmsFallback = { currentScreen = "sms_fallback" },
                        onNavigateToSmsDecoder = { currentScreen = "sms_decoder" },
                        onNavigateToOfflineMap = { currentScreen = "offline_map" },
                        onNavigateToStatus = { currentScreen = "status_update" }
                    )
                    "field_report" -> FieldReportScreen(onBack = { currentScreen = "home" }, onReturnHome = { currentScreen = "home" })
                    "my_requests" -> MyRequestsScreen(onBack = { currentScreen = "home" })
                    "sms_fallback" -> SmsFallbackScreen(onBack = { currentScreen = "home" })
                    "sms_decoder" -> SmsDecoderScreen(onBack = { currentScreen = "home" })
                    "offline_map" -> OfflineMapScreen(onBack = { currentScreen = "home" })
                    "status_update" -> StatusUpdateScreen(onBack = { currentScreen = "home" })
                }
            }
        }
    }

    private fun startRealTimeLocationSender() {
        val fused = LocationServices.getFusedLocationProviderClient(this)
        lifecycleScope.launch {
            while (true) {
                if (ContextCompat.checkSelfPermission(this@MainActivity, Manifest.permission.ACCESS_FINE_LOCATION) == PackageManager.PERMISSION_GRANTED) {
                    try {
                        val location = suspendCancellableCoroutine { cont ->
                            fused.getCurrentLocation(Priority.PRIORITY_HIGH_ACCURACY, null)
                                .addOnSuccessListener { loc -> cont.resume(loc) }
                                .addOnFailureListener { cont.resume(null) }
                        }
                        if (location != null) {
                            ApiClient.postLocationUpdate("NGO01", location.latitude, location.longitude)
                        }
                    } catch (_: Exception) {
                        // ignore GPS/network errors silently
                    }
                }
                delay(10_000) // send every 10 seconds
            }
        }
    }
}
```

---

<a id="file-android-app-src-main-java-org-humanitarian-fieldapp-sms-base36-kt"></a>
## File: `android/app/src/main/java/org/humanitarian/fieldapp/sms/Base36.kt`

```kotlin
package org.humanitarian.fieldapp.sms

/**
 * Base-36 encoding and decoding utilities matching the PACT Python backend.
 * Alphabet: 0-9, A-Z (radix 36).
 */
object Base36 {

    private const val ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    private val CHAR_MAP = ALPHABET.mapIndexed { index, char -> char to index.toLong() }.toMap()

    fun encode(number: Long, minLength: Int = 0): String {
        if (number < 0) {
            throw IllegalArgumentException("Cannot encode negative integer $number in base36")
        }
        if (number == 0L) {
            return "0".padStart(minLength, '0')
        }

        val chars = StringBuilder()
        var n = number
        while (n > 0) {
            val rem = (n % 36).toInt()
            chars.append(ALPHABET[rem])
            n /= 36
        }

        val encoded = chars.reverse().toString()
        return if (minLength > 0 && encoded.length < minLength) {
            encoded.padStart(minLength, '0')
        } else {
            encoded
        }
    }

    fun decode(s: String): Long {
        val trimmed = s.trim().uppercase()
        if (trimmed.isEmpty()) {
            throw IllegalArgumentException("Cannot decode empty string in base36")
        }
        var value = 0L
        for (char in trimmed) {
            val digit = CHAR_MAP[char] ?: throw IllegalArgumentException("Invalid Base-36 character '$char' in '$s'")
            value = value * 36 + digit
        }
        return value
    }
}
```

---

<a id="file-android-app-src-main-java-org-humanitarian-fieldapp-sms-pack10-kt"></a>
## File: `android/app/src/main/java/org/humanitarian/fieldapp/sms/Pack10.kt`

```kotlin
package org.humanitarian.fieldapp.sms

import kotlin.math.roundToLong

/**
 * PACK10 Geolocation Codec matching PACT Python specification.
 * Encodes GPS latitude/longitude into a 10-character Base-36 string with ~1.1m precision.
 */
object Pack10 {

    data class GeoDecoded(
        val latitude: Double,
        val longitude: Double,
        val accuracyMeters: Int = 5
    )

    fun encode(lat: Double, lon: Double): String {
        val clampedLat = lat.coerceIn(-90.0, 90.0)
        val clampedLon = lon.coerceIn(-180.0, 180.0)

        val latOffset = ((clampedLat + 90.0) * 100000.0).roundToLong()
        val lonOffset = ((clampedLon + 180.0) * 100000.0).roundToLong()

        val latToken = Base36.encode(latOffset, minLength = 5)
        val lonToken = Base36.encode(lonOffset, minLength = 5)

        return latToken + lonToken
    }

    fun decode(pack10Str: String): GeoDecoded {
        val s = pack10Str.trim().uppercase()
        if (s.length < 10) {
            throw IllegalArgumentException("PACK10 string must be at least 10 characters: '$pack10Str'")
        }

        val latToken = s.substring(0, 5)
        val lonToken = s.substring(5, 10)

        val latOffset = Base36.decode(latToken)
        val lonOffset = Base36.decode(lonToken)

        val lat = (latOffset / 100000.0) - 90.0
        val lon = (lonOffset / 100000.0) - 180.0

        val roundedLat = (lat * 100000.0).roundToLong() / 100000.0
        val roundedLon = (lon * 100000.0).roundToLong() / 100000.0

        return GeoDecoded(
            latitude = roundedLat,
            longitude = roundedLon,
            accuracyMeters = 5
        )
    }
}
```

---

<a id="file-android-app-src-main-java-org-humanitarian-fieldapp-sms-checksum-kt"></a>
## File: `android/app/src/main/java/org/humanitarian/fieldapp/sms/Checksum.kt`

```kotlin
package org.humanitarian.fieldapp.sms

fun xorChecksum(text: String): String {
    var value = 0

    for (character in text) {
        value = value.xor(character.code)
    }

    return value.toString(16).uppercase().padStart(2, '0')
}
```

---

<a id="file-android-app-src-main-java-org-humanitarian-fieldapp-sms-smscodes-kt"></a>
## File: `android/app/src/main/java/org/humanitarian/fieldapp/sms/SmsCodes.kt`

```kotlin
package org.humanitarian.fieldapp.sms

private val validLocationCodes = setOf(
    "RA",
    "RB",
    "RC",
    "D1",
    "D2"
)

private val validResourceCodes = setOf(
    "F",
    "W",
    "M",
    "T",
    "B",
    "H",
    "D",
    "U"
)

private val validUrgencyCodes = setOf(
    "L",
    "M",
    "H",
    "C"
)

fun locationCode(value: String): String {
    val cleaned = value.trim().uppercase()

    return when {
        cleaned in validLocationCodes -> cleaned
        cleaned == "REGION A" -> "RA"
        cleaned == "REGION B" -> "RB"
        cleaned == "REGION C" -> "RC"
        cleaned == "DISTRICT NORTH" -> "D1"
        cleaned == "DISTRICT SOUTH" -> "D2"
        else -> cleaned.take(8).ifBlank { "RA" }
    }
}

fun resourceCode(value: String): String {
    val cleaned = value.trim().uppercase()

    return when {
        cleaned in validResourceCodes -> cleaned
        cleaned == "FOOD" -> "F"
        cleaned == "FOOD KITS" -> "F"
        cleaned == "FOOD_KITS" -> "F"
        cleaned == "WATER" -> "W"
        cleaned == "WATER KITS" -> "W"
        cleaned == "WATER_KITS" -> "W"
        cleaned == "MEDICAL" -> "M"
        cleaned == "MEDICAL KITS" -> "M"
        cleaned == "MEDICAL_KITS" -> "M"
        cleaned == "TENTS" -> "T"
        cleaned == "TENT" -> "T"
        cleaned == "BLANKETS" -> "B"
        cleaned == "BLANKET" -> "B"
        cleaned == "HYGIENE" -> "H"
        cleaned == "HYGIENE KITS" -> "H"
        cleaned == "HYGIENE_KITS" -> "H"
        cleaned == "MEDICAL TEAMS" -> "D"
        cleaned == "MEDICAL_TEAMS" -> "D"
        cleaned == "UNKNOWN" -> "U"
        else -> "U"
    }
}

fun urgencyCode(value: String): String {
    val cleaned = value.trim().uppercase()

    return when {
        cleaned in validUrgencyCodes -> cleaned
        cleaned == "LOW" -> "L"
        cleaned == "MEDIUM" -> "M"
        cleaned == "HIGH" -> "H"
        cleaned == "CRITICAL" -> "C"
        else -> "M"
    }
}
```

---

<a id="file-android-app-src-main-java-org-humanitarian-fieldapp-sms-smsencoder-kt"></a>
## File: `android/app/src/main/java/org/humanitarian/fieldapp/sms/SmsEncoder.kt`

```kotlin
package org.humanitarian.fieldapp.sms

import android.content.Context
import org.humanitarian.fieldapp.models.FieldReport

object SmsEncoder {

    private const val PREFS_NAME = "pact_sms"

    fun nextSequence(
        context: Context,
        organizationId: String
    ): String {
        val safeOrganizationId = organizationId
            .trim()
            .uppercase()
            .ifBlank { "UNKNOWN" }

        val prefs = context.getSharedPreferences(
            PREFS_NAME,
            Context.MODE_PRIVATE
        )

        val key = "sms_seq_$safeOrganizationId"
        val current = prefs.getInt(key, 1)

        val formatted = current.toString().padStart(3, '0')

        val next = if (current >= 999) {
            1
        } else {
            current + 1
        }

        prefs.edit()
            .putInt(key, next)
            .apply()

        return formatted
    }

    /**
     * Encodes a 10-character Base-36 Requester Payload.
     * Schema: [Version(1)][Situation(1)][Headcount(1)][Injury(1)][Mobility(1)][Urgency(1)][Needs(3)][Vuln(1)]
     */
    fun encodeRequesterPayload(
        situationCode: String = "0",
        headcountCode: String = "0",
        injuryCode: String = "0",
        mobilityCode: String = "0",
        urgencyCode: String = "M",
        needsBitfield: Long = 1L, // default bit 0 = Food
        vulnBitfield: Long = 0L,
        version: String = "1"
    ): String {
        val v = version.take(1).ifBlank { "1" }
        val s = situationCode.take(1).ifBlank { "0" }
        val hc = headcountCode.take(1).ifBlank { "0" }
        val inj = injuryCode.take(1).ifBlank { "0" }
        val mob = mobilityCode.take(1).ifBlank { "0" }
        val urg = urgencyCode.take(1).uppercase().ifBlank { "M" }

        val needsStr = Base36.encode(needsBitfield, minLength = 3)
        val vulnStr = Base36.encode(vulnBitfield, minLength = 1)

        return "$v$s$hc$inj$mob$urg$needsStr$vulnStr".take(10)
    }

    /**
     * Encodes a canonical Q Emergency SOS frame:
     * Q|SEQ|UID|PAYLOAD_10|PACK10_GPS_10|CRC
     */
    fun encodeQFrame(
        seq: String,
        uid: String,
        situationCode: String,
        headcountCode: String,
        injuryCode: String,
        mobilityCode: String,
        urgencyCode: String,
        needsBitfield: Long,
        vulnBitfield: Long = 0L,
        latitude: Double,
        longitude: Double
    ): String {
        val safeUid = uid.trim().uppercase().replace("|", "").ifBlank { "TN01" }
        val payloadStr = encodeRequesterPayload(
            situationCode = situationCode,
            headcountCode = headcountCode,
            injuryCode = injuryCode,
            mobilityCode = mobilityCode,
            urgencyCode = urgencyCode,
            needsBitfield = needsBitfield,
            vulnBitfield = vulnBitfield
        )

        val pack10Geo = Pack10.encode(latitude, longitude)
        val body = "Q|$seq|$safeUid|$payloadStr|$pack10Geo"
        val checksum = xorChecksum(body)
        return "$body|$checksum"
    }

    /**
     * Converts a single resource code (e.g. 'F', 'W', 'M') into a 12-bit needs bitfield.
     */
    fun resourceCodeToBitfield(resourceCode: String): Long {
        return when (resourceCode.trim().uppercase()) {
            "F" -> 1L shl 0  // Food
            "W" -> 1L shl 1  // Water
            "M" -> 1L shl 2  // Medical Kits
            "T" -> 1L shl 3  // Tents
            "B" -> 1L shl 4  // Blankets
            "H" -> 1L shl 5  // Hygiene Kits
            "X" -> 1L shl 6  // Rescue Team
            "V" -> 1L shl 7  // Evacuation Transport
            "P" -> 1L shl 8  // Power / Generators
            "I" -> 1L shl 9  // Infant Kits
            "D" -> 1L shl 10 // Medical Team / Doctor
            "E" -> 1L shl 11 // Heavy Equipment
            else -> 1L shl 0
        }
    }

    /**
     * Encodes FieldReport to canonical N frame with PACK10 GPS coordinates and exact requested quantity.
     */
    fun encodeReport(
        report: FieldReport,
        seq: String
    ): String {
        return encodeNeed(report, seq)
    }

    fun encodeNeed(
        report: FieldReport,
        seq: String
    ): String {
        val organization = report.organizationId
            .trim()
            .uppercase()
            .replace("|", "")
            .ifBlank { "NGO01" }

        val location = if (report.latitude != null && report.longitude != null && (report.latitude != 0.0 || report.longitude != 0.0)) {
            Pack10.encode(report.latitude, report.longitude)
        } else {
            locationCode(report.locationCode)
        }

        val resource = resourceCode(report.resourceCode)
        val urgency = urgencyCode(report.urgencyCode)

        val body = listOf(
            "N",
            seq,
            organization,
            location,
            resource,
            report.quantity.toString(),
            urgency
        ).joinToString("|")

        val checksum = xorChecksum(body)
        return "$body|$checksum"
    }
}
```

---

<a id="file-android-app-src-main-java-org-humanitarian-fieldapp-sms-smsdecoder-kt"></a>
## File: `android/app/src/main/java/org/humanitarian/fieldapp/sms/SmsDecoder.kt`

```kotlin
package org.humanitarian.fieldapp.sms

import org.json.JSONObject
import java.util.LinkedHashMap

object SmsDecoder {

    data class DecodedSms(
        val valid: Boolean,
        val typeLabel: String,
        val typeCode: String,
        val message: String,                       // Human-readable sentence
        val fields: LinkedHashMap<String, String>,
        val json: String,
        val checksumValid: Boolean,
        val error: String
    )

    // Taxonomy mappings
    private val situationNames = mapOf(
        '0' to "General Emergency",
        '1' to "Flood / Rising Water",
        '2' to "Earthquake / Debris",
        '3' to "Fire / Explosion",
        '4' to "Landslide / Mudslide",
        '5' to "Building Collapse",
        '6' to "Cyclone / Hurricane",
        '7' to "Hazardous / Chemical",
        '8' to "Heatwave / Drought"
    )

    private val headcountNames = mapOf(
        '0' to "1 person",
        '1' to "2-3 people",
        '2' to "4-5 people",
        '3' to "6-10 people",
        '4' to "11-20 people",
        '5' to "21-50 people",
        '6' to "50+ people"
    )

    private val injuryNames = mapOf(
        '0' to "No injuries",
        '1' to "Minor injuries",
        '2' to "Moderate trauma / fractures",
        '3' to "Severe trauma / bleeding",
        '4' to "Critical / Fatalities"
    )

    private val mobilityNames = mapOf(
        '0' to "Fully mobile",
        '1' to "Limited mobility",
        '2' to "Trapped in debris",
        '3' to "Waterbound / rooftop",
        '4' to "Bedridden"
    )

    private val locationNames = mapOf(
        "RA" to "Region A", "RB" to "Region B", "RC" to "Region C",
        "D1" to "District North", "D2" to "District South"
    )
    private val resourceNames = mapOf(
        "F" to "food_kits", "W" to "water_kits", "M" to "medical_kits",
        "T" to "tents", "B" to "blankets", "H" to "hygiene_kits",
        "X" to "rescue_teams", "V" to "evac_transport", "P" to "power_generators",
        "I" to "infant_kits", "D" to "medical_teams", "E" to "heavy_equipment", "U" to "unknown"
    )
    private val urgencyNames = mapOf("L" to "low", "M" to "medium", "H" to "high", "C" to "critical")
    private val statusNames = mapOf(
        "0" to "assigned", "1" to "dispatched", "2" to "in_transit",
        "3" to "delivered", "4" to "blocked", "5" to "cancelled"
    )
    private val availabilityNames = mapOf("A" to "available", "L" to "limited", "U" to "unavailable")

    fun decode(raw: String): DecodedSms {
        val message = raw.trim()
        if (message.isEmpty()) return errorResult("Empty message")
        val parts = message.split("|")
        if (parts.size < 2) return errorResult("Invalid format: too few fields")
        return when (parts[0].trim().uppercase()) {
            "Q" -> decodeQ(parts, message)
            "C" -> decodeConfirmation(parts, message)
            "N" -> decodeNeed(parts, message)
            "R" -> decodeResource(parts, message)
            "A" -> decodeAllocation(parts, message)
            "S" -> decodeStatus(parts, message)
            "M" -> decodeMarker(parts, message)
            "X" -> decodeCancel(parts, message)
            else -> errorResult("Unknown message type: ${parts[0]}")
        }
    }

    private fun checksumOk(fullMessage: String, providedCrc: String): Boolean {
        val body = fullMessage.substringBeforeLast("|")
        return xorChecksum(body).equals(providedCrc.trim(), ignoreCase = true)
    }

    private fun pretty(json: JSONObject): String = json.toString(2)

    private fun errorResult(msg: String): DecodedSms {
        return DecodedSms(false, "Error", "", "", LinkedHashMap(), "", false, msg)
    }

    /**
     * Decodes Q Citizen / Emergency SOS Frame:
     * Q|SEQ|UID|PAYLOAD_10|PACK10_GPS|CRC
     */
    private fun decodeQ(parts: List<String>, full: String): DecodedSms {
        if (parts.size < 6) return errorResult("Invalid Q frame (expected Q|SEQ|UID|PAYLOAD|GEO|CRC)")

        val seq = parts[1].trim()
        val uid = parts[2].trim()
        val payloadStr = parts[3].trim().uppercase()
        val geoStr = parts[4].trim().uppercase()
        val crc = parts[5].trim()
        val crcOk = checksumOk(full, crc)

        var lat = 0.0
        var lon = 0.0
        var geoFormatted = geoStr
        try {
            if (geoStr.length >= 10) {
                val geo = Pack10.decode(geoStr)
                lat = geo.latitude
                lon = geo.longitude
                geoFormatted = "Lat: ${"%.5f".format(lat)}, Lon: ${"%.5f".format(lon)}"
            }
        } catch (_: Exception) {}

        var sitName = "Emergency"
        var hcName = "1 person"
        var injName = "Uninjured"
        var mobName = "Mobile"
        var urgName = "Medium"
        val requestedResources = mutableListOf<String>()

        if (payloadStr.length >= 10) {
            sitName = situationNames[payloadStr[1]] ?: "General Emergency"
            hcName = headcountNames[payloadStr[2]] ?: "1 person"
            injName = injuryNames[payloadStr[3]] ?: "No injuries"
            mobName = mobilityNames[payloadStr[4]] ?: "Fully mobile"
            urgName = urgencyNames[payloadStr[5].toString()]?.replaceFirstChar { it.uppercase() } ?: "Medium"

            try {
                val needsInt = Base36.decode(payloadStr.substring(6, 9))
                if ((needsInt and (1L shl 0)) > 0) requestedResources.add("Food")
                if ((needsInt and (1L shl 1)) > 0) requestedResources.add("Water")
                if ((needsInt and (1L shl 2)) > 0) requestedResources.add("Medical Kits")
                if ((needsInt and (1L shl 3)) > 0) requestedResources.add("Tents")
                if ((needsInt and (1L shl 4)) > 0) requestedResources.add("Blankets")
                if ((needsInt and (1L shl 5)) > 0) requestedResources.add("Hygiene Kits")
                if ((needsInt and (1L shl 6)) > 0) requestedResources.add("Rescue Team")
                if ((needsInt and (1L shl 7)) > 0) requestedResources.add("Evac Transport")
                if ((needsInt and (1L shl 8)) > 0) requestedResources.add("Generators")
                if ((needsInt and (1L shl 9)) > 0) requestedResources.add("Infant Kits")
                if ((needsInt and (1L shl 10)) > 0) requestedResources.add("Doctors")
                if ((needsInt and (1L shl 11)) > 0) requestedResources.add("Heavy Equipment")
            } catch (_: Exception) {}
        }

        val resSummary = if (requestedResources.isNotEmpty()) requestedResources.joinToString(", ") else "General Aid"
        val humanSentence = "🚨 [SOS Target $uid]: $sitName involving $hcName. Status: $injName, $mobName. Urgency: $urgName. Needs: $resSummary. Location: ($lat, $lon)."

        val fields = LinkedHashMap<String, String>().apply {
            put("Type", "Emergency SOS (Q)")
            put("Sequence", seq)
            put("Target UID", uid)
            put("Coordinates", geoFormatted)
            put("Situation", sitName)
            put("Population", hcName)
            put("Casualties", injName)
            put("Mobility", mobName)
            put("Urgency", urgName)
            put("Needed Supplies", resSummary)
            put("Checksum", if (crcOk) "$crc (VALID)" else "$crc (INVALID)")
        }

        val json = JSONObject().apply {
            put("type", "individual_request")
            put("seq", seq)
            put("uid", uid)
            put("situation", sitName)
            put("headcount", hcName)
            put("injury", injName)
            put("mobility", mobName)
            put("urgency", urgName)
            put("needed_resources", requestedResources)
            put("latitude", lat)
            put("longitude", lon)
            put("pack10", geoStr)
            put("checksum_valid", crcOk)
        }

        return DecodedSms(true, "Emergency SOS", "Q", humanSentence, fields, pretty(json), crcOk, "")
    }

    /**
     * Decodes C Confirmation ACK frame:
     * C|SEQ|UID|PLAN_ID|STATE|ETA|CRC or C|SEQ|REF|RESULT|CRC
     */
    private fun decodeConfirmation(parts: List<String>, full: String): DecodedSms {
        val seq = parts.getOrNull(1) ?: "001"
        val uid = if (parts.size >= 7) parts[2] else "CIT00"
        val planId = if (parts.size >= 7) parts[3] else (parts.getOrNull(2) ?: "PLAN")
        val state = if (parts.size >= 7) parts[4] else (parts.getOrNull(3) ?: "OK")
        val eta = if (parts.size >= 7) parts[5] else "0"
        val crc = parts.lastOrNull() ?: ""
        val crcOk = checksumOk(full, crc)

        val humanSentence = "✅ Dispatch Plan '$planId' committed for $uid. Status: ${state.uppercase()}, Estimated arrival: $eta hours."

        val fields = LinkedHashMap<String, String>().apply {
            put("Type", "Confirmation ACK (C)")
            put("Sequence", seq)
            put("Recipient UID", uid)
            put("Plan ID", planId)
            put("Commit Status", state.uppercase())
            put("ETA (Hours)", eta)
            put("Checksum", if (crcOk) "$crc (VALID)" else "$crc (INVALID)")
        }

        val json = JSONObject().apply {
            put("type", "confirmation")
            put("seq", seq)
            put("uid", uid)
            put("plan_id", planId)
            put("status", state)
            put("eta_hours", eta.toDoubleOrNull() ?: 0.0)
            put("checksum_valid", crcOk)
        }

        return DecodedSms(true, "Confirmation ACK", "C", humanSentence, fields, pretty(json), crcOk, "")
    }

    private fun decodeNeed(parts: List<String>, full: String): DecodedSms {
        if (parts.size < 8) return errorResult("Invalid Need format (expected N|SEQ|ORG|LOC|RES|QTY|URG|CRC)")
        val seq = parts[1].trim()
        val org = parts[2].trim()
        val loc = parts[3].trim()
        val res = parts[4].trim()
        val qty = parts[5].trim().toIntOrNull() ?: 0
        val urg = parts[6].trim()
        val crc = parts[7].trim()
        val crcOk = checksumOk(full, crc)

        var locDisplay = locationNames[loc] ?: loc
        if (loc.length == 10 && !locationNames.containsKey(loc)) {
            try {
                val geo = Pack10.decode(loc)
                locDisplay = "Coords (${geo.latitude}, ${geo.longitude})"
            } catch (_: Exception) {}
        }

        val resDisplay = resourceNames[res] ?: res
        val urgDisplay = urgencyNames[urg]?.replaceFirstChar { it.uppercase() } ?: urg

        val humanSentence = "Organization $org reports an urgent need of $qty $resDisplay at $locDisplay (Urgency: $urgDisplay)."

        val fields = LinkedHashMap<String, String>().apply {
            put("Type", "Need Request (N)")
            put("Sequence", seq)
            put("Organization", org)
            put("Location", locDisplay)
            put("Resource", resDisplay)
            put("Quantity", qty.toString())
            put("Urgency", urgDisplay)
            put("Checksum", if (crcOk) "$crc (VALID)" else "$crc (INVALID)")
        }

        val json = JSONObject().apply {
            put("type", "need")
            put("seq", seq)
            put("organization", org)
            put("location", loc)
            put("resource", resDisplay)
            put("quantity", qty)
            put("urgency", urgDisplay.lowercase())
            put("checksum_valid", crcOk)
        }

        return DecodedSms(true, "Need Request", "N", humanSentence, fields, pretty(json), crcOk, "")
    }

    private fun decodeResource(parts: List<String>, full: String): DecodedSms {
        if (parts.size < 8) return errorResult("Invalid Resource format")
        val seq = parts[1].trim()
        val org = parts[2].trim()
        val loc = parts[3].trim()
        val res = parts[4].trim()
        val qty = parts[5].trim().toIntOrNull() ?: 0
        val avail = parts[6].trim()
        val crc = parts[7].trim()
        val crcOk = checksumOk(full, crc)

        val humanSentence = "Provider $org offers $qty ${resourceNames[res] ?: res} at ${locationNames[loc] ?: loc} (Status: ${availabilityNames[avail] ?: avail})."

        val fields = LinkedHashMap<String, String>().apply {
            put("Type", "Resource Availability (R)")
            put("Sequence", seq)
            put("Provider", org)
            put("Location", locationNames[loc] ?: loc)
            put("Resource", resourceNames[res] ?: res)
            put("Quantity", qty.toString())
            put("Status", availabilityNames[avail] ?: avail)
            put("Checksum", if (crcOk) "$crc (VALID)" else "$crc (INVALID)")
        }

        val json = JSONObject().apply {
            put("type", "resource")
            put("seq", seq)
            put("provider", org)
            put("quantity", qty)
            put("checksum_valid", crcOk)
        }

        return DecodedSms(true, "Resource Availability", "R", humanSentence, fields, pretty(json), crcOk, "")
    }

    private fun decodeAllocation(parts: List<String>, full: String): DecodedSms {
        if (parts.size < 9) return errorResult("Invalid Allocation format")
        val seq = parts[1].trim()
        val plan = parts[2].trim()
        val org = parts[3].trim()
        val res = parts[4].trim()
        val qty = parts[5].trim()
        val dest = parts[6].trim()
        val eta = parts[7].trim()
        val crc = parts[8].trim()
        val crcOk = checksumOk(full, crc)

        val humanSentence = "Plan $plan: $org allocated $qty ${resourceNames[res] ?: res} to ${locationNames[dest] ?: dest} (ETA: ${eta}h)."

        val fields = LinkedHashMap<String, String>().apply {
            put("Type", "Allocation Assignment (A)")
            put("Sequence", seq)
            put("Plan ID", plan)
            put("Assigned Org", org)
            put("Supplies", "$qty ${resourceNames[res] ?: res}")
            put("Destination", locationNames[dest] ?: dest)
            put("ETA", "${eta}h")
            put("Checksum", if (crcOk) "$crc (VALID)" else "$crc (INVALID)")
        }

        val json = JSONObject().apply {
            put("type", "allocation")
            put("plan_id", plan)
            put("organization", org)
            put("quantity", qty.toIntOrNull() ?: 0)
            put("eta_hours", eta.toDoubleOrNull() ?: 1.0)
            put("checksum_valid", crcOk)
        }

        return DecodedSms(true, "Allocation", "A", humanSentence, fields, pretty(json), crcOk, "")
    }

    private fun decodeStatus(parts: List<String>, full: String): DecodedSms {
        val seq = parts[1].trim()
        val plan = parts[2].trim()
        val statusCode = parts[3].trim()
        val crc = parts.getOrNull(4)?.trim() ?: ""
        val crcOk = if (crc.isNotBlank()) checksumOk(full, crc) else true
        val statusText = statusNames[statusCode] ?: "unknown"

        val humanSentence = "Delivery status for plan $plan updated to ${statusText.uppercase()}."

        val fields = LinkedHashMap<String, String>().apply {
            put("Type", "Status Update (S)")
            put("Sequence", seq)
            put("Plan ID", plan)
            put("Status", statusText.replaceFirstChar { it.uppercase() })
            put("Checksum", if (crcOk) "$crc (VALID)" else "$crc (INVALID)")
        }

        val json = JSONObject().apply {
            put("type", "status")
            put("plan_id", plan)
            put("status", statusText)
            put("checksum_valid", crcOk)
        }

        return DecodedSms(true, "Status Update", "S", humanSentence, fields, pretty(json), crcOk, "")
    }

    private fun decodeMarker(parts: List<String>, full: String): DecodedSms {
        val seq = parts.getOrNull(1) ?: "001"
        val markerId = parts.getOrNull(2) ?: "M01"
        val mType = parts.getOrNull(3) ?: "CR"
        val loc = parts.getOrNull(4) ?: "RA"
        val crc = parts.lastOrNull() ?: ""
        val crcOk = checksumOk(full, crc)

        val humanSentence = "Map marker $markerId registered at $loc."

        val fields = LinkedHashMap<String, String>().apply {
            put("Type", "Map Marker (M)")
            put("Marker ID", markerId)
            put("Marker Type", mType)
            put("Location", loc)
            put("Checksum", if (crcOk) "$crc (VALID)" else "$crc (INVALID)")
        }

        val json = JSONObject().apply {
            put("type", "marker")
            put("marker_id", markerId)
            put("checksum_valid", crcOk)
        }

        return DecodedSms(true, "Map Marker", "M", humanSentence, fields, pretty(json), crcOk, "")
    }

    private fun decodeCancel(parts: List<String>, full: String): DecodedSms {
        val seq = parts.getOrNull(1) ?: "001"
        val ref = parts.getOrNull(2) ?: "REF"
        val reason = parts.getOrNull(3) ?: "Cancelled by dispatcher"
        val crc = parts.lastOrNull() ?: ""
        val crcOk = checksumOk(full, crc)

        val humanSentence = "Request/Plan $ref was CANCELLED. Reason: $reason."

        val fields = LinkedHashMap<String, String>().apply {
            put("Type", "Cancel Request (X)")
            put("Reference", ref)
            put("Reason", reason)
            put("Checksum", if (crcOk) "$crc (VALID)" else "$crc (INVALID)")
        }

        val json = JSONObject().apply {
            put("type", "cancel")
            put("reference", ref)
            put("reason", reason)
            put("checksum_valid", crcOk)
        }

        return DecodedSms(true, "Cancel Request", "X", humanSentence, fields, pretty(json), crcOk, "")
    }
}
```

---

<a id="file-android-app-src-main-java-org-humanitarian-fieldapp-sms-directsmssender-kt"></a>
## File: `android/app/src/main/java/org/humanitarian/fieldapp/sms/DirectSmsSender.kt`

```kotlin
package org.humanitarian.fieldapp.sms

import android.content.Context
import android.os.Build
import android.telephony.SmsManager
import android.util.Log

object DirectSmsSender {

    private const val TAG = "DirectSmsSender"

    /**
     * Sends an SMS silently in the background directly via Cellular SIM.
     * Does NOT open the external SMS messenger app.
     */
    fun sendDirectSms(context: Context, phoneNumber: String, message: String): Boolean {
        return try {
            val smsManager: SmsManager = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
                context.getSystemService(SmsManager::class.java) ?: SmsManager.getDefault()
            } else {
                @Suppress("DEPRECATION")
                SmsManager.getDefault()
            }

            if (message.length > 160) {
                val parts = smsManager.divideMessage(message)
                smsManager.sendMultipartTextMessage(phoneNumber, null, parts, null, null)
            } else {
                smsManager.sendTextMessage(phoneNumber, null, message, null, null)
            }

            Log.i(TAG, "Successfully dispatched direct background SMS to $phoneNumber: $message")
            true
        } catch (e: Exception) {
            Log.e(TAG, "Failed to send background SMS to $phoneNumber", e)
            false
        }
    }
}
```

---

<a id="file-android-app-src-main-java-org-humanitarian-fieldapp-network-apiclient-kt"></a>
## File: `android/app/src/main/java/org/humanitarian/fieldapp/network/ApiClient.kt`

```kotlin
package org.humanitarian.fieldapp.network

import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import org.humanitarian.fieldapp.models.FieldReport
import org.humanitarian.fieldapp.models.OrgRequest
import org.json.JSONObject
import java.net.HttpURLConnection
import java.net.URL

sealed class ApiResult<out T> {
    data class Success<T>(val data: T) : ApiResult<T>()
    data class Error(val message: String) : ApiResult<Nothing>()
}

object ApiClient {

    // ═══════════════════════════════════════════════════════
    // CHANNEL 1: NORMAL INTERNET API
    // Used when internet is available (Field Report direct send, M10 sync)
    // ═══════════════════════════════════════════════════════
    private const val INTERNET_API_URL = "http://10.142.1.84:8000"

    // ═══════════════════════════════════════════════════════
    // CHANNEL 2: SMS GATEWAY (SIMULATED)
    // Used for SMS fallback: sending SMS payloads + polling inbox
    // Can be a DIFFERENT IP/port to simulate a separate telecom gateway
    // ═══════════════════════════════════════════════════════
    private const val SMS_GATEWAY_URL = "http://10.142.1.84:8000"

    // ───────────── INTERNET CHANNEL ─────────────

    suspend fun postNeed(report: FieldReport): ApiResult<String> {
        return withContext(Dispatchers.IO) {
            var connection: HttpURLConnection? = null
            try {
                val url = URL("$INTERNET_API_URL/api/v1/needs")
                connection = url.openConnection() as HttpURLConnection
                connection.requestMethod = "POST"
                connection.connectTimeout = 8000
                connection.readTimeout = 8000
                connection.setRequestProperty("Content-Type", "application/json")
                connection.doOutput = true

                val payload = JSONObject()
                    .put("type", "need")
                    .put("organization_id", report.organizationId)
                    .put("location_code", report.locationCode)
                    .put("location_name", locationName(report.locationCode))
                    .put("location", locationName(report.locationCode))
                    .put("resource", resourceName(report.resourceCode))
                    .put("resource_code", report.resourceCode)
                    .put("quantity", report.quantity)
                    .put("urgency", urgencyName(report.urgencyCode))
                    .put("urgency_code", report.urgencyCode)
                    .put("notes", report.notes)
                    .put("source", "android")
                    .put("latitude", report.latitude ?: 0.0)
                    .put("longitude", report.longitude ?: 0.0)

                connection.outputStream.use { outputStream ->
                    outputStream.write(payload.toString().toByteArray())
                    outputStream.flush()
                }

                val responseCode = connection.responseCode
                val responseBody = if (responseCode in 200..299) {
                    connection.inputStream.bufferedReader().use { it.readText() }
                } else {
                    connection.errorStream?.bufferedReader()?.use { it.readText() } ?: ""
                }

                if (responseCode in 200..299) ApiResult.Success(responseBody.ifBlank { "HTTP $responseCode" })
                else ApiResult.Error("HTTP $responseCode: ${responseBody.take(200)}")
            } catch (exception: Exception) {
                ApiResult.Error(exception.message ?: "Network request failed")
            } finally {
                connection?.disconnect()
            }
        }
    }

    // ───────────── SMS GATEWAY CHANNEL ─────────────

    suspend fun postSmsWebhook(smsPayload: String): ApiResult<String> {
        return withContext(Dispatchers.IO) {
            var connection: HttpURLConnection? = null
            try {
                val url = URL("$SMS_GATEWAY_URL/api/v1/sms/webhook")
                connection = url.openConnection() as HttpURLConnection
                connection.requestMethod = "POST"
                connection.connectTimeout = 8000
                connection.readTimeout = 8000
                connection.setRequestProperty("Content-Type", "application/json")
                connection.doOutput = true

                val payload = JSONObject().put("sms", smsPayload)

                connection.outputStream.use { outputStream ->
                    outputStream.write(payload.toString().toByteArray())
                    outputStream.flush()
                }

                val responseCode = connection.responseCode
                val responseBody = if (responseCode in 200..299) {
                    connection.inputStream.bufferedReader().use { it.readText() }
                } else {
                    connection.errorStream?.bufferedReader()?.use { it.readText() } ?: ""
                }

                if (responseCode in 200..299) ApiResult.Success(responseBody)
                else ApiResult.Error("HTTP $responseCode: ${responseBody.take(200)}")
            } catch (exception: Exception) {
                ApiResult.Error(exception.message ?: "SMS gateway unreachable")
            } finally {
                connection?.disconnect()
            }
        }
    }

    suspend fun getSmsInbox(): ApiResult<List<String>> {
        return withContext(Dispatchers.IO) {
            var connection: HttpURLConnection? = null
            try {
                val url = URL("$SMS_GATEWAY_URL/api/v1/sms/inbox")
                connection = url.openConnection() as HttpURLConnection
                connection.requestMethod = "GET"
                connection.connectTimeout = 5000
                connection.readTimeout = 5000

                val responseCode = connection.responseCode
                if (responseCode in 200..299) {
                    val body = connection.inputStream.bufferedReader().use { it.readText() }
                    val json = JSONObject(body)
                    val messagesArray = json.getJSONArray("messages")
                    val messages = mutableListOf<String>()
                    for (i in 0 until messagesArray.length()) {
                        messages.add(messagesArray.getString(i))
                    }
                    ApiResult.Success(messages)
                } else {
                    ApiResult.Error("HTTP $responseCode")
                }
            } catch (e: Exception) {
                ApiResult.Error(e.message ?: "Inbox fetch failed")
            } finally {
                connection?.disconnect()
            }
        }
    }

    suspend fun clearInbox(): ApiResult<String> {
        return withContext(Dispatchers.IO) {
            var connection: HttpURLConnection? = null
            try {
                val url = URL("$SMS_GATEWAY_URL/api/v1/sms/clear")
                connection = url.openConnection() as HttpURLConnection
                connection.requestMethod = "POST"
                connection.connectTimeout = 5000
                connection.readTimeout = 5000
                connection.responseCode
                ApiResult.Success("cleared")
            } catch (e: Exception) {
                ApiResult.Error(e.message ?: "Clear failed")
            } finally {
                connection?.disconnect()
            }
        }
    }

    // ───────────── REAL-TIME LOCATION + STATUS POLLING ─────────────

    // Send live GPS to backend every 10 seconds
    suspend fun postLocationUpdate(organizationId: String, lat: Double, lng: Double): ApiResult<String> {
        return withContext(Dispatchers.IO) {
            var connection: HttpURLConnection? = null
            try {
                val url = URL("$INTERNET_API_URL/api/v1/location/update")
                connection = url.openConnection() as HttpURLConnection
                connection.requestMethod = "POST"
                connection.connectTimeout = 5000
                connection.readTimeout = 5000
                connection.setRequestProperty("Content-Type", "application/json")
                connection.doOutput = true

                val payload = JSONObject()
                    .put("organization_id", organizationId)
                    .put("latitude", lat)
                    .put("longitude", lng)

                connection.outputStream.use { it.write(payload.toString().toByteArray()); it.flush() }

                val code = connection.responseCode
                if (code in 200..299) ApiResult.Success("ok")
                else ApiResult.Error("HTTP $code")
            } catch (e: Exception) {
                ApiResult.Error(e.message ?: "Location update failed")
            } finally {
                connection?.disconnect()
            }
        }
    }

    // Poll approval status of this org's requests
    suspend fun getRequestsByOrg(organizationId: String): ApiResult<List<OrgRequest>> {
        return withContext(Dispatchers.IO) {
            var connection: HttpURLConnection? = null
            try {
                val url = URL("$INTERNET_API_URL/api/v1/requests/by-org/$organizationId")
                connection = url.openConnection() as HttpURLConnection
                connection.requestMethod = "GET"
                connection.connectTimeout = 5000
                connection.readTimeout = 5000

                val code = connection.responseCode
                if (code in 200..299) {
                    val body = connection.inputStream.bufferedReader().use { it.readText() }
                    val arr = JSONObject(body).getJSONArray("requests")
                    val list = mutableListOf<OrgRequest>()
                    for (i in 0 until arr.length()) {
                        val o = arr.getJSONObject(i)
                        list.add(
                            OrgRequest(
                                id = o.optString("id", ""),
                                type = o.optString("type", ""),
                                resource = o.optString("resource", ""),
                                quantity = o.optInt("quantity", 0),
                                status = o.optString("status", "pending"),
                                latitude = if (o.isNull("latitude")) null else o.optDouble("latitude"),
                                longitude = if (o.isNull("longitude")) null else o.optDouble("longitude"),
                                createdAt = o.optString("created_at", "")
                            )
                        )
                    }
                    ApiResult.Success(list)
                } else {
                    ApiResult.Error("HTTP $code")
                }
            } catch (e: Exception) {
                ApiResult.Error(e.message ?: "Status fetch failed")
            } finally {
                connection?.disconnect()
            }
        }
    }

    // ───────────── MAPPINGS ─────────────

    private fun resourceName(code: String): String {
        return when (code) {
            "F" -> "food_kits"; "W" -> "water_kits"; "M" -> "medical_kits"
            "T" -> "tents"; "B" -> "blankets"; "H" -> "hygiene_kits"
            "D" -> "medical_teams"; else -> "unknown"
        }
    }

    private fun urgencyName(code: String): String {
        return when (code) {
            "L" -> "low"; "M" -> "medium"; "H" -> "high"; "C" -> "critical"; else -> "unknown"
        }
    }

    private fun locationName(code: String): String {
        return when (code) {
            "RA" -> "Region A"; "RB" -> "Region B"; "RC" -> "Region C"
            "D1" -> "District North"; "D2" -> "District South"; else -> code
        }
    }
}
```

---

<a id="file-android-app-src-main-java-org-humanitarian-fieldapp-offline-offlinequeue-kt"></a>
## File: `android/app/src/main/java/org/humanitarian/fieldapp/offline/OfflineQueue.kt`

```kotlin
package org.humanitarian.fieldapp.offline

import android.content.Context
import android.content.SharedPreferences
import org.humanitarian.fieldapp.models.FieldReport
import org.json.JSONArray
import org.json.JSONObject

data class QueuedReport(
    val report: FieldReport,
    val smsPayload: String
)

object OfflineQueue {
    private const val PREFS_NAME = "pact_offline_queue"
    private const val KEY_REPORTS = "pending_reports"

    private fun getPrefs(context: Context): SharedPreferences {
        return context.getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE)
    }

    fun addReport(context: Context, report: FieldReport, smsPayload: String) {
        val prefs = getPrefs(context)
        val jsonArray = JSONArray(prefs.getString(KEY_REPORTS, "[]"))

        val jsonObj = JSONObject()
            .put("organizationId", report.organizationId)
            .put("locationCode", report.locationCode)
            .put("resourceCode", report.resourceCode)
            .put("quantity", report.quantity)
            .put("urgencyCode", report.urgencyCode)
            .put("notes", report.notes)
            .put("smsPayload", smsPayload)

        jsonArray.put(jsonObj)
        prefs.edit().putString(KEY_REPORTS, jsonArray.toString()).apply()
    }

    fun getQueuedReports(context: Context): List<QueuedReport> {
        val prefs = getPrefs(context)
        val jsonArray = JSONArray(prefs.getString(KEY_REPORTS, "[]"))
        val reports = mutableListOf<QueuedReport>()

        for (i in 0 until jsonArray.length()) {
            val obj = jsonArray.getJSONObject(i)
            val report = FieldReport(
                organizationId = obj.getString("organizationId"),
                locationCode = obj.getString("locationCode"),
                resourceCode = obj.getString("resourceCode"),
                quantity = obj.getInt("quantity"),
                urgencyCode = obj.getString("urgencyCode"),
                notes = obj.optString("notes", "")
            )
            val payload = obj.optString("smsPayload", "")
            reports.add(QueuedReport(report, payload))
        }
        return reports
    }

    // Rewrites the queue with only the given reports (used after partial sync)
    fun replaceQueue(context: Context, reports: List<QueuedReport>) {
        val prefs = getPrefs(context)
        val jsonArray = JSONArray()
        for (item in reports) {
            val jsonObj = JSONObject()
                .put("organizationId", item.report.organizationId)
                .put("locationCode", item.report.locationCode)
                .put("resourceCode", item.report.resourceCode)
                .put("quantity", item.report.quantity)
                .put("urgencyCode", item.report.urgencyCode)
                .put("notes", item.report.notes)
                .put("smsPayload", item.smsPayload)
            jsonArray.put(jsonObj)
        }
        prefs.edit().putString(KEY_REPORTS, jsonArray.toString()).apply()
    }

    fun clearQueue(context: Context) {
        getPrefs(context).edit().remove(KEY_REPORTS).apply()
    }

    fun getQueueSize(context: Context): Int {
        return getQueuedReports(context).size
    }
}
```

---

<a id="file-android-app-src-main-java-org-humanitarian-fieldapp-ui-fieldreportscreen-kt"></a>
## File: `android/app/src/main/java/org/humanitarian/fieldapp/ui/FieldReportScreen.kt`

```kotlin
package org.humanitarian.fieldapp.ui

import android.Manifest
import android.content.pm.PackageManager
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.DropdownMenu
import androidx.compose.material3.DropdownMenuItem
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.RadioButton
import androidx.compose.material3.RadioButtonDefaults
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.TopAppBarDefaults
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.unit.dp
import androidx.core.app.ActivityCompat
import com.google.android.gms.location.LocationServices
import com.google.android.gms.location.Priority
import kotlinx.coroutines.launch
import org.json.JSONObject
import org.humanitarian.fieldapp.models.FieldReport
import org.humanitarian.fieldapp.network.ApiClient
import org.humanitarian.fieldapp.network.ApiResult
import org.humanitarian.fieldapp.offline.OfflineQueue
import org.humanitarian.fieldapp.offline.SubmittedReports
import org.humanitarian.fieldapp.sms.SmsEncoder
import org.humanitarian.fieldapp.ui.theme.PactAccent
import org.humanitarian.fieldapp.ui.theme.PactBackground
import org.humanitarian.fieldapp.ui.theme.PactOnPrimary
import org.humanitarian.fieldapp.ui.theme.PactPrimary
import org.humanitarian.fieldapp.ui.theme.PactSurface
import org.humanitarian.fieldapp.ui.theme.PactTextPrimary
import org.humanitarian.fieldapp.ui.theme.PactTextSecondary

private data class CodeOption(val code: String, val label: String)

private val locationOptions = listOf(
    CodeOption("RA", "Region A"), CodeOption("RB", "Region B"), CodeOption("RC", "Region C"),
    CodeOption("D1", "District North"), CodeOption("D2", "District South")
)
private val resourceOptions = listOf(
    CodeOption("F", "Food kits"), CodeOption("W", "Water kits"), CodeOption("M", "Medical kits"),
    CodeOption("T", "Tents"), CodeOption("B", "Blankets"), CodeOption("H", "Hygiene kits"),
    CodeOption("D", "Medical teams"), CodeOption("U", "Unknown")
)
private val urgencyOptions = listOf(
    CodeOption("L", "Low"), CodeOption("M", "Medium"), CodeOption("H", "High"), CodeOption("C", "Critical")
)

private fun submitReport(report: FieldReport): Boolean {
    return report.organizationId.isNotBlank() &&
        locationOptions.any { it.code == report.locationCode } &&
        resourceOptions.any { it.code == report.resourceCode } &&
        report.quantity > 0 &&
        urgencyOptions.any { it.code == report.urgencyCode }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun FieldReportScreen(onBack: () -> Unit, onReturnHome: () -> Unit) {
    var organizationId by rememberSaveable { mutableStateOf("NGO01") }
    var locationCode by rememberSaveable { mutableStateOf("RA") }
    var resourceCode by rememberSaveable { mutableStateOf("F") }
    var quantity by rememberSaveable { mutableStateOf("") }
    var urgencyCode by rememberSaveable { mutableStateOf("H") }
    var notes by rememberSaveable { mutableStateOf("") }

    var submittedReport by remember { mutableStateOf<FieldReport?>(null) }
    var showError by rememberSaveable { mutableStateOf(false) }
    var submissionState by remember { mutableStateOf("idle") }
    var apiMessage by remember { mutableStateOf("") }
    var smsPayload by remember { mutableStateOf("") }

    val coroutineScope = rememberCoroutineScope()
    val context = LocalContext.current
    
    // GPS Location State
    var currentLat by remember { mutableStateOf(0.0) }
    var currentLng by remember { mutableStateOf(0.0) }
    val fusedLocationClient = remember { LocationServices.getFusedLocationProviderClient(context) }

    // Fetch GPS on load
    LaunchedEffect(Unit) {
        if (ActivityCompat.checkSelfPermission(context, Manifest.permission.ACCESS_FINE_LOCATION) == PackageManager.PERMISSION_GRANTED) {
            fusedLocationClient.getCurrentLocation(Priority.PRIORITY_HIGH_ACCURACY, null).addOnSuccessListener { location ->
                if (location != null) {
                    currentLat = location.latitude
                    currentLng = location.longitude
                }
            }
        }
    }

        val sendReport: (FieldReport) -> Unit = { report ->
        submittedReport = report
        showError = false
        submissionState = "submitting"
        apiMessage = ""

        coroutineScope.launch {
            // 1. Try normal internet API first
            val internetResult = ApiClient.postNeed(report)
            
            if (internetResult is ApiResult.Success) {
                submissionState = "success"
                apiMessage = "Sent directly via Internet API."
                smsPayload = ""
                val needId = try { 
                    JSONObject(internetResult.data).optString("need_id", "unknown") 
                } catch (e: Exception) { "unknown" }
                SubmittedReports.add(context, report, needId)
            } else {
                // 2. Internet failed -> Generate SMS Payload
                val seq = SmsEncoder.nextSequence(
                    context = context,
                    organizationId = report.organizationId
                )
                val generatedPayload = SmsEncoder.encodeReport(report = report, seq = seq)
                smsPayload = generatedPayload

                // 3. Auto-dispatch Direct Cellular SMS in Background via SIM
                val directSmsSent = org.humanitarian.fieldapp.sms.DirectSmsSender.sendDirectSms(
                    context = context,
                    phoneNumber = PACT_GATEWAY_PHONE,
                    message = generatedPayload
                )

                if (directSmsSent) {
                    submissionState = "success"
                    apiMessage = "Emergency SOS dispatched directly via Cellular SIM!"
                } else {
                    // Try HTTP gateway endpoint if direct SMS failed
                    val smsResult = ApiClient.postSmsWebhook(generatedPayload)
                    if (smsResult is ApiResult.Success) {
                        submissionState = "success"
                        apiMessage = "Sent via SMS Gateway HTTP Bridge!"
                    } else {
                        submissionState = "queued"
                        apiMessage = "Saved to offline queue."
                    }
                }
            }
        }
    }

    Scaffold(
        containerColor = PactBackground,
        topBar = {
            TopAppBar(
                title = { Text(text = "Field Report", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.SemiBold, color = PactTextPrimary) },
                navigationIcon = { TextButton(onClick = onBack) { Text(text = "Back", color = PactPrimary, fontWeight = FontWeight.SemiBold) } },
                colors = TopAppBarDefaults.topAppBarColors(containerColor = PactSurface, titleContentColor = PactTextPrimary, navigationIconContentColor = PactPrimary)
            )
        }
    ) { padding ->
        val report = submittedReport
        if (report != null) {
            FieldReportSubmittedContent(
                padding = padding, report = report, submissionState = submissionState, apiMessage = apiMessage, smsPayload = smsPayload,
                onCreateAnother = { submittedReport = null; showError = false; submissionState = "idle"; apiMessage = ""; smsPayload = "" },
                onReturnHome = onReturnHome
            )
        } else {
            Column(
                modifier = Modifier.fillMaxSize().padding(padding).verticalScroll(rememberScrollState()).padding(20.dp),
                verticalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                Surface(modifier = Modifier.fillMaxWidth(), shape = RoundedCornerShape(24.dp), color = PactSurface, border = BorderStroke(1.dp, PactAccent)) {
                    Column(modifier = Modifier.padding(20.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                        Text(text = "Need Report", style = MaterialTheme.typography.headlineSmall, fontWeight = FontWeight.SemiBold, color = PactTextPrimary)
                        Text(text = "Select location, resource, and urgency. GPS coordinates are automatically attached.", style = MaterialTheme.typography.bodyMedium, color = PactTextSecondary)
                    }
                }

                OutlinedTextField(value = organizationId, onValueChange = { organizationId = it.uppercase() }, label = { Text("Organization ID") }, singleLine = true, shape = RoundedCornerShape(16.dp), modifier = Modifier.fillMaxWidth())
                CodeDropdown(label = "Location", options = locationOptions, selectedCode = locationCode, onCodeSelected = { locationCode = it }, supportingText = "Select a predefined location code.")
                CodeDropdown(label = "Resource", options = resourceOptions, selectedCode = resourceCode, onCodeSelected = { resourceCode = it }, supportingText = "Select a resource type code.")
                UrgencyRadioGroup(selectedCode = urgencyCode, onCodeSelected = { urgencyCode = it })
                OutlinedTextField(value = quantity, onValueChange = { quantity = it.filter { c -> c.isDigit() } }, label = { Text("Quantity") }, singleLine = true, keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number), shape = RoundedCornerShape(16.dp), modifier = Modifier.fillMaxWidth())
                OutlinedTextField(value = notes, onValueChange = { notes = it }, label = { Text("Notes, optional") }, maxLines = 3, shape = RoundedCornerShape(16.dp), modifier = Modifier.fillMaxWidth())

                if (showError) Text(text = "Please fill all required fields.", color = PactPrimary, style = MaterialTheme.typography.bodyMedium, fontWeight = FontWeight.Medium)

                Button(
                    onClick = {
                        val reportCandidate = FieldReport(
                            organizationId = organizationId.trim().uppercase(), locationCode = locationCode.trim().uppercase(),
                            resourceCode = resourceCode.trim().uppercase(), quantity = quantity.trim().toIntOrNull() ?: 0,
                            urgencyCode = urgencyCode.trim().uppercase(), notes = notes.trim(),
                            latitude = currentLat, longitude = currentLng // ATTACHED GPS
                        )
                        if (submitReport(reportCandidate)) sendReport(reportCandidate) else showError = true
                    },
                    modifier = Modifier.fillMaxWidth().height(56.dp), shape = RoundedCornerShape(16.dp),
                    colors = ButtonDefaults.buttonColors(containerColor = PactPrimary, contentColor = PactOnPrimary)
                ) {
                    Text(text = "Submit Field Report", style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.SemiBold)
                }
            }
        }
    }
}

@Composable
private fun CodeDropdown(label: String, options: List<CodeOption>, selectedCode: String, onCodeSelected: (String) -> Unit, supportingText: String) {
    var expanded by remember { mutableStateOf(false) }
    val selectedOption = options.firstOrNull { it.code == selectedCode }
    val displayValue = selectedOption?.let { "${it.code} - ${it.label}" } ?: "Select"
    Box(modifier = Modifier.fillMaxWidth()) {
        Box(modifier = Modifier.fillMaxWidth().clickable { expanded = true }) {
            Surface(modifier = Modifier.fillMaxWidth(), shape = RoundedCornerShape(16.dp), color = PactBackground, border = BorderStroke(1.dp, PactAccent)) {
                Column(modifier = Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(4.dp)) {
                    Text(text = label, style = MaterialTheme.typography.labelLarge, color = PactTextSecondary)
                    Text(text = displayValue, style = MaterialTheme.typography.bodyLarge, fontWeight = FontWeight.Medium, color = PactTextPrimary)
                    Text(text = supportingText, style = MaterialTheme.typography.bodySmall, color = PactTextSecondary)
                }
            }
        }
        DropdownMenu(expanded = expanded, onDismissRequest = { expanded = false }) {
            options.forEach { option -> DropdownMenuItem(text = { Text("${option.code} - ${option.label}") }, onClick = { onCodeSelected(option.code); expanded = false }) }
        }
    }
}

@Composable
private fun UrgencyRadioGroup(selectedCode: String, onCodeSelected: (String) -> Unit) {
    Surface(modifier = Modifier.fillMaxWidth(), shape = RoundedCornerShape(16.dp), color = PactSurface, border = BorderStroke(1.dp, PactAccent)) {
        Column(modifier = Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
            Text(text = "Urgency", style = MaterialTheme.typography.labelLarge, color = PactTextSecondary)
            urgencyOptions.forEach { option ->
                Row(modifier = Modifier.fillMaxWidth(), verticalAlignment = Alignment.CenterVertically) {
                    RadioButton(selected = selectedCode == option.code, onClick = { onCodeSelected(option.code) }, colors = RadioButtonDefaults.colors(selectedColor = PactPrimary, unselectedColor = PactTextSecondary))
                    Spacer(modifier = Modifier.width(8.dp))
                    Text(text = "${option.label} (${option.code})", style = MaterialTheme.typography.bodyLarge, color = PactTextPrimary)
                }
            }
        }
    }
}
```

---

<a id="file-android-app-src-main-java-org-humanitarian-fieldapp-ui-smsdecoderscreen-kt"></a>
## File: `android/app/src/main/java/org/humanitarian/fieldapp/ui/SmsDecoderScreen.kt`

```kotlin
package org.humanitarian.fieldapp.ui

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.TopAppBarDefaults
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import org.humanitarian.fieldapp.sms.SmsDecoder
import org.humanitarian.fieldapp.ui.theme.PactAccent
import org.humanitarian.fieldapp.ui.theme.PactBackground
import org.humanitarian.fieldapp.ui.theme.PactOnPrimary
import org.humanitarian.fieldapp.ui.theme.PactPrimary
import org.humanitarian.fieldapp.ui.theme.PactSurface
import org.humanitarian.fieldapp.ui.theme.PactTextPrimary
import org.humanitarian.fieldapp.ui.theme.PactTextSecondary

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SmsDecoderScreen(
    onBack: () -> Unit
) {
    var input by remember { mutableStateOf("") }
    var result by remember { mutableStateOf<SmsDecoder.DecodedSms?>(null) }
    var showTechnical by remember { mutableStateOf(false) }

    Scaffold(
        containerColor = PactBackground,
        topBar = {
            TopAppBar(
                title = {
                    Text(
                        text = "SMS Decoder",
                        style = MaterialTheme.typography.titleLarge,
                        fontWeight = FontWeight.SemiBold,
                        color = PactTextPrimary
                    )
                },
                navigationIcon = {
                    TextButton(onClick = onBack) {
                        Text(text = "Back", color = PactPrimary, fontWeight = FontWeight.SemiBold)
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = PactSurface,
                    titleContentColor = PactTextPrimary,
                    navigationIconContentColor = PactPrimary
                )
            )
        }
    ) { padding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .verticalScroll(rememberScrollState())
                .padding(20.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            Surface(
                modifier = Modifier.fillMaxWidth(),
                shape = RoundedCornerShape(24.dp),
                color = PactSurface,
                border = BorderStroke(1.dp, PactAccent)
            ) {
                Column(modifier = Modifier.padding(20.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    Text(
                        text = "SMS Decoder Demo",
                        style = MaterialTheme.typography.headlineSmall,
                        fontWeight = FontWeight.SemiBold,
                        color = PactTextPrimary
                    )
                    Text(
                        text = "Paste an SMS payload and it will be decoded into a readable message. Encoding and decoding are handled by separate functions.",
                        style = MaterialTheme.typography.bodyMedium,
                        color = PactTextSecondary
                    )
                }
            }

            OutlinedTextField(
                value = input,
                onValueChange = { input = it },
                label = { Text("SMS Payload") },
                supportingText = { Text("Example: N|001|NGO01|RA|F|300|H|1C") },
                minLines = 3,
                shape = RoundedCornerShape(16.dp),
                modifier = Modifier.fillMaxWidth()
            )

            SamplePayloadRow { sample ->
                input = sample
                result = null
                showTechnical = false
            }

            Button(
                onClick = {
                    result = SmsDecoder.decode(input)
                    showTechnical = false
                },
                modifier = Modifier.fillMaxWidth().height(56.dp),
                shape = RoundedCornerShape(16.dp),
                colors = ButtonDefaults.buttonColors(containerColor = PactPrimary, contentColor = PactOnPrimary)
            ) {
                Text("Decode SMS", style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.SemiBold)
            }

            val decoded = result
            if (decoded != null) {
                Surface(
                    modifier = Modifier.fillMaxWidth(),
                    shape = RoundedCornerShape(24.dp),
                    color = PactSurface,
                    border = BorderStroke(1.dp, if (decoded.valid) PactAccent else PactPrimary)
                ) {
                    Column(modifier = Modifier.padding(20.dp), verticalArrangement = Arrangement.spacedBy(12.dp)) {
                        if (decoded.valid) {
                            // Type + integrity badge
                            Row(
                                modifier = Modifier.fillMaxWidth(),
                                horizontalArrangement = Arrangement.SpaceBetween,
                                verticalAlignment = Alignment.CenterVertically
                            ) {
                                Text(
                                    text = decoded.typeLabel,
                                    style = MaterialTheme.typography.titleMedium,
                                    fontWeight = FontWeight.SemiBold,
                                    color = PactTextSecondary
                                )
                                Text(
                                    text = "Integrity verified",
                                    style = MaterialTheme.typography.labelLarge,
                                    fontWeight = FontWeight.SemiBold,
                                    color = PactPrimary
                                )
                            }

                            // PRIMARY OUTPUT: the readable decoded message
                            Surface(
                                modifier = Modifier.fillMaxWidth(),
                                shape = RoundedCornerShape(16.dp),
                                color = PactBackground,
                                border = BorderStroke(1.dp, PactAccent)
                            ) {
                                Text(
                                    text = decoded.message,
                                    modifier = Modifier.padding(16.dp),
                                    style = MaterialTheme.typography.bodyLarge,
                                    fontWeight = FontWeight.Medium,
                                    color = PactTextPrimary
                                )
                            }

                            // Optional technical details (hidden by default)
                            OutlinedButton(
                                onClick = { showTechnical = !showTechnical },
                                modifier = Modifier.fillMaxWidth(),
                                shape = RoundedCornerShape(16.dp),
                                border = BorderStroke(1.dp, PactAccent),
                                colors = ButtonDefaults.outlinedButtonColors(
                                    containerColor = PactSurface, contentColor = PactTextPrimary
                                )
                            ) {
                                Text(
                                    text = if (showTechnical) "Hide technical details" else "Show technical details",
                                    style = MaterialTheme.typography.titleMedium,
                                    fontWeight = FontWeight.Medium
                                )
                            }

                            if (showTechnical) {
                                decoded.fields.forEach { (key, value) ->
                                    Column {
                                        Text(key, style = MaterialTheme.typography.labelLarge, color = PactTextSecondary)
                                        Text(
                                            text = value,
                                            style = MaterialTheme.typography.bodyLarge,
                                            fontWeight = FontWeight.Medium,
                                            color = PactTextPrimary
                                        )
                                    }
                                }

                                Box(modifier = Modifier.fillMaxWidth().height(1.dp).background(PactAccent))

                                Text(
                                    text = "Structured JSON (for agent pipeline)",
                                    style = MaterialTheme.typography.titleMedium,
                                    fontWeight = FontWeight.SemiBold,
                                    color = PactTextPrimary
                                )
                                Surface(
                                    modifier = Modifier.fillMaxWidth(),
                                    shape = RoundedCornerShape(12.dp),
                                    color = PactBackground,
                                    border = BorderStroke(1.dp, PactAccent)
                                ) {
                                    Text(
                                        text = decoded.json,
                                        modifier = Modifier.padding(16.dp),
                                        style = MaterialTheme.typography.bodyMedium,
                                        fontFamily = FontFamily.Monospace,
                                        color = PactTextPrimary
                                    )
                                }
                            }
                        } else {
                            Text(
                                text = "Decode Failed",
                                style = MaterialTheme.typography.titleLarge,
                                fontWeight = FontWeight.SemiBold,
                                color = PactPrimary
                            )
                            Text(text = decoded.error, style = MaterialTheme.typography.bodyMedium, color = PactTextSecondary)
                        }
                    }
                }
            }
        }
    }
}

@Composable
private fun SamplePayloadRow(
    onSelect: (String) -> Unit
) {
    // Checksums below are the REAL XOR values (sms.md examples are illustrative).
    val samples = listOf(
        "SOS (Q)" to "Q|101|TN01|11414C03L1|64PZKFHQPC|79",
        "Confirm (C)" to "C|001|CIT00|PLAN_14551|OK|0|1C",
        "Need (N)" to "N|001|NGO01|RA|F|300|H|1C",
        "Status (S)" to "S|004|PLAN101|3|0B",
        "Marker (M)" to "M|008|23.2599,77.4126|CR|9|F300|7B"
    )

    Row(
        modifier = Modifier.fillMaxWidth().horizontalScroll(rememberScrollState()),
        horizontalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        samples.forEach { (label, payload) ->
            OutlinedButton(
                onClick = { onSelect(payload) },
                shape = RoundedCornerShape(16.dp),
                border = BorderStroke(1.dp, PactAccent),
                colors = ButtonDefaults.outlinedButtonColors(containerColor = PactSurface, contentColor = PactTextPrimary)
            ) {
                Text(text = label, style = MaterialTheme.typography.labelLarge)
            }
        }
    }
}
```

---

<a id="file-android-app-src-main-java-org-humanitarian-fieldapp-ui-smsfallbackscreen-kt"></a>
## File: `android/app/src/main/java/org/humanitarian/fieldapp/ui/SmsFallbackScreen.kt`

```kotlin
package org.humanitarian.fieldapp.ui

import android.content.Intent
import android.net.Uri
import android.telephony.SmsManager
import android.widget.Toast
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalClipboardManager
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.AnnotatedString
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import kotlinx.coroutines.launch
import org.humanitarian.fieldapp.network.ApiClient
import org.humanitarian.fieldapp.network.ApiResult
import org.humanitarian.fieldapp.offline.OfflineQueue
import org.humanitarian.fieldapp.ui.theme.*

const val PACT_GATEWAY_PHONE = "9345302551"

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SmsFallbackScreen(onBack: () -> Unit) {
    val context = LocalContext.current
    val clipboardManager = LocalClipboardManager.current
    val coroutineScope = rememberCoroutineScope()
    
    var queuedPayloads by remember { mutableStateOf<List<String>>(emptyList()) }
    var statusMessage by remember { mutableStateOf("") }

    fun refreshQueue() {
        val reports = OfflineQueue.getQueuedReports(context)
        queuedPayloads = reports.map { it.smsPayload }.filter { it.isNotBlank() }
    }

    LaunchedEffect(Unit) {
        refreshQueue()
    }

    fun dispatchSms(payload: String) {
        val success = org.humanitarian.fieldapp.sms.DirectSmsSender.sendDirectSms(context, PACT_GATEWAY_PHONE, payload)
        if (success) {
            Toast.makeText(context, "SMS dispatched to $PACT_GATEWAY_PHONE", Toast.LENGTH_LONG).show()
            statusMessage = "Dispatched SMS directly to $PACT_GATEWAY_PHONE via Cellular SIM."
        } else {
            val intent = Intent(Intent.ACTION_SENDTO).apply {
                data = Uri.parse("smsto:$PACT_GATEWAY_PHONE")
                putExtra("sms_body", payload)
            }
            context.startActivity(intent)
            statusMessage = "Opened SMS Messenger for $PACT_GATEWAY_PHONE."
        }
    }

    Scaffold(
        containerColor = PactBackground,
        topBar = {
            TopAppBar(
                title = { Text("SMS Fallback Queue", fontWeight = FontWeight.SemiBold, color = PactTextPrimary) },
                navigationIcon = { TextButton(onClick = onBack) { Text("Back", color = PactPrimary) } },
                colors = TopAppBarDefaults.topAppBarColors(containerColor = PactSurface)
            )
        }
    ) { padding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .verticalScroll(rememberScrollState())
                .padding(20.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            Surface(
                modifier = Modifier.fillMaxWidth(),
                shape = RoundedCornerShape(16.dp),
                color = PactSurface,
                border = BorderStroke(1.dp, PactAccent)
            ) {
                Column(modifier = Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) {
                    Text("Gateway Target: $PACT_GATEWAY_PHONE", fontWeight = FontWeight.Bold, color = PactTextPrimary)
                    Text("Messages are sent directly over GSM cellular SMS to your Termux gateway laptop bridge.", color = PactTextSecondary, style = MaterialTheme.typography.bodySmall)
                }
            }

            if (queuedPayloads.isEmpty()) {
                Text("No pending SMS reports in queue.", color = PactTextSecondary)
            } else {
                Text("Pending Reports: ${queuedPayloads.size}", style = MaterialTheme.typography.titleMedium, color = PactTextPrimary)
                
                for ((index, payload) in queuedPayloads.withIndex()) {
                    Surface(
                        modifier = Modifier.fillMaxWidth(),
                        shape = RoundedCornerShape(16.dp),
                        color = PactSurface,
                        border = BorderStroke(1.dp, PactAccent)
                    ) {
                        Column(modifier = Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(12.dp)) {
                            Text("Report #${index + 1}", fontWeight = FontWeight.Bold, color = PactTextPrimary)
                            
                            Text(
                                text = payload,
                                fontFamily = FontFamily.Monospace,
                                color = PactPrimary,
                                modifier = Modifier.fillMaxWidth()
                            )

                            Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                                Button(
                                    onClick = { dispatchSms(payload) },
                                    modifier = Modifier.fillMaxWidth(),
                                    colors = ButtonDefaults.buttonColors(containerColor = PactPrimary, contentColor = PactOnPrimary)
                                ) { 
                                    Text("📱 Send Cellular SMS ($PACT_GATEWAY_PHONE)") 
                                }

                                Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                                    OutlinedButton(
                                        onClick = { 
                                            clipboardManager.setText(AnnotatedString(payload))
                                            Toast.makeText(context, "Copied payload", Toast.LENGTH_SHORT).show()
                                        },
                                        modifier = Modifier.weight(1f),
                                        colors = ButtonDefaults.outlinedButtonColors(contentColor = PactTextPrimary)
                                    ) { Text("Copy") }

                                    Button(
                                        onClick = {
                                            coroutineScope.launch {
                                                statusMessage = "Sending via HTTP Gateway API..."
                                                when (val result = ApiClient.postSmsWebhook(payload)) {
                                                    is ApiResult.Success -> {
                                                        statusMessage = "Success! Ingested by backend."
                                                    }
                                                    is ApiResult.Error -> {
                                                        statusMessage = "HTTP Failed: ${result.message}"
                                                    }
                                                }
                                            }
                                        },
                                        modifier = Modifier.weight(1f),
                                        colors = ButtonDefaults.buttonColors(containerColor = PactAccent, contentColor = PactTextPrimary)
                                    ) { Text("HTTP Bridge") }
                                }
                            }
                        }
                    }
                }
            }
            
            if (statusMessage.isNotBlank()) {
                Text(statusMessage, color = PactPrimary, fontWeight = FontWeight.Bold)
            }
        }
    }
}
```

---

<a id="file-android-app-src-main-java-org-humanitarian-fieldapp-ui-homescreen-kt"></a>
## File: `android/app/src/main/java/org/humanitarian/fieldapp/ui/HomeScreen.kt`

```kotlin
package org.humanitarian.fieldapp.ui

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.TopAppBarDefaults
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import org.humanitarian.fieldapp.offline.OfflineQueue
import org.humanitarian.fieldapp.sync.SyncManager
import org.humanitarian.fieldapp.ui.theme.PactAccent
import org.humanitarian.fieldapp.ui.theme.PactBackground
import org.humanitarian.fieldapp.ui.theme.PactOnPrimary
import org.humanitarian.fieldapp.ui.theme.PactPrimary
import org.humanitarian.fieldapp.ui.theme.PactSurface
import org.humanitarian.fieldapp.ui.theme.PactTextPrimary
import org.humanitarian.fieldapp.ui.theme.PactTextSecondary

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun HomeScreen(
    onNavigateToFieldReport: () -> Unit,
    onNavigateToMyRequests: () -> Unit,
    onNavigateToSmsFallback: () -> Unit,
    onNavigateToSmsDecoder: () -> Unit,
    onNavigateToOfflineMap: () -> Unit,
    onNavigateToStatus: () -> Unit
) {
    val context = LocalContext.current
    var queueSize by remember { mutableStateOf(OfflineQueue.getQueueSize(context)) }
    var autoSyncMessage by remember { mutableStateOf("") }

    // Auto-sync whenever the home screen opens.
    // If internet is back, queued reports are pushed to the backend silently.
    LaunchedEffect(Unit) {
        queueSize = OfflineQueue.getQueueSize(context)
        if (queueSize > 0) {
            val result = SyncManager.syncQueue(context)
            if (result.synced > 0) {
                autoSyncMessage = "${result.synced} queued report(s) synced automatically."
            }
            queueSize = OfflineQueue.getQueueSize(context)
        }
    }

    Scaffold(
        containerColor = PactBackground,
        topBar = {
            TopAppBar(
                title = {
                    Column {
                        Text(
                            text = "PACT Field App",
                            style = MaterialTheme.typography.titleLarge,
                            fontWeight = FontWeight.SemiBold,
                            color = PactTextPrimary
                        )
                        Text(
                            text = "Offline-first humanitarian coordination",
                            style = MaterialTheme.typography.bodySmall,
                            color = PactTextSecondary
                        )
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = PactSurface,
                    titleContentColor = PactTextPrimary
                )
            )
        }
    ) { padding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .verticalScroll(rememberScrollState())
                .padding(20.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            Surface(
                modifier = Modifier.fillMaxWidth(),
                shape = RoundedCornerShape(24.dp),
                color = PactSurface,
                border = BorderStroke(1.dp, PactAccent)
            ) {
                Column(modifier = Modifier.padding(20.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    Text(
                        text = "Mission Console",
                        style = MaterialTheme.typography.headlineSmall,
                        fontWeight = FontWeight.SemiBold,
                        color = PactTextPrimary
                    )
                    Text(
                        text = "Select an operational module. The interface is optimized for low connectivity and fast field use.",
                        style = MaterialTheme.typography.bodyMedium,
                        color = PactTextSecondary
                    )
                }
            }

            // OFFLINE QUEUE BANNER
            if (queueSize > 0) {
                Surface(
                    modifier = Modifier.fillMaxWidth(),
                    shape = RoundedCornerShape(16.dp),
                    color = PactAccent,
                    border = BorderStroke(1.dp, PactPrimary)
                ) {
                    Column(modifier = Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(4.dp)) {
                        Text(
                            text = "$queueSize report(s) in offline queue",
                            style = MaterialTheme.typography.titleMedium,
                            fontWeight = FontWeight.SemiBold,
                            color = PactTextPrimary
                        )
                        Text(
                            text = "Open My Requests to view payloads or sync when internet returns.",
                            style = MaterialTheme.typography.bodySmall,
                            color = PactTextSecondary
                        )
                    }
                }
            }

            if (autoSyncMessage.isNotBlank()) {
                Text(
                    text = autoSyncMessage,
                    style = MaterialTheme.typography.bodyMedium,
                    fontWeight = FontWeight.Medium,
                    color = PactPrimary
                )
            }

            Button(
                onClick = onNavigateToFieldReport,
                modifier = Modifier.fillMaxWidth().height(56.dp),
                shape = RoundedCornerShape(16.dp),
                colors = ButtonDefaults.buttonColors(
                    containerColor = PactPrimary,
                    contentColor = PactOnPrimary
                )
            ) {
                Text(
                    text = "Field Report",
                    style = MaterialTheme.typography.titleMedium,
                    fontWeight = FontWeight.SemiBold
                )
            }

            Button(
                onClick = onNavigateToMyRequests,
                modifier = Modifier.fillMaxWidth().height(56.dp),
                shape = RoundedCornerShape(16.dp),
                colors = ButtonDefaults.buttonColors(
                    containerColor = PactSurface,
                    contentColor = PactTextPrimary
                ),
                border = BorderStroke(1.dp, PactAccent)
            ) {
                Text(
                    text = "My Requests",
                    style = MaterialTheme.typography.titleMedium,
                    fontWeight = FontWeight.SemiBold
                )
            }

            HomeActionButton(title = "SMS Fallback", onClick = onNavigateToSmsFallback)
            HomeActionButton(title = "SMS Decoder", onClick = onNavigateToSmsDecoder)
            HomeActionButton(title = "Offline Map", onClick = onNavigateToOfflineMap)
            HomeActionButton(title = "Status Update", onClick = onNavigateToStatus)
        }
    }
}

@Composable
private fun HomeActionButton(
    title: String,
    onClick: () -> Unit
) {
    OutlinedButton(
        onClick = onClick,
        modifier = Modifier.fillMaxWidth().height(56.dp),
        shape = RoundedCornerShape(16.dp),
        border = BorderStroke(1.dp, PactAccent),
        colors = ButtonDefaults.outlinedButtonColors(
            containerColor = PactBackground,
            contentColor = PactTextPrimary
        )
    ) {
        Text(
            text = title,
            style = MaterialTheme.typography.titleMedium,
            fontWeight = FontWeight.Medium
        )
    }
}
```

---

<a id="file-app-static-index-html"></a>
## File: `app/static/index.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>PACT — Autonomous Multi-Agent Coordination Platform</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin=""/>
  <link rel="stylesheet" href="/static/css/styles.css">
</head>
<body>

  <!-- Top Command Header -->
  <header class="command-header">
    <div class="brand-block">
      <div class="brand-monogram">PACT</div>
      <div class="brand-meta">
        <h1 id="headerTitle">Autonomous Crisis Coordination Center</h1>
        <p id="headerSubtitle">Zero-Connectivity Resilience · Zero-Hallucination Solvers · Multi-Agent Negotiation</p>
      </div>
    </div>

    <div class="header-actions">
      <!-- Organization / Persona Switcher Dropdown -->
      <div class="persona-switcher-box">
        <label for="orgPersonaSelect" class="persona-label">ACTIVE PORTAL:</label>
        <select id="orgPersonaSelect" class="persona-dropdown" onchange="onOrgPersonaChanged()">
          <option value="ADMIN_ALL">Global Command (Admin / All)</option>
          <option value="NGO_TN_RED_CROSS">Red Cross Tamil Nadu</option>
          <option value="TNDRF_ARAKKONAM_CHENNAI">TNDRF Search and Rescue Force</option>
          <option value="HOSPITAL_CHENNAI_RGGGH">Apollo / Trauma Medical Center</option>
          <option value="CSR_TATA_SOUTH_HUB">Tata / CSR Logistics Hub</option>
          <option value="COIMBATORE_GHAT_RESCUE">Nilgiris Mountain Rescue</option>
        </select>
      </div>

      <div id="wsStatusPill" class="hud-pill disconnected">
        <span class="hud-pip"></span>
        <span id="wsStatusText">CONNECTING BUS</span>
      </div>

      <div id="adminAutopilotWrap" class="tactile-switch">
        <span class="switch-label">Autopilot (3s)</span>
        <label class="toggle-track">
          <input type="checkbox" id="autopilotToggle" checked>
          <span class="toggle-slider"></span>
        </label>
      </div>

      <button id="btnResetSeed" class="btn-tactile">
        Reset Depots
      </button>

      <a href="/docs" target="_blank" class="btn-tactile btn-primary">
        OpenAPI Spec
      </a>
    </div>
  </header>

  <!-- =========================================================================
       1. GLOBAL ADMIN INCIDENT COMMAND VIEW (Visible only to Admin)
       ========================================================================= -->
  <main id="adminViewContainer" class="bento-container">

    <!-- Hero Telemetry Matrix -->
    <section class="hero-telemetry-matrix">
      <div class="telemetry-card">
        <div class="telemetry-top">
          <span class="telemetry-title">Ingested SOS Frames</span>
          <span class="telemetry-code">PACKET_Q</span>
        </div>
        <div class="telemetry-value-wrap">
          <span id="statTotalRequests" class="telemetry-num">0</span>
          <span class="telemetry-sub">transmissions</span>
        </div>
      </div>

      <div class="telemetry-card">
        <div class="telemetry-top">
          <span class="telemetry-title">Active Depots</span>
          <span class="telemetry-code">REGISTRY</span>
        </div>
        <div class="telemetry-value-wrap">
          <span id="statActiveOffers" class="telemetry-num">11</span>
          <span class="telemetry-sub">relief hubs</span>
        </div>
      </div>

      <div class="telemetry-card">
        <div class="telemetry-top">
          <span class="telemetry-title">Committed Dispatches</span>
          <span class="telemetry-code">ALLOC_COMMITTED</span>
        </div>
        <div class="telemetry-value-wrap">
          <span id="statCommittedMatches" class="telemetry-num">0</span>
          <span class="telemetry-sub">verified plans</span>
        </div>
      </div>

      <div class="telemetry-card">
        <div class="telemetry-top">
          <span class="telemetry-title">Agent Bus Events</span>
          <span class="telemetry-code">EVENT_BUS</span>
        </div>
        <div class="telemetry-value-wrap">
          <span id="statAgentEvents" class="telemetry-num">0</span>
          <span class="telemetry-sub">signals</span>
        </div>
      </div>
    </section>

    <!-- Master Bento Workspace -->
    <div class="bento-workspace">

      <!-- LEFT: Pipeline Reasoning, Multi-Agent Debate & Solver Matrix -->
      <section class="bento-card">
        <div class="bento-card-header">
          <div class="bento-title-group">
            <div class="bento-title">Autonomous Multi-Agent Pipeline and Negotiation</div>
          </div>
          <span id="activeRunBadge" class="bento-badge">TRACE: STANDBY</span>
        </div>

        <div class="bento-body">
          <!-- 11-Stage Connected Rail Tracker -->
          <div class="pipeline-rail">
            <div id="step-A0" class="rail-node">A0 Intake</div>
            <div id="step-A1" class="rail-node">A1 Dedupe</div>
            <div id="step-A2" class="rail-node">A2 Triage</div>
            <div id="step-A3" class="rail-node">A3 GeoNear</div>
            <div id="step-A4" class="rail-node">A4 Debate</div>
            <div id="step-A5" class="rail-node">A5 Solver</div>
            <div id="step-A6" class="rail-node">A6 Arbiter</div>
            <div id="step-A7" class="rail-node">A7 Privacy</div>
            <div id="step-A8" class="rail-node">A8 Gate</div>
            <div id="step-A9" class="rail-node">A9 Bulletin</div>
            <div id="step-A10" class="rail-node">A10 Commit</div>
          </div>

          <!-- Tactical Reasoning Stream Deck -->
          <div class="terminal-deck">
            <div class="deck-label">
              <span>Multi-Agent Live Telemetry and Negotiation Stream</span>
              <span>Groq LLM (Llama 3.3) · Autonomous Agents</span>
            </div>
            <div id="streamContent" class="terminal-viewport">System online. Listening on cellular GSM-7 ingress channel...</div>
          </div>

          <!-- Multi-Agency Tactical Capacity & Deliberation Feed -->
          <div class="terminal-deck">
            <div class="deck-label">
              <span>Nearby Provider Advocate Agents Deliberation (A4)</span>
              <span>LIVE DATABASE AND TOOL ACCESS</span>
            </div>
            <div id="debateFeed" class="capacity-feed-deck">
              <div class="capacity-node">
                <div class="capacity-node-header">
                  <span class="capacity-node-name">Multi-Agency Negotiation Chamber</span>
                  <span class="capacity-node-role">ACTIVE</span>
                </div>
                <div class="capacity-node-body">Awaiting inbound emergency frame to initiate autonomous multi-agent dialogue, route assessment, and consensus building.</div>
              </div>
            </div>
          </div>

          <!-- 3-Option Comparative Solver Deck -->
          <div class="terminal-deck">
            <div class="deck-label">
              <span>Comparative Solver Plans (A5) and Arbiter Selection (A6)</span>
              <span>DETERMINISTIC OPTIMIZER</span>
            </div>
            <div id="solverOptionsGrid" class="solver-deck">
              <div class="solver-option-card">
                <div class="solver-card-header">[1] Fastest Response</div>
                <div class="solver-metrics-row"><span>COV: --</span><span>ETA: --</span></div>
                <div class="solver-track"><div class="solver-fill" style="width:0%"></div></div>
              </div>
              <div class="solver-option-card">
                <div class="solver-card-header">[2] Max Coverage</div>
                <div class="solver-metrics-row"><span>COV: --</span><span>ETA: --</span></div>
                <div class="solver-track"><div class="solver-fill" style="width:0%"></div></div>
              </div>
              <div class="solver-option-card">
                <div class="solver-card-header">[3] Least Depleting</div>
                <div class="solver-metrics-row"><span>COV: --</span><span>ETA: --</span></div>
                <div class="solver-track"><div class="solver-fill" style="width:0%"></div></div>
              </div>
            </div>
          </div>

          <!-- Review Gate Action Bar -->
          <div id="adminActionBar" class="review-gate-bar" style="display:none;">
            <div class="gate-info">
              <h4 id="adminActionTitle">Awaiting Commander Review</h4>
              <p>Autopilot paused. Verify allocations before dispatch authorization.</p>
            </div>
            <div style="display:flex; gap:0.5rem;">
              <button class="btn-tactile btn-success" onclick="submitAdminDecision('approve')">Commit Plan</button>
              <button class="btn-tactile btn-danger" onclick="submitAdminDecision('reject')">Reject Plan</button>
            </div>
          </div>

          <!-- Outbound Acknowledgement Deck Banner -->
          <div id="ackFrameBox" class="ack-deck-banner" style="display:none;"></div>

        </div>
      </section>

      <!-- RIGHT: Spatial Operations Map & NOC Telemetry -->
      <section style="display:flex; flex-direction:column; gap:1.25rem;">

        <!-- Spatial Operations Map Panel -->
        <div class="bento-card">
          <div class="bento-card-header">
            <div class="bento-title-group">
              <div class="bento-title">Disaster Spatial Operations ($geoNear)</div>
            </div>
            <span class="bento-badge">OpenStreetMap</span>
          </div>
          <div style="padding:0;">
            <div id="crisisMapContainer" class="map-canvas-container"></div>
          </div>
        </div>

        <!-- NOC Cellular Gateway Operations Panel -->
        <div class="bento-card">
          <div class="bento-card-header">
            <div class="bento-title-group">
              <div class="bento-title">GSM-7 Cellular Ingress Operations</div>
            </div>
            <span class="hud-tag hud-tag-success">ONLINE</span>
          </div>
          <div class="bento-body">
            <div class="noc-grid">
              <div class="noc-cell">
                <div class="noc-cell-label">Ingress Channel</div>
                <div class="noc-cell-value">GSM Cellular SMS</div>
              </div>
              <div class="noc-cell">
                <div class="noc-cell-label">Privacy Shield</div>
                <div class="noc-cell-value">Zero-Knowledge 2km Grid</div>
              </div>
              <div class="noc-cell">
                <div class="noc-cell-label">Spatial Codec</div>
                <div class="noc-cell-value">PACK10 (10-char Base-36)</div>
              </div>
              <div class="noc-cell">
                <div class="noc-cell-label">Data Integrity</div>
                <div class="noc-cell-value">2-Char Bitwise XOR CRC</div>
              </div>
            </div>

            <div style="font-family:var(--font-mono); font-size:0.72rem; color:var(--pact-muted); padding-top:0.4rem; border-top:1px solid var(--pact-border);">
              Cellular gateway online. Ingesting emergency frames (<code>Q|...</code> / <code>N|...</code>) via cellular SIM.
            </div>
          </div>
        </div>

      </section>

    </div>

    <!-- Bottom Registry Tables Section -->
    <section class="registry-tables-grid">

      <!-- Inbound Emergency SOS Log -->
      <div class="bento-card">
        <div class="bento-card-header">
          <div class="bento-title">Inbound Emergency SOS Log</div>
          <button class="btn-tactile" onclick="loadRequestsTable()">Refresh</button>
        </div>
        <div class="table-responsive">
          <table class="tactile-table">
            <thead>
              <tr>
                <th>UID</th>
                <th>Situation</th>
                <th>Headcount</th>
                <th>Urgency</th>
                <th>Frame</th>
              </tr>
            </thead>
            <tbody id="requestsTableBody">
              <!-- Populated dynamically -->
            </tbody>
          </table>
        </div>
      </div>

      <!-- Committed Humanitarian Dispatch Registry -->
      <div class="bento-card">
        <div class="bento-card-header">
          <div class="bento-title">Global Committed Dispatch Registry</div>
          <button class="btn-tactile" onclick="loadMatchesTable()">Refresh</button>
        </div>
        <div class="table-responsive">
          <table class="tactile-table">
            <thead>
              <tr>
                <th>Plan ID</th>
                <th>Recipient</th>
                <th>Strategy</th>
                <th>Status</th>
                <th>Inspect</th>
              </tr>
            </thead>
            <tbody id="matchesTableBody">
              <!-- Populated dynamically -->
            </tbody>
          </table>
        </div>
      </div>

    </section>

  </main>

  <!-- =========================================================================
       2. FIELD ORGANIZATION DISPATCH PORTAL (Red Cross / TNDRF / Apollo / Tata)
       ========================================================================= -->
  <main id="providerViewContainer" class="bento-container" style="display:none;">

    <!-- Active Organization Hero Banner -->
    <div class="persona-active-banner">
      <div>
        <h2 id="pOrgTitle" style="font-size:1.1rem; font-weight:800; color:var(--pact-text); margin:0;">Red Cross Tamil Nadu Relief Command</h2>
        <p id="pOrgSubtitle" style="font-size:0.78rem; color:var(--pact-muted); margin:0;">Field Operations Portal · Viewing only victims & relief supplies allocated to your organization.</p>
      </div>
      <button class="btn-tactile" onclick="resetToAdminView()">Switch to Admin View</button>
    </div>

    <!-- Provider Specific Metrics Matrix -->
    <section class="hero-telemetry-matrix">
      <div class="telemetry-card">
        <div class="telemetry-top">
          <span class="telemetry-title">Assigned Missions</span>
          <span class="telemetry-code">MY_ALLOC</span>
        </div>
        <div class="telemetry-value-wrap">
          <span id="pStatMissions" class="telemetry-num">0</span>
          <span class="telemetry-sub">active victims</span>
        </div>
      </div>

      <div class="telemetry-card">
        <div class="telemetry-top">
          <span class="telemetry-title">Committed Supplies</span>
          <span class="telemetry-code">QUOTA</span>
        </div>
        <div class="telemetry-value-wrap">
          <span id="pStatSupplies" class="telemetry-num" style="font-size:1.4rem;">0 Units</span>
          <span class="telemetry-sub">allocated</span>
        </div>
      </div>

      <div class="telemetry-card">
        <div class="telemetry-top">
          <span class="telemetry-title">Base Depot</span>
          <span class="telemetry-code">STATION</span>
        </div>
        <div class="telemetry-value-wrap">
          <span id="pStatBase" class="telemetry-num" style="font-size:1.2rem; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">Chennai</span>
          <span class="telemetry-sub">operational</span>
        </div>
      </div>

      <div class="telemetry-card">
        <div class="telemetry-top">
          <span class="telemetry-title">Fleet Readiness</span>
          <span class="telemetry-code">TRANSPORT</span>
        </div>
        <div class="telemetry-value-wrap">
          <span id="pStatFleet" class="telemetry-num" style="font-size:1.1rem;">Active Fleet</span>
          <span class="telemetry-sub">ready</span>
        </div>
      </div>
    </section>

    <!-- Provider Workspace (Assigned Missions & Focused Map) -->
    <div class="bento-workspace">

      <!-- LEFT: Matched Help Seekers & Mission Details -->
      <section style="display:flex; flex-direction:column; gap:1.25rem;">

        <!-- Matched Help Seekers Table Card -->
        <div class="bento-card">
          <div class="bento-card-header">
            <div class="bento-title">Assigned Help-Seeker Queue</div>
            <span class="bento-badge" id="pQueueCount">0 MATCHES</span>
          </div>
          <div class="table-responsive">
            <table class="tactile-table">
              <thead>
                <tr>
                  <th>Victim ID</th>
                  <th>Incident & Severity</th>
                  <th>Casualties</th>
                  <th>Supplies Needed</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody id="providerMatchesTableBody">
                <!-- Populated dynamically -->
              </tbody>
            </table>
          </div>
        </div>

        <!-- Selected Help Seeker Detail Card -->
        <div id="pSelectedVictimCard" class="bento-card" style="border-left: 4px solid var(--pact-primary);">
          <div class="bento-card-header">
            <div class="bento-title" id="pCardTitle">Target Incident Details</div>
            <span id="pCardStatusBadge" class="hud-tag hud-tag-info">SELECT A VICTIM</span>
          </div>
          <div class="bento-body">
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:0.75rem;">
              <div class="modal-stat-box">
                <div class="modal-stat-label">INCIDENT TYPE & CASUALTIES</div>
                <div id="pDetailIncident" class="modal-stat-val">Select a victim from the queue above</div>
              </div>
              <div class="modal-stat-box">
                <div class="modal-stat-label">ALLOCATED ITEMS TO DELIVER</div>
                <div id="pDetailItems" class="modal-stat-val">--</div>
              </div>
              <div class="modal-stat-box">
                <div class="modal-stat-label">ESTIMATED TRANSIT & DISTANCE</div>
                <div id="pDetailETA" class="modal-stat-val">--</div>
              </div>
              <div class="modal-stat-box">
                <div class="modal-stat-label">TARGET GPS COORDINATES</div>
                <div id="pDetailCoords" class="modal-stat-val" style="font-family:var(--font-mono); font-size:0.75rem;">--</div>
              </div>
            </div>

            <div style="display:flex; justify-content:space-between; align-items:center; margin-top:0.5rem; padding-top:0.75rem; border-top:1px solid var(--pact-border);">
              <span style="font-size:0.75rem; color:var(--pact-muted);">Confirm delivery dispatch from your depot:</span>
              <button class="btn-tactile btn-success" onclick="confirmProviderDispatch()">Confirm Delivery Dispatched</button>
            </div>
          </div>
        </div>

      </section>

      <!-- RIGHT: Focused Provider Operations Map & Live Stockpile -->
      <section style="display:flex; flex-direction:column; gap:1.25rem;">

        <!-- Focused Provider Operations Map -->
        <div class="bento-card">
          <div class="bento-card-header">
            <div class="bento-title">Operational Deployment Map and Routing</div>
            <span class="bento-badge">Assigned Perimeter</span>
          </div>
          <div style="padding:0;">
            <div id="providerMapContainer" class="map-canvas-container"></div>
          </div>
        </div>

        <!-- Live Depot Warehouse Reserves Card -->
        <div class="bento-card">
          <div class="bento-card-header">
            <div class="bento-title">Live Warehouse Stockpile Reserves</div>
            <span class="hud-tag hud-tag-success">ACTIVE INVENTORY</span>
          </div>
          <div class="bento-body">
            <div id="providerStockGrid" style="display:grid; grid-template-columns: repeat(3, 1fr); gap:0.6rem;">
              <!-- Populated dynamically with live DB inventory -->
            </div>
            <div id="providerFleetText" style="font-size:0.75rem; color:var(--pact-text-secondary); margin-top:0.4rem; padding-top:0.5rem; border-top:1px solid var(--pact-border);">
              Fleet: Loading vehicle readiness...
            </div>
          </div>
        </div>

      </section>

    </div>

  </main>

  <!-- Interactive Dispatch Detail Inspection Modal -->
  <div id="dispatchDetailModal" class="modal-backdrop" style="display:none;">
    <div class="modal-card">
      <div class="modal-header">
        <div>
          <h3 id="modalPlanTitle" style="font-size:1rem; font-weight:700; margin:0;">Dispatch Plan Inspection</h3>
          <p id="modalPlanSubtitle" style="font-size:0.75rem; color:var(--pact-muted); margin:0;">Plan ID: PLAN_00000</p>
        </div>
        <button class="btn-tactile" onclick="closeDispatchModal()">Close</button>
      </div>

      <div class="modal-body">
        <div class="modal-grid">
          <!-- Left: Tactical Details -->
          <div style="display:flex; flex-direction:column; gap:0.75rem;">
            <div class="modal-stat-box">
              <div class="modal-stat-label">RECIPIENT & INCIDENT</div>
              <div id="modalRecipient" class="modal-stat-val">Target: NGO01 · Flood Crisis</div>
            </div>

            <div class="modal-stat-box">
              <div class="modal-stat-label">ALLOCATED SUPPLIES & QUOTA</div>
              <div id="modalSupplies" class="modal-stat-val">286 Hygiene Kits</div>
            </div>

            <div class="modal-stat-box">
              <div class="modal-stat-label">ASSIGNED DEPOT & FLEET</div>
              <div id="modalDepot" class="modal-stat-val">Red Cross Tamil Nadu Relief (ETA ~0.5h)</div>
            </div>

            <div class="modal-stat-box">
              <div class="modal-stat-label">TARGET GPS COORDINATES</div>
              <div id="modalCoords" class="modal-stat-val" style="font-family:var(--font-mono); font-size:0.8rem;">[13.00835, 80.00557] · PACK10: 64S6BFHA5P</div>
            </div>
          </div>

          <!-- Right: Modal Mini-Map View -->
          <div style="display:flex; flex-direction:column; gap:0.5rem;">
            <div style="font-size:0.75rem; font-weight:700; color:var(--pact-text-secondary);">TACTICAL OPENSTREETMAP ROUTING VIEW:</div>
            <div id="modalMapCanvas" style="height:230px; width:100%; border-radius:8px; border:1px solid var(--pact-border);"></div>
          </div>
        </div>
      </div>

      <div class="modal-footer">
        <span id="modalStatusBadge" class="hud-tag hud-tag-success">DISPATCH COMMITTED</span>
        <button class="btn-tactile btn-primary" onclick="focusOnMainMap()">View on Full Operations Map</button>
      </div>
    </div>
  </div>

  <!-- Scripts -->
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script>
  <script src="/static/js/map.js"></script>
  <script src="/static/js/app.js"></script>
</body>
</html>
```

---

<a id="file-app-static-css-styles-css"></a>
## File: `app/static/css/styles.css`

```css
/* ==========================================================================
   PACT — Humanitarian Coordination Dashboard Theme
   Matches the PACT Mobile & Command Center Specification
   Palette:
     Background: #FFFAF3
     Surface:    #FFF2DB
     Accent:     #FFE5BF
     Primary:    #F62440
     PrimaryDark:#D81E38
     Text:       #2B2119
     Muted:      #6B5D4F
     Border:     #EBDDC0 (rgba(120, 85, 40, 0.12))
   ========================================================================== */

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

:root {
  /* Core Theme Tokens */
  --pact-bg: #FFFAF3;
  --pact-surface: #FFF2DB;
  --pact-surface-elevated: #FFF7EB;
  --pact-accent: #FFE5BF;
  --pact-accent-hover: #FDD9A6;
  --pact-primary: #F62440;
  --pact-primary-dark: #D81E38;
  --pact-primary-light: #FEE8EC;

  /* Typography Colors */
  --pact-text: #2B2119;
  --pact-text-secondary: #3B2F23;
  --pact-muted: #6B5D4F;
  --pact-subtle: #8C7C6D;

  /* Borders & Dividers */
  --pact-border: #EBDDC0;
  --pact-border-subtle: rgba(120, 85, 40, 0.12);
  --pact-border-focus: #F62440;

  /* Font Families */
  --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
  --font-mono: 'JetBrains Mono', 'Fira Code', monospace;

  /* Radii & Shadows */
  --radius-sm: 6px;
  --radius-md: 10px;
  --radius-lg: 12px;
  --shadow-subtle: 0 1px 2px rgba(43, 33, 25, 0.04);
  --shadow-card: 0 1px 3px rgba(43, 33, 25, 0.06), 0 1px 2px rgba(43, 33, 25, 0.04);

  /* Status Colors */
  --status-green-bg: #E7F6EC;
  --status-green-text: #196D34;
  --status-green-border: #BFE8CB;

  --status-blue-bg: #E8F1FC;
  --status-blue-text: #175494;
  --status-blue-border: #BFD8F8;

  --status-amber-bg: #FEF3D6;
  --status-amber-text: #8A5B07;
  --status-amber-border: #FCE19B;

  --status-purple-bg: #F2EBFB;
  --status-purple-text: #5B2B9E;
  --status-purple-border: #DDC8F7;

  --status-red-bg: #FEE8EC;
  --status-red-text: #B8142B;
  --status-red-border: #FBBEC7;
}

/* Global Reset & Page Setup */
*, *::before, *::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

html {
  font-size: 14px;
  background-color: var(--pact-bg);
  color: var(--pact-text);
  font-family: var(--font-sans);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

body {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: var(--pact-bg);
  color: var(--pact-text);
}

/* Header Navigation Bar */
.command-header {
  position: sticky;
  top: 0;
  z-index: 1000;
  height: 58px;
  background: var(--pact-surface);
  border-bottom: 1px solid var(--pact-border);
  box-shadow: var(--shadow-subtle);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 1.75rem;
}

.brand-block {
  display: flex;
  align-items: center;
  gap: 0.85rem;
}

.brand-monogram {
  font-family: var(--font-mono);
  font-size: 0.82rem;
  font-weight: 800;
  letter-spacing: 0.08em;
  padding: 0.32rem 0.7rem;
  background: var(--pact-primary);
  border-radius: var(--radius-sm);
  color: #ffffff;
  display: flex;
  align-items: center;
}

.brand-meta {
  display: flex;
  flex-direction: column;
}

.brand-meta h1 {
  font-size: 0.95rem;
  font-weight: 700;
  letter-spacing: -0.01em;
  color: var(--pact-text);
  line-height: 1.2;
}

.brand-meta p {
  font-family: var(--font-sans);
  font-size: 0.68rem;
  color: var(--pact-muted);
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

/* Status Pill */
.hud-pill {
  display: inline-flex;
  align-items: center;
  gap: 0.45rem;
  font-family: var(--font-mono);
  font-size: 0.72rem;
  font-weight: 600;
  padding: 0.32rem 0.75rem;
  border-radius: var(--radius-sm);
  background: var(--pact-accent);
  border: 1px solid var(--pact-border);
  color: var(--pact-text-secondary);
}

.hud-pill.connected {
  color: var(--status-green-text);
  border-color: var(--status-green-border);
  background: var(--status-green-bg);
}

.hud-pill.disconnected {
  color: var(--status-red-text);
  border-color: var(--status-red-border);
  background: var(--status-red-bg);
}

.hud-pip {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: currentColor;
}

/* Toggle Switch */
.tactile-switch {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: var(--pact-accent);
  border: 1px solid var(--pact-border);
  border-radius: var(--radius-sm);
  padding: 0.25rem 0.6rem;
}

.switch-label {
  font-family: var(--font-sans);
  font-size: 0.68rem;
  font-weight: 600;
  color: var(--pact-text-secondary);
  text-transform: uppercase;
}

.toggle-track {
  position: relative;
  width: 32px;
  height: 18px;
  cursor: pointer;
}

.toggle-track input { opacity: 0; width: 0; height: 0; }

.toggle-slider {
  position: absolute;
  inset: 0;
  background: #D8C7AA;
  border-radius: 10px;
  transition: 0.15s ease;
}

.toggle-slider::before {
  content: '';
  position: absolute;
  height: 12px;
  width: 12px;
  left: 3px;
  top: 3px;
  background: #ffffff;
  border-radius: 50%;
  transition: 0.15s ease;
}

.toggle-track input:checked + .toggle-slider {
  background: var(--pact-primary);
}

.toggle-track input:checked + .toggle-slider::before {
  transform: translateX(14px);
}

/* Buttons */
.btn-tactile {
  font-family: var(--font-sans);
  font-size: 0.78rem;
  font-weight: 600;
  padding: 0.42rem 0.9rem;
  border-radius: var(--radius-sm);
  border: 1px solid var(--pact-border);
  background: var(--pact-surface);
  color: var(--pact-text);
  box-shadow: var(--shadow-subtle);
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  transition: 0.15s ease;
  text-decoration: none;
}

.btn-tactile:hover {
  background: var(--pact-accent);
  border-color: #D8C7AA;
  color: var(--pact-text);
}

.btn-primary {
  background: var(--pact-primary) !important;
  border-color: var(--pact-primary) !important;
  color: #ffffff !important;
}

.btn-primary:hover {
  background: var(--pact-primary-dark) !important;
  border-color: var(--pact-primary-dark) !important;
}

.btn-success {
  background: #1E7E34 !important;
  border-color: #1E7E34 !important;
  color: #ffffff !important;
}

.btn-danger {
  background: var(--pact-primary) !important;
  border-color: var(--pact-primary) !important;
  color: #ffffff !important;
}

/* Main Layout Container */
.bento-container {
  max-width: 1680px;
  margin: 0 auto;
  padding: 1.5rem 1.75rem;
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
  width: 100%;
}

/* Hero Telemetry Cards */
.hero-telemetry-matrix {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
}

.telemetry-card {
  background: var(--pact-surface);
  border: 1px solid var(--pact-border);
  border-radius: var(--radius-lg);
  padding: 1.15rem 1.35rem;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  box-shadow: var(--shadow-subtle);
  transition: transform 0.15s ease, background-color 0.15s ease;
}

.telemetry-card:hover {
  background: var(--pact-surface-elevated);
}

.telemetry-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.telemetry-title {
  font-family: var(--font-sans);
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.02em;
  text-transform: uppercase;
  color: var(--pact-muted);
}

.telemetry-code {
  font-family: var(--font-mono);
  font-size: 0.65rem;
  font-weight: 600;
  color: var(--pact-muted);
  background: var(--pact-accent);
  padding: 2px 6px;
  border-radius: 4px;
}

.telemetry-value-wrap {
  display: flex;
  align-items: baseline;
  gap: 0.45rem;
  margin-top: 0.65rem;
}

.telemetry-num {
  font-family: var(--font-sans);
  font-size: 2.1rem;
  font-weight: 800;
  letter-spacing: -0.03em;
  line-height: 1;
  color: var(--pact-text) !important;
}

.telemetry-sub {
  font-family: var(--font-sans);
  font-size: 0.72rem;
  font-weight: 600;
  color: var(--pact-muted);
}

/* Bento Cards & Panels */
.bento-workspace {
  display: grid;
  grid-template-columns: 1.15fr 0.85fr;
  gap: 1.25rem;
}

@media (max-width: 1280px) {
  .bento-workspace {
    grid-template-columns: 1fr;
  }
}

.bento-card {
  background: var(--pact-surface);
  border: 1px solid var(--pact-border);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-subtle);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.bento-card-header {
  height: 48px;
  padding: 0 1.25rem;
  background: var(--pact-accent);
  border-bottom: 1px solid var(--pact-border);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.bento-title-group {
  display: flex;
  align-items: center;
  gap: 0.6rem;
}

.bento-title {
  font-family: var(--font-sans);
  font-size: 0.85rem;
  font-weight: 700;
  color: var(--pact-text);
  display: flex;
  align-items: center;
  gap: 0.4rem;
}

.bento-badge {
  font-family: var(--font-mono);
  font-size: 0.68rem;
  font-weight: 700;
  color: var(--pact-text);
  padding: 3px 8px;
  background: #ffffff;
  border: 1px solid var(--pact-border);
  border-radius: var(--radius-sm);
}

.bento-body {
  padding: 1.25rem;
  display: flex;
  flex-direction: column;
  gap: 1.15rem;
}

/* 11-Stage Connected Rail */
.pipeline-rail {
  display: grid;
  grid-template-columns: repeat(11, 1fr);
  gap: 4px;
  background: var(--pact-accent);
  padding: 4px;
  border-radius: var(--radius-md);
  border: 1px solid var(--pact-border);
}

.rail-node {
  font-family: var(--font-mono);
  font-size: 0.65rem;
  font-weight: 600;
  text-align: center;
  padding: 0.45rem 0.2rem;
  background: var(--pact-surface);
  color: var(--pact-muted);
  border: 1px solid var(--pact-border);
  border-radius: var(--radius-sm);
  transition: 0.15s ease;
  user-select: none;
}

.rail-node.active {
  background: var(--pact-primary);
  color: #ffffff;
  border-color: var(--pact-primary);
  font-weight: 700;
}

/* Terminal Viewport Deck */
.terminal-deck {
  display: flex;
  flex-direction: column;
  gap: 0.45rem;
}

.deck-label {
  font-family: var(--font-sans);
  font-size: 0.75rem;
  font-weight: 700;
  color: var(--pact-text-secondary);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.deck-label span:last-child {
  color: var(--pact-muted) !important;
  font-family: var(--font-mono);
  font-size: 0.65rem;
  font-weight: 600;
}

.terminal-viewport {
  background: #ffffff;
  border: 1px solid var(--pact-border);
  border-radius: var(--radius-md);
  padding: 1rem;
  height: 250px;
  overflow-y: auto;
  font-family: var(--font-mono);
  font-size: 0.78rem;
  line-height: 1.65;
  color: var(--pact-text);
  white-space: pre-wrap;
  word-break: break-word;
}

.terminal-viewport::-webkit-scrollbar {
  width: 6px;
}
.terminal-viewport::-webkit-scrollbar-track {
  background: var(--pact-surface);
}
.terminal-viewport::-webkit-scrollbar-thumb {
  background: var(--pact-border);
  border-radius: 3px;
}

/* Capacity & Debate Cards */
.capacity-feed-deck {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  max-height: 190px;
  overflow-y: auto;
}

.capacity-node {
  background: #ffffff;
  border: 1px solid var(--pact-border);
  border-left: 4px solid var(--pact-primary);
  border-radius: var(--radius-md);
  padding: 0.75rem 0.95rem;
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
  font-size: 0.78rem;
  transition: 0.15s ease;
}

.capacity-node:hover {
  background: var(--pact-surface-elevated);
}

.capacity-node-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.capacity-node-name {
  font-weight: 700;
  color: var(--pact-text);
  font-size: 0.82rem;
}

.capacity-node-role {
  font-family: var(--font-mono);
  font-size: 0.65rem;
  font-weight: 700;
  color: var(--pact-muted);
  padding: 2px 7px;
  background: var(--pact-accent);
  border: 1px solid var(--pact-border);
  border-radius: var(--radius-sm);
}

.capacity-node-body {
  color: var(--pact-text-secondary);
  font-size: 0.75rem;
  line-height: 1.5;
}

/* 3-Option Comparative Solver Deck */
.solver-deck {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 0.75rem;
}

.solver-option-card {
  background: #ffffff;
  border: 1px solid var(--pact-border);
  border-radius: var(--radius-md);
  padding: 0.9rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  cursor: pointer;
  transition: 0.15s ease;
}

.solver-option-card:hover {
  background: var(--pact-surface-elevated);
  border-color: #D8C7AA;
}

.solver-option-card.selected {
  background: var(--pact-accent);
  border: 1.5px solid var(--pact-primary);
}

.solver-card-header {
  font-size: 0.8rem;
  font-weight: 700;
  color: var(--pact-text);
}

.solver-metrics-row {
  display: flex;
  justify-content: space-between;
  font-family: var(--font-mono);
  font-size: 0.68rem;
  color: var(--pact-muted);
}

.solver-track {
  height: 6px;
  background: var(--pact-surface);
  border-radius: 3px;
  overflow: hidden;
}

.solver-fill {
  height: 100%;
  background: var(--pact-primary);
  border-radius: 3px;
  transition: width 400ms ease;
}

/* Review Gate Action Bar */
.review-gate-bar {
  background: var(--status-amber-bg);
  border: 1.5px solid var(--status-amber-border);
  border-left: 5px solid var(--status-amber-text);
  border-radius: var(--radius-md);
  padding: 0.85rem 1.15rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.gate-info h4 {
  font-size: 0.85rem;
  font-weight: 700;
  color: var(--status-amber-text);
}

.gate-info p {
  font-size: 0.72rem;
  color: var(--pact-text-secondary);
}

/* Outbound ACK Banner */
.ack-deck-banner {
  font-family: var(--font-mono);
  font-size: 0.75rem;
  font-weight: 600;
  padding: 0.75rem 1rem;
  background: var(--status-green-bg);
  border: 1px solid var(--status-green-border);
  border-left: 5px solid var(--status-green-text);
  border-radius: var(--radius-md);
  color: var(--status-green-text);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

/* Map Canvas */
.map-canvas-container {
  height: 480px;
  width: 100%;
  background: var(--pact-accent);
}

/* NOC Grid Cells */
.noc-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.75rem;
}

.noc-cell {
  background: #ffffff;
  border: 1px solid var(--pact-border);
  border-radius: var(--radius-md);
  padding: 0.8rem 1rem;
}

.noc-cell-label {
  font-family: var(--font-sans);
  font-size: 0.65rem;
  font-weight: 700;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  color: var(--pact-muted);
}

.noc-cell-value {
  font-size: 0.85rem;
  font-weight: 700;
  color: var(--pact-text) !important;
  margin-top: 4px;
}

/* Tables */
.table-responsive {
  overflow-x: auto;
}

table.tactile-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.78rem;
  text-align: left;
  background: var(--pact-surface);
}

table.tactile-table th {
  font-family: var(--font-sans);
  font-size: 0.68rem;
  font-weight: 700;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  color: var(--pact-muted);
  padding: 0.75rem 1rem;
  background: var(--pact-accent);
  border-bottom: 1px solid var(--pact-border);
}

table.tactile-table td {
  padding: 0.65rem 1rem;
  border-bottom: 1px solid rgba(120, 85, 40, 0.08);
  color: var(--pact-text-secondary);
  transition: 0.15s ease;
}

table.tactile-table tr:hover td {
  background: rgba(255, 229, 191, 0.45);
  color: var(--pact-text);
}

/* Badges */
.hud-tag {
  display: inline-block;
  font-family: var(--font-sans);
  font-size: 0.65rem;
  font-weight: 700;
  letter-spacing: 0.02em;
  padding: 3px 9px;
  border-radius: var(--radius-sm);
  text-transform: uppercase;
}

.hud-tag-critical {
  background: var(--status-red-bg);
  border: 1px solid var(--status-red-border);
  color: var(--status-red-text);
}

.hud-tag-high {
  background: #FFF0D4;
  border: 1px solid #FCD289;
  color: #9E5B00;
}

.hud-tag-success {
  background: var(--status-green-bg);
  border: 1px solid var(--status-green-border);
  color: var(--status-green-text);
}

.hud-tag-info {
  background: var(--status-blue-bg);
  border: 1px solid var(--status-blue-border);
  color: var(--status-blue-text);
}

/* Persona Switcher Box */
.persona-switcher-box {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: var(--pact-accent);
  border: 1px solid var(--pact-border);
  border-radius: var(--radius-sm);
  padding: 0.2rem 0.6rem;
}

.persona-label {
  font-family: var(--font-sans);
  font-size: 0.65rem;
  font-weight: 700;
  color: var(--pact-muted);
  letter-spacing: 0.04em;
}

.persona-dropdown {
  background: transparent;
  border: none;
  color: var(--pact-text);
  font-family: var(--font-sans);
  font-size: 0.78rem;
  font-weight: 600;
  cursor: pointer;
  outline: none;
  padding-right: 0.5rem;
}

.persona-dropdown option {
  background: var(--pact-surface);
  color: var(--pact-text);
  font-size: 0.8rem;
}

/* Active Persona Banner */
.persona-active-banner {
  background: var(--pact-surface);
  border: 1.5px solid var(--pact-border);
  border-left: 5px solid var(--pact-primary);
  border-radius: var(--radius-lg);
  padding: 0.9rem 1.25rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: var(--shadow-subtle);
}

/* Modal Dialog */
.modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(43, 33, 25, 0.45);
  backdrop-filter: blur(2px);
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1.5rem;
}

.modal-card {
  background: var(--pact-surface);
  border: 1px solid var(--pact-border);
  border-radius: var(--radius-lg);
  box-shadow: 0 16px 32px rgba(43, 33, 25, 0.15);
  width: 100%;
  max-width: 820px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.modal-header {
  padding: 1.1rem 1.4rem;
  background: var(--pact-accent);
  border-bottom: 1px solid var(--pact-border);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.modal-body {
  padding: 1.4rem;
}

.modal-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.25rem;
}

@media (max-width: 768px) {
  .modal-grid {
    grid-template-columns: 1fr;
  }
}

.modal-stat-box {
  background: #ffffff;
  border: 1px solid var(--pact-border);
  border-radius: var(--radius-md);
  padding: 0.75rem 1rem;
}

.modal-stat-label {
  font-family: var(--font-sans);
  font-size: 0.65rem;
  font-weight: 700;
  color: var(--pact-muted);
  letter-spacing: 0.04em;
  text-transform: uppercase;
}

.modal-stat-val {
  font-size: 0.85rem;
  font-weight: 700;
  color: var(--pact-text);
  margin-top: 4px;
}

.modal-footer {
  padding: 1rem 1.4rem;
  background: var(--pact-accent);
  border-top: 1px solid var(--pact-border);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

/* Leaflet Popup Overrides */
.leaflet-container {
  background: var(--pact-accent) !important;
  font-family: var(--font-sans) !important;
}

.pact-dark-popup .leaflet-popup-content-wrapper {
  background: var(--pact-surface) !important;
  border: 1px solid var(--pact-border) !important;
  border-radius: var(--radius-md) !important;
  box-shadow: var(--shadow-card) !important;
  padding: 2px !important;
  color: var(--pact-text) !important;
}

.pact-dark-popup .leaflet-popup-tip {
  background: var(--pact-surface) !important;
}

.pact-tooltip {
  background: var(--pact-surface) !important;
  border: 1px solid var(--pact-border) !important;
  color: var(--pact-text) !important;
  font-family: var(--font-mono) !important;
  font-size: 0.68rem !important;
  font-weight: 700 !important;
  border-radius: var(--radius-sm) !important;
  padding: 4px 8px !important;
  box-shadow: var(--shadow-subtle) !important;
}
```

---

<a id="file-app-static-js-map-js"></a>
## File: `app/static/js/map.js`

```javascript
/**
 * PACT Geospatial Visualization Engine (OpenStreetMap / Leaflet).
 * Renders multi-tiered disaster spatial layers:
 *  - Provider stockpiles & relief depots
 *  - Victim SOS coordinates (unmasked or 2km zero-knowledge grid)
 *  - Cascading $geoNear search radiuses & route trajectories
 */

class CrisisMap {
  constructor(containerId = "crisisMapContainer") {
    this.containerId = containerId;
    this.map = null;
    this.depotLayer = null;
    this.victimLayer = null;
    this.searchRingsLayer = null;
    this.routeLayer = null;
    this.depots = [];

    this.initMap();
  }

  initMap() {
    if (typeof L === "undefined") {
      console.warn("Leaflet not loaded yet. Map initialization deferred.");
      return;
    }

    const elem = document.getElementById(this.containerId);
    if (!elem) {
      console.error(`Map container #${this.containerId} not found.`);
      return;
    }

    // Default center on Tamil Nadu (Chennai corridor)
    const defaultCenter = [13.0827, 80.2707];

    this.map = L.map(this.containerId, {
      center: defaultCenter,
      zoom: 11,
      zoomControl: true,
      attributionControl: false
    });

    // Clean OpenStreetMap default tiles
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 18,
      attribution: '© OpenStreetMap contributors'
    }).addTo(this.map);

    // Initialize dedicated layer groups
    this.searchRingsLayer = L.layerGroup().addTo(this.map);
    this.routeLayer = L.layerGroup().addTo(this.map);
    this.depotLayer = L.layerGroup().addTo(this.map);
    this.victimLayer = L.layerGroup().addTo(this.map);

    console.log("[MAP] PACT OpenStreetMap Engine initialized.");
  }

  /**
   * Updates map view center & zoom.
   */
  setCenter(lat, lon, zoom = 12) {
    if (this.map) {
      this.map.setView([lat, lon], zoom);
    }
  }

  /**
   * Sets & renders provider relief depots.
   */
  setDepots(depotsList) {
    if (!this.map || !this.depotLayer) return;
    this.depotLayer.clearLayers();
    this.depots = depotsList;

    depotsList.forEach(d => {
      const loc = d.loc || d.location || {};
      const coords = loc.coordinates || [80.2707, 13.0827];
      const lon = coords[0];
      const lat = coords[1];
      const name = d.provider_name || d.name || "Relief Depot";
      const pid = d.provider_id || "DEPOT";
      const inventory = d.inventory || {};

      let badgeLabel = "DEPOT";
      let borderColor = "#6B5D4F";
      if (pid.includes("HOSPITAL") || pid.includes("MEDICAL")) {
        badgeLabel = "MED";
        borderColor = "#F62440";
      } else if (pid.includes("NGO") || pid.includes("ALPHA")) {
        badgeLabel = "NGO";
        borderColor = "#196D34";
      } else if (pid.includes("NDRF") || pid.includes("RESCUE")) {
        badgeLabel = "DRF";
        borderColor = "#8A5B07";
      } else if (pid.includes("CSR")) {
        badgeLabel = "CSR";
        borderColor = "#175494";
      }

      const depotIcon = L.divIcon({
        className: 'custom-depot-marker',
        html: `
          <div style="
            background: #FFF2DB;
            border: 2px solid ${borderColor};
            border-radius: 6px;
            width: 32px;
            height: 24px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 10px;
            font-weight: 700;
            color: #2B2119;
            box-shadow: 0 1px 3px rgba(43,33,25,0.15);
            cursor: pointer;
          ">${badgeLabel}</div>
        `,
        iconSize: [32, 24],
        iconAnchor: [16, 12]
      });

      const itemsList = Object.entries(inventory)
        .map(([k, v]) => `<div style="display:flex; justify-content:space-between; font-family:var(--font-mono); font-size:10px; color:#6B5D4F; padding:2px 0; border-bottom:1px solid #EBDDC0;"><span>${k.replace('_', ' ').toUpperCase()}</span><strong style="color:#2B2119">${v}</strong></div>`)
        .join('');

      const popupContent = `
        <div style="font-family:var(--font-sans); font-size:11px; color:#2B2119; min-width:200px; padding:4px;">
          <div style="font-weight:700; color:${borderColor}; font-size:12px; margin-bottom:2px;">[${badgeLabel}] ${name}</div>
          <div style="font-family:var(--font-mono); font-size:9px; color:#6B5D4F; margin-bottom:8px;">ID: ${pid} · [${lat.toFixed(4)}, ${lon.toFixed(4)}]</div>
          <div style="font-family:var(--font-sans); font-size:10px; font-weight:700; color:#2B2119; margin-bottom:4px; text-transform:uppercase;">Stockpiled Reserves</div>
          <div style="display:flex; flex-direction:column;">
            ${itemsList || '<span style="color:#6B5D4F">Active supplies</span>'}
          </div>
        </div>
      `;

      const marker = L.marker([lat, lon], { icon: depotIcon })
        .bindPopup(popupContent, { className: 'pact-dark-popup' });

      this.depotLayer.addLayer(marker);
    });
  }

  /**
   * Adds an emergency victim SOS marker.
   */
  addVictim(lat, lon, uid = "SOS", situation = "Emergency", isMasked = false) {
    if (!this.map || !this.victimLayer) return;

    const label = isMasked ? `GRID: ${uid}` : uid;

    const victimIcon = L.divIcon({
      className: 'custom-victim-marker',
      html: `
        <div style="
          background: #F62440;
          border: 2px solid #ffffff;
          border-radius: 4px;
          width: 32px;
          height: 22px;
          display: flex;
          align-items: center;
          justify-content: center;
          font-size: 9px;
          font-weight: 800;
          color: #ffffff;
          box-shadow: 0 2px 6px rgba(246,36,64,0.4);
          cursor: pointer;
        ">${label.substring(0, 4)}</div>
      `,
      iconSize: [32, 22],
      iconAnchor: [16, 11]
    });

    const popupContent = `
      <div style="font-family:var(--font-sans); font-size:11px; color:#2B2119; min-width:180px; padding:4px;">
        <div style="font-weight:700; color:#F62440; font-size:12px; margin-bottom:2px;">Target Incident: ${uid}</div>
        <div style="font-size:10px; color:#6B5D4F; margin-bottom:4px;">Type: ${situation}</div>
        <div style="font-family:var(--font-mono); font-size:9px; color:#6B5D4F; margin-bottom:6px;">GPS: [${lat.toFixed(4)}, ${lon.toFixed(4)}]</div>
        <div style="font-size:9px; font-weight:600; color:${isMasked ? '#8A5B07' : '#196D34'};">
          ${isMasked ? 'Zero-Knowledge 2km Grid Mask Active' : 'Verified Exact Coordinates'}
        </div>
      </div>
    `;

    const marker = L.marker([lat, lon], { icon: victimIcon })
      .bindPopup(popupContent, { className: 'pact-dark-popup' })
      .addTo(this.victimLayer);

    marker.openPopup();
    this.map.panTo([lat, lon]);
  }

  /**
   * Visualizes expanding geospatial search rings.
   */
  triggerGeoSearch(lat, lon, maxRadiusKm = 25) {
    if (!this.map || !this.searchRingsLayer) return;
    this.searchRingsLayer.clearLayers();

    const radiuses = [maxRadiusKm * 0.4, maxRadiusKm * 0.7, maxRadiusKm];
    radiuses.forEach((rKm, idx) => {
      const circle = L.circle([lat, lon], {
        radius: rKm * 1000,
        color: '#F62440',
        weight: 1.5,
        fillColor: '#FFE5BF',
        fillOpacity: 0.08 + (idx * 0.04),
        dashArray: '4, 4'
      }).addTo(this.searchRingsLayer);

      circle.bindTooltip(`Tier ${idx + 1}: ${rKm.toFixed(0)} km search perimeter`, {
        permanent: false,
        direction: 'top',
        className: 'pact-tooltip'
      });
    });

    setTimeout(() => {
      if (this.searchRingsLayer) {
        this.searchRingsLayer.clearLayers();
      }
    }, 12000);
  }

  /**
   * Draws tactical dispatch routes between assigned depots and victim.
   */
  drawDispatchPlan(planAllocations, victimLat, victimLon) {
    if (!this.map || !this.routeLayer) return;
    this.routeLayer.clearLayers();

    planAllocations.forEach(alloc => {
      const pLat = alloc.provider_lat || (victimLat + (Math.random() * 0.06 - 0.03));
      const pLon = alloc.provider_lon || (victimLon + (Math.random() * 0.06 - 0.03));

      const polyline = L.polyline([[pLat, pLon], [victimLat, victimLon]], {
        color: '#F62440',
        weight: 3,
        opacity: 0.8,
        dashArray: '6, 6'
      }).addTo(this.routeLayer);

      polyline.bindTooltip(`ETA: ~${alloc.eta_hours || 1.0}h | Dist: ${alloc.distance_km || 12} km`, {
        permanent: true,
        direction: 'center',
        className: 'pact-tooltip'
      });
    });
  }

  clearVictims() {
    if (this.victimLayer) this.victimLayer.clearLayers();
    if (this.routeLayer) this.routeLayer.clearLayers();
    if (this.searchRingsLayer) this.searchRingsLayer.clearLayers();
  }
}
```

---

<a id="file-app-static-js-app-js"></a>
## File: `app/static/js/app.js`

```javascript
/**
 * PACT Admin Command Portal & Field Provider Portal.
 * Clean, professional humanitarian theme matching the PACT specification.
 * Zero emojis, clear contrast, readable tables, and focused routing maps.
 */

let socket = null;
let crisisMap = null;
let providerMap = null;
let modalMiniMap = null;
let currentRunId = null;
let activeDecisionId = null;
let accumulatedTokens = "";
let currentOrgPersona = "ADMIN_ALL";
let activeInspectedMatch = null;
let selectedProviderVictimMatch = null;

const PERSONA_CONFIGS = {
  "ADMIN_ALL": {
    name: "Global Incident Command (Admin)",
    subtitle: "Zero-Connectivity Resilience · Zero-Hallucination Solvers · Multi-Agent Negotiation"
  },
  "NGO_TN_RED_CROSS": {
    name: "Red Cross Tamil Nadu Relief Command",
    subtitle: "Field Operations Portal · Viewing only victims and relief supplies allocated to your organization."
  },
  "TNDRF_ARAKKONAM_CHENNAI": {
    name: "Tamil Nadu Disaster Response Force (TNDRF)",
    subtitle: "Field Operations Portal · Rapid flood rescue, boat allocations, and emergency extractions."
  },
  "HOSPITAL_CHENNAI_RGGGH": {
    name: "Rajiv Gandhi / Apollo Trauma Medical Center",
    subtitle: "Field Operations Portal · Critical casualty triage, trauma teams, and ALS ambulance routing."
  },
  "CSR_TATA_SOUTH_HUB": {
    name: "Tata / CSR Southern Disaster Logistics Hub",
    subtitle: "Field Operations Portal · Regional bulk logistics, freight trucks, and generator reserves."
  },
  "COIMBATORE_GHAT_RESCUE": {
    name: "Nilgiris and Western Ghats Mountain Rescue Unit",
    subtitle: "Field Operations Portal · High-altitude 4x4 vehicles, landslide response, and mountain aid."
  }
};

document.addEventListener("DOMContentLoaded", () => {
  crisisMap = new CrisisMap("crisisMapContainer");
  initWebSocket();
  loadInitialData();
  setupEventListeners();
});

function initWebSocket() {
  const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
  const wsUrl = `${protocol}//${window.location.host}/ws/agents`;

  socket = new WebSocket(wsUrl);

  socket.onopen = () => {
    updateWsStatus(true);
    console.log("[WS] Connected to PACT live agent bus");
  };

  socket.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data);
      handleAgentEvent(data);
    } catch (e) {
      console.error("[WS] Parse error:", e);
    }
  };

  socket.onclose = () => {
    updateWsStatus(false);
    console.log("[WS] Disconnected. Reconnecting in 2s...");
    setTimeout(initWebSocket, 2000);
  };
}

function updateWsStatus(connected) {
  const pill = document.getElementById("wsStatusPill");
  const text = document.getElementById("wsStatusText");
  if (pill && text) {
    if (connected) {
      pill.className = "hud-pill connected";
      text.textContent = "AGENT BUS ONLINE";
    } else {
      pill.className = "hud-pill disconnected";
      text.textContent = "RECONNECTING...";
    }
  }
}

function handleAgentEvent(evt) {
  const type = evt.type;
  const agent = evt.agent;
  const payload = evt.payload || {};
  const runId = evt.run_id;

  // If in Provider Portal mode, update live matches table quietly
  if (currentOrgPersona !== "ADMIN_ALL") {
    if (type === "match.committed" || type === "run.completed") {
      loadProviderPortalData(currentOrgPersona);
    }
    return;
  }

  // ── ADMIN VIEW EVENT HANDLERS ─────────────────────────────────────────────

  // 1. Run Started
  if (type === "run.started") {
    currentRunId = runId;
    accumulatedTokens = "";
    resetPipelineStepper();
    clearDebateFeed();
    document.getElementById("streamContent").textContent = "";
    document.getElementById("ackFrameBox").style.display = "none";
    document.getElementById("adminActionBar").style.display = "none";
    updateActiveRunBadge(runId);
  }

  // 2. Agent Entered
  if (type === "agent.entered") {
    const stage = payload.stage || agent;
    highlightStepperStage(stage);
    const streamElem = document.getElementById("streamContent");
    if (streamElem) {
      let stageDesc = "";
      if (stage === "A0") stageDesc = " [Deterministic] Frame parsing and 2-char XOR checksum verification";
      else if (stage === "A1") stageDesc = " [Deterministic] Compound deduplication check on (UID, SEQ)";
      else if (stage === "A2") stageDesc = " [Tool-Augmented LLM] Situational triage and meteorological hazard evaluation";
      else if (stage === "A3") stageDesc = " [MongoDB] Cascading $geoNear spatial candidate radius lookup";
      else if (stage === "A4") stageDesc = " [Multi-Agent Negotiation] Independent provider advocates debating deployment bids";
      else if (stage === "A5") stageDesc = " [Python Math Solver] Linear greedy optimization of 3 plans";
      else if (stage === "A6") stageDesc = " [Groq LLM Arbiter] Judging debate arguments and choosing optimal plan";
      else if (stage === "A7") stageDesc = " [Privacy] Zero-knowledge 2km grid masking and hashing";
      else if (stage === "A8") stageDesc = " [Human-in-the-Loop] Dispatcher review gate and Autopilot timer";
      else if (stage === "A9") stageDesc = " [Groq LLM] Plain-English operational bulletin generation";
      else if (stage === "A10") stageDesc = " [Database] Stock deduction and Outbound SMS frame generation";

      accumulatedTokens += `\n\n[${stage} AGENT ENTERED]${stageDesc}:\n`;
      streamElem.textContent = accumulatedTokens;
      streamElem.scrollTop = streamElem.scrollHeight;
    }
  }

  // 3. Tool Execution Event
  if (type === "agent.tool_called") {
    const streamElem = document.getElementById("streamContent");
    if (streamElem) {
      const summary = payload.summary || `Executed tool ${payload.tool_name}`;
      accumulatedTokens += `  [EXECUTED TOOL: ${payload.tool_name}]: ${summary}\n`;
      streamElem.textContent = accumulatedTokens;
      streamElem.scrollTop = streamElem.scrollHeight;
    }
  }

  // 4. Token Streaming
  if (type === "agent.token") {
    const token = payload.token || "";
    accumulatedTokens += token;
    const streamElem = document.getElementById("streamContent");
    if (streamElem) {
      streamElem.textContent = accumulatedTokens;
      streamElem.scrollTop = streamElem.scrollHeight;
    }
  }

  // 5. Debate Turn
  if (type === "debate.turn") {
    appendDebateCard(payload);
  }

  // 6. Solver Options
  if (type === "solver.computed") {
    renderSolverCards(payload.options || {});
  }

  // 7. Decision Proposed
  if (type === "decision.proposed") {
    selectSolverCard(payload.selected_option_id);
  }

  // 8. Admin Gate Required
  if (type === "admin.gate_required") {
    activeDecisionId = payload.decision_id || "DEC_TEMP";
    showAdminGateAction(payload);
  }

  // 9. Match Committed
  if (type === "match.committed") {
    loadMatchesTable();
    loadOffersTable();
    refreshStats();
  }

  // 10. Frame Transmitted
  if (type === "frame.transmitted") {
    showAckBanner(payload.raw_frame || "");
  }

  // 11. Run Completed
  if (type === "run.completed") {
    completePipelineStepper();
    updateActiveRunBadge("STANDBY", false);
    refreshStats();
    loadRequestsTable();
  }
}

// ── Persona & Portal Switching Logic ──────────────────────────────────────────

function onOrgPersonaChanged() {
  const select = document.getElementById("orgPersonaSelect");
  if (!select) return;
  currentOrgPersona = select.value;

  const adminView = document.getElementById("adminViewContainer");
  const providerView = document.getElementById("providerViewContainer");
  const autopilotWrap = document.getElementById("adminAutopilotWrap");
  const headerTitle = document.getElementById("headerTitle");
  const headerSubtitle = document.getElementById("headerSubtitle");

  const config = PERSONA_CONFIGS[currentOrgPersona] || PERSONA_CONFIGS["ADMIN_ALL"];

  if (currentOrgPersona === "ADMIN_ALL") {
    if (adminView) adminView.style.display = "flex";
    if (providerView) providerView.style.display = "none";
    if (autopilotWrap) autopilotWrap.style.display = "flex";
    if (headerTitle) headerTitle.textContent = "Autonomous Crisis Coordination Center";
    if (headerSubtitle) headerSubtitle.textContent = config.subtitle;

    loadInitialData();
  } else {
    if (adminView) adminView.style.display = "none";
    if (providerView) providerView.style.display = "flex";
    if (autopilotWrap) autopilotWrap.style.display = "none";
    if (headerTitle) headerTitle.textContent = config.name;
    if (headerSubtitle) headerSubtitle.textContent = config.subtitle;

    document.getElementById("pOrgTitle").textContent = config.name;
    document.getElementById("pOrgSubtitle").textContent = config.subtitle;

    loadProviderPortalData(currentOrgPersona);
  }
}

function resetToAdminView() {
  const select = document.getElementById("orgPersonaSelect");
  if (select) {
    select.value = "ADMIN_ALL";
    onOrgPersonaChanged();
  }
}

// ── Field Organization Portal Data Loading ───────────────────────────────────

async function loadProviderPortalData(providerId) {
  try {
    const offerRes = await fetch(`/api/v1/offers/${providerId}`);
    let providerData = {};
    if (offerRes.ok) {
      providerData = await offerRes.json();
    }

    document.getElementById("pStatBase").textContent = providerData.location_name || "Chennai Hub";
    document.getElementById("pStatFleet").textContent = providerData.fleet_description || "Ready Fleet";
    document.getElementById("providerFleetText").textContent = `Fleet Readiness: ${providerData.fleet_description || 'Standard response vehicles ready'}`;

    const stockGrid = document.getElementById("providerStockGrid");
    if (stockGrid) {
      stockGrid.innerHTML = "";
      const inv = providerData.inventory || {};
      Object.entries(inv).forEach(([itemKey, qty]) => {
        const itemBox = document.createElement("div");
        itemBox.className = "modal-stat-box";
        itemBox.innerHTML = `
          <div class="modal-stat-label">${itemKey.replace('_', ' ').toUpperCase()}</div>
          <div class="modal-stat-val" style="font-size:1.1rem; color:var(--pact-primary);">${qty}</div>
        `;
        stockGrid.appendChild(itemBox);
      });
    }

    const matchRes = await fetch(`/api/v1/matches?provider_id=${providerId}&limit=20`);
    const matchData = await matchRes.json();
    const matches = matchData.matches || [];

    document.getElementById("pStatMissions").textContent = matches.length;
    document.getElementById("pQueueCount").textContent = `${matches.length} ASSIGNED`;

    let totalUnits = 0;
    matches.forEach(m => {
      const items = m.items || m.allocated_items || (m.selected_plan?.allocations?.[0]?.items) || {};
      Object.values(items).forEach(val => {
        if (typeof val === "number") totalUnits += val;
      });
    });
    document.getElementById("pStatSupplies").textContent = `${totalUnits} Units`;

    const tbody = document.getElementById("providerMatchesTableBody");
    if (tbody) {
      tbody.innerHTML = "";
      if (matches.length === 0) {
        tbody.innerHTML = `<tr><td colspan="5" style="text-align:center; padding:1.5rem; color:var(--pact-muted);">No help seekers currently assigned to this unit. Standing by for incoming SOS.</td></tr>`;
      } else {
        matches.forEach((m, idx) => {
          const tr = document.createElement("tr");
          tr.style.cursor = "pointer";
          tr.onclick = () => selectProviderVictim(m);

          const items = m.items || m.allocated_items || (m.selected_plan?.allocations?.[0]?.items) || {};
          const itemsStr = Object.entries(items).map(([k, v]) => `${v} ${k.replace('_kits', '')}`).join(", ") || "Aid Pack";

          tr.innerHTML = `
            <td><strong style="font-family:var(--font-mono); color:var(--pact-primary);">${m.uid || 'CIT01'}</strong></td>
            <td><strong>${m.situation || 'Crisis Incident'}</strong></td>
            <td>${m.headcount || '1 person'}</td>
            <td><span class="hud-tag hud-tag-info" style="font-size:0.7rem;">${itemsStr}</span></td>
            <td>
              <button class="btn-tactile" style="padding:0.25rem 0.6rem; font-size:0.68rem;" onclick="event.stopPropagation(); selectProviderVictim(m)">
                Inspect Route
              </button>
            </td>
          `;
          tbody.appendChild(tr);

          if (idx === 0 && !selectedProviderVictimMatch) {
            selectProviderVictim(m);
          }
        });
      }
    }

    initProviderMap(providerData, matches);

  } catch (e) {
    console.error("Failed to load provider portal data:", e);
  }
}

function selectProviderVictim(match) {
  selectedProviderVictimMatch = match;

  const cardTitle = document.getElementById("pCardTitle");
  const badge = document.getElementById("pCardStatusBadge");
  const incident = document.getElementById("pDetailIncident");
  const itemsEl = document.getElementById("pDetailItems");
  const etaEl = document.getElementById("pDetailETA");
  const coordsEl = document.getElementById("pDetailCoords");

  if (cardTitle) cardTitle.textContent = `Mission: Target ${match.uid || 'Citizen'} · Plan ${match.match_id || ''}`;
  if (badge) {
    badge.className = "hud-tag hud-tag-success";
    badge.textContent = "ASSIGNED TO YOU";
  }

  const items = match.items || match.allocated_items || (match.selected_plan?.allocations?.[0]?.items) || {};
  const itemsStr = Object.entries(items).map(([k, v]) => `• ${v} ${k.replace('_', ' ').toUpperCase()}`).join("\n") || "Emergency Aid Quota";

  if (incident) incident.textContent = `${match.situation || 'Flood and Entrapment'} (${match.headcount || '1 person'} affected · ${match.urgency || 'High'} Urgency)`;
  if (itemsEl) itemsEl.textContent = itemsStr;

  const dist = match.distance_km || match.selected_plan?.allocations?.[0]?.distance_km || 14.2;
  const eta = match.eta_hours || match.selected_plan?.allocations?.[0]?.eta_hours || 0.6;
  if (etaEl) etaEl.textContent = `${dist} km distance (Estimated Arrival: ~${eta} hours)`;

  const coords = match.request_geo?.coordinates || [80.00557, 13.00835];
  const pack10 = match.request_geo?.pack10 || "COORDS";
  if (coordsEl) coordsEl.textContent = `[Lat: ${coords[1].toFixed(5)}, Lon: ${coords[0].toFixed(5)}] · PACK10: ${pack10}`;

  if (providerMap) {
    providerMap.flyTo([coords[1], coords[0]], 13, { animate: true, duration: 0.8 });
  }
}

function initProviderMap(providerData, matches) {
  const container = document.getElementById("providerMapContainer");
  if (!container || typeof L === "undefined") return;

  const depotCoords = providerData.loc?.coordinates || [80.2609, 13.0732];
  const depotLat = depotCoords[1];
  const depotLon = depotCoords[0];

  if (!providerMap) {
    providerMap = L.map("providerMapContainer", {
      center: [depotLat, depotLon],
      zoom: 12,
      zoomControl: true,
      attributionControl: false
    });
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { maxZoom: 18 }).addTo(providerMap);
  } else {
    providerMap.setView([depotLat, depotLon], 12);
    providerMap.eachLayer((layer) => {
      if (layer instanceof L.Marker || layer instanceof L.Polyline) {
        providerMap.removeLayer(layer);
      }
    });
  }

  // Add organization main depot marker
  const depotIcon = L.divIcon({
    className: 'custom-depot-marker',
    html: `<div style="background:#FFF2DB; border:2px solid #F62440; border-radius:6px; width:34px; height:24px; display:flex; align-items:center; justify-content:center; font-size:10px; font-weight:700; color:#2B2119; box-shadow:0 1px 3px rgba(43,33,25,0.15);">BASE</div>`,
    iconSize: [34, 24],
    iconAnchor: [17, 12]
  });
  L.marker([depotLat, depotLon], { icon: depotIcon })
    .bindPopup(`<strong>${providerData.name || 'Your Depot'}</strong><br>${providerData.location_name || 'Operational Hub'}`)
    .addTo(providerMap);

  // Add assigned victim markers and draw dashed routes
  matches.forEach(m => {
    const coords = m.request_geo?.coordinates || [depotLon + 0.03, depotLat + 0.02];
    const victimLat = coords[1];
    const victimLon = coords[0];

    const victimIcon = L.divIcon({
      className: 'custom-victim-marker',
      html: `<div style="background:#F62440; border:2px solid #ffffff; border-radius:4px; width:28px; height:20px; display:flex; align-items:center; justify-content:center; font-size:9px; font-weight:800; color:#fff; box-shadow:0 2px 6px rgba(246,36,64,0.35);">SOS</div>`,
      iconSize: [28, 20],
      iconAnchor: [14, 10]
    });

    const marker = L.marker([victimLat, victimLon], { icon: victimIcon })
      .bindPopup(`<strong>Target: ${m.uid}</strong><br>Incident: ${m.situation || 'Crisis'}<br>Supplies: ${m.items || 'Aid'}`)
      .addTo(providerMap);

    marker.on('click', () => selectProviderVictim(m));

    L.polyline([[depotLat, depotLon], [victimLat, victimLon]], {
      color: '#F62440',
      weight: 3,
      dashArray: '6, 6',
      opacity: 0.8
    }).addTo(providerMap);
  });

  setTimeout(() => {
    if (providerMap) providerMap.invalidateSize();
  }, 250);
}

function confirmProviderDispatch() {
  if (!selectedProviderVictimMatch) {
    alert("Please select an assigned help seeker first.");
    return;
  }
  alert(`Dispatch Confirmed: Relief convoy mobilized from your depot for Target [${selectedProviderVictimMatch.uid}]. Live tracking active.`);
}

// ── Interactive Dispatch Detail Modal (Admin View) ────────────────────────────

async function inspectDispatch(matchId) {
  try {
    const res = await fetch(`/api/v1/matches/${matchId}`);
    if (!res.ok) return;
    const match = await res.json();
    activeInspectedMatch = match;

    const modal = document.getElementById("dispatchDetailModal");
    if (!modal) return;

    document.getElementById("modalPlanTitle").textContent = `Dispatch Plan: ${match.match_id || matchId}`;
    document.getElementById("modalPlanSubtitle").textContent = `Allocated to: ${match.provider_name || match.provider_id || 'Relief Agency'}`;
    document.getElementById("modalRecipient").textContent = `Target: ${match.uid || 'Citizen'} · ${match.situation || 'Emergency'}`;

    const items = match.items || match.allocated_items || (match.selected_plan?.allocations?.[0]?.items) || {};
    const itemsStr = Object.entries(items).map(([k, v]) => `${v} ${k.replace('_', ' ').toUpperCase()}`).join(", ") || "General Emergency Aid";
    document.getElementById("modalSupplies").textContent = itemsStr;

    const dist = match.distance_km || match.selected_plan?.allocations?.[0]?.distance_km || 12.5;
    const eta = match.eta_hours || match.selected_plan?.allocations?.[0]?.eta_hours || 0.5;
    document.getElementById("modalDepot").textContent = `${match.provider_name || match.provider_id || 'Relief Unit'} (${dist} km · ETA ~${eta}h)`;

    const coords = match.request_geo?.coordinates || [80.00557, 13.00835];
    const pack10 = match.request_geo?.pack10 || "COORDS";
    document.getElementById("modalCoords").textContent = `[Lat: ${coords[1].toFixed(5)}, Lon: ${coords[0].toFixed(5)}] · PACK10: ${pack10}`;

    modal.style.display = "flex";

    setTimeout(() => {
      renderModalMiniMap(coords[1], coords[0], match.provider_id);
    }, 150);

  } catch (e) {
    console.error("Inspect error:", e);
  }
}

function renderModalMiniMap(targetLat, targetLon, providerId) {
  const container = document.getElementById("modalMapCanvas");
  if (!container || typeof L === "undefined") return;

  if (!modalMiniMap) {
    modalMiniMap = L.map("modalMapCanvas", {
      center: [targetLat, targetLon],
      zoom: 13,
      zoomControl: false,
      attributionControl: false
    });
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { maxZoom: 18 }).addTo(modalMiniMap);
  } else {
    modalMiniMap.setView([targetLat, targetLon], 13);
    modalMiniMap.eachLayer((layer) => {
      if (layer instanceof L.Marker || layer instanceof L.Polyline) {
        modalMiniMap.removeLayer(layer);
      }
    });
  }

  const victimIcon = L.divIcon({
    className: 'custom-victim-marker',
    html: `<div style="background:#F62440; border:2px solid #ffffff; border-radius:4px; width:26px; height:20px; display:flex; align-items:center; justify-content:center; font-size:9px; font-weight:800; color:#fff;">SOS</div>`,
    iconSize: [26, 20],
    iconAnchor: [13, 10]
  });
  L.marker([targetLat, targetLon], { icon: victimIcon }).addTo(modalMiniMap);

  const depotLat = targetLat + 0.04;
  const depotLon = targetLon + 0.03;
  const depotIcon = L.divIcon({
    className: 'custom-depot-marker',
    html: `<div style="background:#FFF2DB; border:2px solid #2B2119; border-radius:4px; width:28px; height:20px; display:flex; align-items:center; justify-content:center; font-size:9px; font-weight:700;">BASE</div>`,
    iconSize: [28, 20],
    iconAnchor: [14, 10]
  });
  L.marker([depotLat, depotLon], { icon: depotIcon }).addTo(modalMiniMap);

  L.polyline([[depotLat, depotLon], [targetLat, targetLon]], {
    color: '#F62440',
    weight: 3,
    dashArray: '6, 6'
  }).addTo(modalMiniMap);

  modalMiniMap.invalidateSize();
}

function closeDispatchModal() {
  const modal = document.getElementById("dispatchDetailModal");
  if (modal) modal.style.display = "none";
}

function focusOnMainMap() {
  if (activeInspectedMatch && crisisMap) {
    const coords = activeInspectedMatch.request_geo?.coordinates || [80.00557, 13.00835];
    crisisMap.setCenter(coords[1], coords[0], 14);
    crisisMap.triggerGeoSearch(coords[1], coords[0], 15);
  }
  closeDispatchModal();
}

// ── Admin Stepper & Viewport Helpers ──────────────────────────────────────────

function resetPipelineStepper() {
  for (let i = 0; i <= 10; i++) {
    const el = document.getElementById(`step-A${i}`);
    if (el) el.className = "rail-node";
  }
}

function highlightStepperStage(stage) {
  const el = document.getElementById(`step-${stage}`);
  if (el) el.className = "rail-node active";
}

function completePipelineStepper() {
  for (let i = 0; i <= 10; i++) {
    const el = document.getElementById(`step-A${i}`);
    if (el) el.className = "rail-node";
  }
}

function updateActiveRunBadge(runId, active = true) {
  const badge = document.getElementById("activeRunBadge");
  if (badge) {
    if (active) {
      badge.textContent = `TRACE: ${runId.substring(0, 8)}... (LIVE)`;
      badge.style.color = "var(--pact-primary)";
    } else {
      badge.textContent = "TRACE: STANDBY";
      badge.style.color = "var(--pact-muted)";
    }
  }
}

function clearDebateFeed() {
  const feed = document.getElementById("debateFeed");
  if (feed) feed.innerHTML = "";
}

function appendDebateCard(turn) {
  const feed = document.getElementById("debateFeed");
  if (!feed) return;

  const card = document.createElement("div");
  card.className = "capacity-node";

  const speaker = turn.speaker || "Relief Advocate";
  const role = turn.role || turn.stance || "Advocate";
  const arg = turn.argument || "";

  card.innerHTML = `
    <div class="capacity-node-header">
      <span class="capacity-node-name">${speaker}</span>
      <span class="capacity-node-role">${role}</span>
    </div>
    <div class="capacity-node-body">${arg}</div>
  `;

  feed.appendChild(card);
  feed.scrollTop = feed.scrollHeight;
}

function renderSolverCards(options) {
  const grid = document.getElementById("solverOptionsGrid");
  if (!grid) return;
  grid.innerHTML = "";

  const order = ["fastest", "max_coverage", "least_depleting"];
  order.forEach((optId, idx) => {
    const opt = options[optId] || {};
    const title = opt.title || `[${idx + 1}] ${optId.replace('_', ' ').toUpperCase()}`;
    const cov = Math.round((opt.coverage_ratio || 1.0) * 100);
    const eta = opt.max_eta_hours || 1.0;

    const card = document.createElement("div");
    card.id = `solverCard-${optId}`;
    card.className = "solver-option-card";
    card.onclick = () => selectSolverCard(optId);

    card.innerHTML = `
      <div class="solver-card-header">${title}</div>
      <div class="solver-metrics-row">
        <span>COV: ${cov}%</span>
        <span>ETA: ~${eta}h</span>
      </div>
      <div class="solver-track">
        <div class="solver-fill" style="width: ${cov}%"></div>
      </div>
    `;
    grid.appendChild(card);
  });
}

function selectSolverCard(optionId) {
  const cards = document.querySelectorAll(".solver-option-card");
  cards.forEach(c => c.classList.remove("selected"));

  const target = document.getElementById(`solverCard-${optionId}`);
  if (target) target.classList.add("selected");
}

function showAdminGateAction(payload) {
  const bar = document.getElementById("adminActionBar");
  const title = document.getElementById("adminActionTitle");
  if (bar && title) {
    title.textContent = `Dispatcher Action Required: ${payload.reason || 'Approve Proposed Allocation'}`;
    bar.style.display = "flex";
  }
}

async function submitAdminDecision(action) {
  const bar = document.getElementById("adminActionBar");
  if (bar) bar.style.display = "none";

  try {
    await fetch("/api/v1/admin/gate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        decision_id: activeDecisionId,
        action: action === "approve" ? "approve" : "reject",
        user_id: "COMMANDER_DISPATCHER"
      })
    });
  } catch (e) {
    console.error("Admin gate error:", e);
  }
}

function showAckBanner(frame) {
  const box = document.getElementById("ackFrameBox");
  if (box) {
    box.textContent = `OUTBOUND CELLULAR ACK: ${frame}`;
    box.style.display = "flex";
  }
}

// ── Admin Initial Data Loaders ────────────────────────────────────────────────

async function loadInitialData() {
  await Promise.all([
    refreshStats(),
    loadOffersTable(),
    loadRequestsTable(),
    loadMatchesTable()
  ]);
}

async function refreshStats() {
  try {
    const res = await fetch("/api/v1/admin/stats");
    const data = await res.json();

    document.getElementById("statTotalRequests").textContent = data.total_requests || 0;
    document.getElementById("statActiveOffers").textContent = data.total_offers || 11;
    document.getElementById("statCommittedMatches").textContent = data.total_matches || 0;
    document.getElementById("statAgentEvents").textContent = data.total_events || 0;
  } catch (e) {
    console.error("Stats refresh error:", e);
  }
}

async function loadOffersTable() {
  try {
    const res = await fetch("/api/v1/offers?limit=15");
    const data = await res.json();

    if (crisisMap && data.offers) {
      crisisMap.setDepots(data.offers);
    }
  } catch (e) {
    console.error("Offers load error:", e);
  }
}

async function loadRequestsTable() {
  try {
    const res = await fetch("/api/v1/requests?limit=10");
    const data = await res.json();
    const tbody = document.getElementById("requestsTableBody");
    if (!tbody) return;
    tbody.innerHTML = "";

    data.requests.forEach(r => {
      const payload = r.payload || {};
      const uid = r.uid || "SOS";
      const sit = payload.situation?.name || "General Crisis";
      const urg = payload.urgency?.label || "Medium";
      let tagClass = "hud-tag-info";
      if (urg.toLowerCase() === "critical") tagClass = "hud-tag-critical";
      else if (urg.toLowerCase() === "high") tagClass = "hud-tag-high";

      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td><strong style="font-family:var(--font-mono); color:var(--pact-primary);">${uid}</strong></td>
        <td>${sit}</td>
        <td>${payload.people_estimate || 1} persons</td>
        <td><span class="hud-tag ${tagClass}">${urg}</span></td>
        <td style="font-family:var(--font-mono); font-size:0.7rem; color:var(--pact-muted);">${r.raw_frame || 'Q|...'}</td>
      `;
      tbody.appendChild(tr);
    });
  } catch (e) {
    console.error("Requests load error:", e);
  }
}

async function loadMatchesTable() {
  try {
    const res = await fetch("/api/v1/matches?limit=15");
    const data = await res.json();
    const tbody = document.getElementById("matchesTableBody");
    if (!tbody) return;
    tbody.innerHTML = "";

    data.matches.forEach(m => {
      const tr = document.createElement("tr");
      tr.style.cursor = "pointer";
      tr.onclick = () => inspectDispatch(m.match_id);

      tr.innerHTML = `
        <td><strong style="font-family:var(--font-mono); color:var(--status-green-text);">${m.match_id}</strong></td>
        <td style="font-family:var(--font-mono);">${m.uid || 'CIT00'}</td>
        <td>${m.selected_option_id || 'Depletion Balanced'}</td>
        <td><span class="hud-tag hud-tag-success">${m.status || 'Committed'}</span></td>
        <td>
          <button class="btn-tactile" style="padding:0.25rem 0.6rem; font-size:0.68rem;" onclick="event.stopPropagation(); inspectDispatch('${m.match_id}')">
            Inspect Route
          </button>
        </td>
      `;
      tbody.appendChild(tr);
    });
  } catch (e) {
    console.error("Matches load error:", e);
  }
}

function setupEventListeners() {
  const resetBtn = document.getElementById("btnResetSeed");
  if (resetBtn) {
    resetBtn.onclick = async () => {
      if (confirm("Reset and re-seed all relief provider inventory in database?")) {
        await fetch("/api/v1/admin/seed", { method: "POST" });
        loadInitialData();
      }
    };
  }

  const toggle = document.getElementById("autopilotToggle");
  if (toggle) {
    toggle.onchange = async () => {
      try {
        await fetch("/api/v1/admin/autopilot", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ enabled: toggle.checked, timeout_seconds: 3.0 })
        });
        refreshStats();
      } catch (e) {
        console.error("Autopilot error:", e);
      }
    };
  }
}
```

---

<a id="file-tests-test_codec-py"></a>
## File: `tests/test_codec.py`

```python
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
```

---

<a id="file-tests-test_pipeline-py"></a>
## File: `tests/test_pipeline.py`

```python
"""
Tests for Multi-Agent Reasoning Pipeline, Solver Arithmetic, and Firewall Boundaries.
"""

import pytest
import asyncio
from app.db.mongo import db_manager
from app.db.seed import seed_database
from app.agents.pipeline import pipeline
from app.agents.a5_solver import a5_solver
from app.agents.a6_arbiter import a6_arbiter
from app.agents.a7_redactor import a7_redactor
from app.agents.a8_admin_gate import a8_admin_gate


@pytest.mark.asyncio
async def test_solver_deterministic_math():
    demand = [
        {"resource_key": "food_kits", "quantity": 100},
        {"resource_key": "water_kits", "quantity": 250},
        {"resource_key": "medical_kits", "quantity": 10}
    ]
    candidates = [
        {
            "provider_id": "DEPOT_A",
            "provider_name": "Depot A (Close)",
            "distance_km": 2.0,
            "eta_hours": 0.5,
            "inventory": {"food_kits": 50, "water_kits": 100, "medical_kits": 20}
        },
        {
            "provider_id": "DEPOT_B",
            "provider_name": "Depot B (Large Hub)",
            "distance_km": 15.0,
            "eta_hours": 2.0,
            "inventory": {"food_kits": 500, "water_kits": 1000, "medical_kits": 5}
        }
    ]

    options = await a5_solver.solve(demand, candidates, run_id="test_run")

    assert "fastest" in options
    assert "max_coverage" in options
    assert "least_depleting" in options

    # Check fastest option allocates from closest first
    fastest = options["fastest"]
    assert fastest["coverage_ratio"] == 1.0
    alloc_a = [a for a in fastest["allocations"] if a["provider_id"] == "DEPOT_A"][0]
    assert alloc_a["items"]["food_kits"] == 50  # took all 50 available
    assert alloc_a["items"]["water_kits"] == 100
    assert alloc_a["items"]["medical_kits"] == 10

    # Ensure no allocated quantity exceeds inventory
    for opt_id, opt in options.items():
        for alloc in opt["allocations"]:
            p_id = alloc["provider_id"]
            cand_inv = [c["inventory"] for c in candidates if c["provider_id"] == p_id][0]
            for r_key, qty in alloc["items"].items():
                assert qty <= cand_inv[r_key], f"Allocated {qty} exceeds stock {cand_inv[r_key]}"


@pytest.mark.asyncio
async def test_arbiter_hallucination_firewall():
    options = {
        "fastest": {"option_id": "fastest", "title": "Fast Plan", "max_eta_hours": 1.0, "allocations": []},
        "max_coverage": {"option_id": "max_coverage", "title": "Max Plan", "max_eta_hours": 3.0, "allocations": []},
        "least_depleting": {"option_id": "least_depleting", "title": "Balanced Plan", "max_eta_hours": 2.0, "allocations": []}
    }
    triage = {"priority_level": "P1_CRITICAL", "risk_score": 9.5}
    debate = {"consensus_summary": "Urgent medical required"}

    res = await a6_arbiter.arbitrate(options, triage, debate, run_id="test_arbiter")
    chosen = res["decision"]["selected_option_id"]
    assert chosen in options, f"Selected option '{chosen}' is not in valid pre-solved set"


@pytest.mark.asyncio
async def test_privacy_redaction():
    req_data = {
        "uid": "7F3K",
        "sender": "+919876543210",
        "geo": {"latitude": 23.25991, "longitude": 77.41263}
    }
    plan = {"option_id": "fastest"}

    redacted = await a7_redactor.redact(req_data, plan, run_id="test_redactor")
    assert redacted["uid"] == "7F3K"
    assert redacted["masked_phone"] == "+91******3210"
    assert redacted["masked_coordinates"] == [77.41, 23.26]  # fuzzed


@pytest.mark.asyncio
async def test_full_pipeline_execution():
    await db_manager.connect()
    await seed_database(force=True)
    a8_admin_gate.set_autopilot(enabled=True, timeout_seconds=0.1)

    raw_sms = "Q|001|7F3K|15223C03Q0|6QR6VFBQ33|7F"
    result = await pipeline.run(raw_input=raw_sms, transport="sms", sender="+919876543210")

    assert result["status"] == "success"
    assert "match" in result
    match = result["match"]
    assert match["status"] == "committed"
    assert match["sms_ack_frame"].startswith("C|001|7F3K|")
    assert "OK" in match["sms_ack_frame"]
```

---

<a id="file-tests-test_api-py"></a>
## File: `tests/test_api.py`

```python
"""
API Endpoints Integration Tests for PACT Server.
"""

import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.db.mongo import db_manager
from app.db.seed import seed_database
from app.agents.a8_admin_gate import a8_admin_gate


@pytest.fixture(autouse=True)
async def setup_test_db():
    await db_manager.connect()
    await seed_database(force=True)
    a8_admin_gate.set_autopilot(enabled=True, timeout_seconds=0.1)


@pytest.mark.asyncio
async def test_api_health():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/api/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"


@pytest.mark.asyncio
async def test_api_pact_ingest():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        payload = {"text": "Q|001|7F3K|15223C03Q0|6QR6VFBQ33|7F", "transport": "http"}
        response = await ac.post("/api/v1/pact/ingest", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] in ("success", "duplicate")


@pytest.mark.asyncio
async def test_api_sms_webhook():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        form_data = {"Body": "Q|002|8M9L|15223C03Q0|6QR6VFBQ33|7F", "From": "+919876543210"}
        response = await ac.post("/api/v1/sms/webhook", data=form_data)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "received"


@pytest.mark.asyncio
async def test_api_admin_stats():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/api/v1/admin/stats")
        assert response.status_code == 200
        data = response.json()
        assert "metrics" in data
        assert data["status"] == "operational"


@pytest.mark.asyncio
async def test_api_presets():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/api/v1/sms/presets")
        assert response.status_code == 200
        data = response.json()
        assert len(data["presets"]) >= 5
```

---

