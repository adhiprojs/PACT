# PACT — Privacy-Preserving Agent Coordination Technology

> **"Zero-connectivity resilience, zero hallucinated aid, zero-knowledge privacy."**

PACT is an emergency humanitarian coordination and dispatch platform built for rapid multi-agent response during infrastructure blackouts, disasters, and telecommunications collapse.

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
