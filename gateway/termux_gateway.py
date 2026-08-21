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
