# PACT: Project Updates & Architectural Enhancements
**Record of Changes Implemented**

---

## 1. Summary of Updates

1. **Auto-Pinning Coordinates to OpenStreetMap on Ingest:**
   - **`A0_Intake` & `A3_GeoMatcher` Fix ([`a0_intake.py`](file:///home/adhithya/Desktop/PACT%20project/app/agents/a0_intake.py) & [`a3_geo_matcher.py`](file:///home/adhithya/Desktop/PACT%20project/app/agents/a3_geo_matcher.py)):** Emits `agent.completed` containing decoded GPS coordinates, victim UID, and search radius.
   - **Dashboard Auto-Pan ([`app.js`](file:///home/adhithya/Desktop/PACT%20project/app/static/js/app.js)):** On `A0_Intake` completion, the map immediately places the red `[SOS]` marker, centers on the victim, triggers the 25km `$geoNear` radius scan, and draws the routing line once allocated.

2. **Deduplicated Streaming & Token Pipeline:**
   - Fixed WebSocket reconnection handlers and stage-entry deduplication in `app.js` to eliminate double-printing and token stuttering in the terminal viewport.

3. **Data-Grounded Advocate Arguments & Proximity Rebuttals:**
   - Rewrote **[`a4_advocates.py`](file:///home/adhithya/Desktop/PACT%20project/app/agents/a4_advocates.py)**: Advocates cite their exact distance (`self.distance_km` km), arrival ETA (`self.eta_hours`h), itemized warehouse inventory, and transport vehicles. Rebuttals dynamically assert frontline arrival for closer depots and secondary bulk replenishment for rear hubs.

4. **Android GSM-7 Canonical Q-Frame Codec & Port Forwarding:**
   - Updated [`SmsEncoder.kt`](file:///home/adhithya/Desktop/PACT%20project/android/app/src/main/java/org/humanitarian/fieldapp/sms/SmsEncoder.kt) and [`SmsCodes.kt`](file:///home/adhithya/Desktop/PACT%20project/android/app/src/main/java/org/humanitarian/fieldapp/sms/SmsCodes.kt) with canonical Base-36 `Q|...` and `N|...` frames and PACK10 geocodes.
   - Fixed network failover in [`ApiClient.kt`](file:///home/adhithya/Desktop/PACT%20project/android/app/src/main/java/org/humanitarian/fieldapp/network/ApiClient.kt) for `http://127.0.0.1:8000` over USB and `http://172.16.58.76:8000` over Wi-Fi.
   - Updated [`MyRequestsScreen.kt`](file:///home/adhithya/Desktop/PACT%20project/android/app/src/main/java/org/humanitarian/fieldapp/ui/MyRequestsScreen.kt) to poll status using the logged-in user's organization ID.
