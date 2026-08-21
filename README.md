# PACT — Privacy-Preserving Agent Coordination Technology

> **"Zero-connectivity resilience, zero hallucinated aid, zero-knowledge privacy."**

PACT is an emergency humanitarian coordination and dispatch platform built for rapid multi-agent response during infrastructure blackouts, disasters, and telecommunications collapse.

---

## 💡 The Core Innovation: 2G When the Internet Fails

During catastrophic disasters (earthquakes, cyclones, floods, conflict zones), **broadband and 4G/5G data networks are the first infrastructure to collapse**. Fiber lines sever, base stations lose backhaul, and power grids fail.

**However, low-frequency 2G GSM cellular signals almost always survive.** 
2G operates at 850/900 MHz frequencies with minimal power requirements. These low-frequency radio waves **penetrate collapsed concrete structures, deep rubble, mountain valleys, and remote rural pockets** where no high-frequency 4G/5G signal or internet packet can reach.

### How PACT Leverages 2G:
Instead of waiting for internet restoration, **PACT turns 2G SMS into a high-density, tamper-proof emergency coordination grid**. 
- Using a custom **Base-36 and PACK10 codec**, an entire multi-parameter distress request (victim headcount, trapped status, injuries, required supplies, 1.1-meter pinpoint GPS, and error-checking checksums) is compressed into **just 35 plain characters** (`Q|001|7F3K|15223C03Q0|6QR6VFBQ33|7F`).
- Leaves **125 characters spare** in a standard 160-character 2G SMS, guaranteeing transmission success even over fluctuating, single-bar cellular connections.

---

## 🛡️ Core Architectural Pillars

1. **Zero-Connectivity Resilience**: Works completely offline using 2G GSM SMS or local device SQLite queues with automatic background sync.
2. **Zero Hallucinated Aid**: Large Language Models (LLMs) are strictly forbidden from performing mathematical allocations. Pure Python deterministic algorithms compute all supply distribution, while AI agents reason about constraints and triage priorities.
3. **Zero-Knowledge Privacy**: Requesters' real names, phone numbers, and pinpoint coordinates are masked by default. Sensitive details are only revealed to a confirmed responder after an allocation is officially accepted and locked.

---

## 📱 Android Field Application (`/android`)

The Android mobile client (`org.humanitarian.fieldapp`) is built with **Kotlin and Jetpack Compose**, engineered specifically for first responders and disaster-affected citizens operating without internet.

```
                  ┌─────────────────────────────────────────┐
                  │        Android Mobile Client (App)       │
                  └────────────────────┬────────────────────┘
                                       │
                ┌──────────────────────┴──────────────────────┐
                ▼                                             ▼
     [ 1. User Interface (UI) ]                   [ 2. Codec & SMS Engine ]
     • FieldReportScreen                          • SmsEncoder & Pack10
     • HomeScreen & MyRequests                    • Checksum (XOR CRC)
     • OfflineMapScreen                           • DirectSmsSender
     • SmsFallback & SmsDecoder                   • Base36 bitfield packer
                │                                             │
                └──────────────────────┬──────────────────────┘
                                       │
                ┌──────────────────────┴──────────────────────┐
                ▼                                             ▼
    [ 3. Offline & Sync Engine ]                  [ 4. Network & Session ]
     • OfflineQueue (Local persistence)           • ApiClient (HTTP/REST)
     • SyncManager (Auto-drain queue)             • UserSession (Preferences)
```

### Key Android Components:
* **`SmsEncoder.kt` & `Pack10.kt`**:
  - Compresses multi-variable distress reports into 10-char Base-36 strings and maps hardware GPS coordinates down to **~1.1-meter precision in 10 characters** (`PACK10`).
* **`DirectSmsSender.kt`**:
  - Leverages Android's `SmsManager` to **silently dispatch background 2G SMS packets** directly through the SIM card without opening third-party messenger apps.
* **`Checksum.kt`**:
  - Computes a 2-digit uppercase hexadecimal XOR checksum across every frame to reject noisy or corrupted cellular transmissions.
* **`OfflineQueue.kt` & `SyncManager.kt`**:
  - Offline-first SQLite queue that holds unsent reports and automatically flushes them via `ApiClient` when an internet or gateway connection is restored.
* **`FieldReportScreen.kt`**:
  - Chip-based and dropdown-based UI eliminating panic typos. Automatically acquires GPS from Google Play Services `LocationServices`.
* **`OfflineMapScreen.kt` & `SmsDecoderScreen.kt`**:
  - Built-in responder utilities for offline spatial marker navigation and manual SMS frame decoding in the field.

---

## ⚡ 12-Stage Multi-Agent Reasoning Pipeline

```
[ Ingest (2G SMS / HTTP) ]
           │
           ▼
 ┌────────────────────────────────────────────────────────────────────────┐
 │               12-STAGE MULTI-AGENT REASONING PIPELINE                  │
 ├────────────────────────────────────────────────────────────────────────┤
 │  A0: Intake (Frame parsing & XOR Checksum validation)                  │
 │  A1: Dedupe (Compound (uid, seq) deduplication)                        │
 │  A2: Triage (Groq Llama-3.3-70B situational triage & risk scoring)    │
 │  A3: Geo Matcher (MongoDB $geoNear 2dsphere rings: 10km → 150km)       │
 │  A4: Advocates (Parallel AI agents simulating provider constraints)    │
 │  A5: Allocation Solver (Pure Python deterministic math optimizer)      │
 │  A6: Arbiter (LLM selects best plan — firewalled from inventing numbers)│
 │  A7: Privacy Redactor (Zero-knowledge masking of names & coordinates)  │
 │  A8: Admin Gate (Live human override + configurable Autopilot timer)   │
 │  A9: Narrator (Translates decision into natural language bulletin)     │
 │  A10: Verification (Generates SMS handshake confirmations)             │
 │  A11: Replanner (Auto re-routes if a provider rejects or fails)        │
 └────────────────────────────────────────────────────────────────────────┘
           │
           ▼
[ Live WebSocket Command Portal & Outbound SMS Confirmation ]
```

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
All unit and integration tests verify PACK10 round-tripping, XOR checksum arithmetic, deterministic solver math, and API endpoints.

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
├── android/                    # Android Kotlin Jetpack Compose Field Application
│   ├── app/src/main/java/org/humanitarian/fieldapp/
│   │   ├── sms/                # Base-36, PACK10, Checksum & DirectSmsSender
│   │   ├── offline/            # OfflineQueue & SubmittedReports
│   │   ├── sync/               # SyncManager auto-sync engine
│   │   ├── network/            # ApiClient & REST models
│   │   └── ui/                 # FieldReport, OfflineMap, Decoder & Home screens
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
└── README.md                   # Complete Platform & Codec Documentation
```
