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
