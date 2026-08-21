"""
PACT API Package.
Exports all REST and WebSocket routers.
"""

from fastapi import APIRouter
from app.api.ingest import router as ingest_router
from app.api.requests import router as requests_router
from app.api.offers import router as offers_router
from app.api.matches import router as matches_router
from app.api.admin import router as admin_router
from app.api.ws import router as ws_router

api_router = APIRouter()
api_router.include_router(ingest_router)
api_router.include_router(requests_router)
api_router.include_router(offers_router)
api_router.include_router(matches_router)
api_router.include_router(admin_router)

__all__ = [
    "api_router",
    "ws_router",
    "ingest_router",
    "requests_router",
    "offers_router",
    "matches_router",
    "admin_router",
]
