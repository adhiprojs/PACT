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
