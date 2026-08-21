"""
Unified Ingestion API Endpoints.
Provides /api/v1/pact/ingest (unified wire format), /api/v1/sms/webhook (gateway adapter),
and /api/v1/sms/inbox (cellular SMS confirmation polling for mobile apps).
"""

from typing import List
from fastapi import APIRouter, Request, HTTPException
from app.agents.pipeline import pipeline
from app.db.mongo import get_collection, clean_mongo_doc

router = APIRouter(prefix="/api/v1", tags=["Ingest"])

# In-memory fast queue for outbound SMS confirmations delivered to mobile apps
OUTBOUND_SMS_QUEUE: List[str] = []


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
    
    # Enqueue SMS ack frame if produced
    ack_sms = result.get("ack_sms") or result.get("sms_ack_frame")
    if ack_sms:
        OUTBOUND_SMS_QUEUE.append(ack_sms)

    return clean_mongo_doc(result)


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
            msg_body = data.get("Body") or data.get("body") or data.get("text") or data.get("sms") or ""
            msg_from = data.get("From") or data.get("from") or data.get("sender") or "TERMUX_SMS"
        except Exception:
            pass
    elif "application/x-www-form-urlencoded" in content_type or "multipart/form-data" in content_type:
        try:
            form = await request.form()
            msg_body = str(form.get("Body") or form.get("body") or form.get("text") or form.get("sms") or "")
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

    ack_sms = result.get("ack_sms") or result.get("sms_ack_frame")
    if ack_sms:
        OUTBOUND_SMS_QUEUE.append(ack_sms)

    return {
        "status": "received",
        "ack_sms": ack_sms,
        "pipeline_result": clean_mongo_doc(result)
    }


@router.get("/sms/inbox")
async def get_sms_inbox():
    """
    Returns outbound SMS confirmation frames waiting to be delivered to mobile phones.
    """
    matches_col = get_collection("matches")
    recent_matches = await matches_col.find({"sms_ack_frame": {"$exists": True}}).sort("created_at", -1).limit(10).to_list(10)
    
    db_acks = [m.get("sms_ack_frame") for m in recent_matches if m.get("sms_ack_frame")]
    combined = list(dict.fromkeys(OUTBOUND_SMS_QUEUE[-10:] + db_acks))

    return {
        "count": len(combined),
        "messages": combined
    }


@router.post("/sms/clear")
async def clear_sms_inbox():
    """Clears outbound SMS inbox."""
    OUTBOUND_SMS_QUEUE.clear()
    return {"status": "cleared"}
