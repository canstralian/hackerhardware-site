"""
API v1 - Main router combining all v1 endpoints
"""

from fastapi import APIRouter

from backend.api.v1 import health, metrics, system

router = APIRouter()

# Include sub-routers
router.include_router(health.router, tags=["Health"])
router.include_router(metrics.router, tags=["Metrics"])
router.include_router(system.router, tags=["System"])

__all__ = ["router"]
