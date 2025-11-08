"""
Health Check Endpoints
Provides system health and readiness checks
"""

from datetime import datetime, timezone
from typing import Dict

from fastapi import APIRouter, status
from pydantic import BaseModel, Field

router = APIRouter()


class HealthResponse(BaseModel):
    """Health check response model."""

    status: str = Field(..., description="Health status: healthy, degraded, unhealthy")
    timestamp: datetime = Field(..., description="Current server timestamp")
    version: str = Field(..., description="API version")
    uptime_seconds: float = Field(..., description="Application uptime in seconds")


class ReadinessResponse(BaseModel):
    """Readiness check response model."""

    ready: bool = Field(..., description="Whether the service is ready to accept traffic")
    checks: Dict[str, bool] = Field(..., description="Individual readiness checks")


# Track application start time
_start_time = datetime.now(timezone.utc)


@router.get(
    "/healthz",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Health Check",
    description="Returns the health status of the API",
)
async def health_check() -> HealthResponse:
    """
    Health check endpoint for load balancers and monitoring systems.

    Returns:
        HealthResponse: Current health status and metadata
    """
    current_time = datetime.now(timezone.utc)
    uptime = (current_time - _start_time).total_seconds()

    return HealthResponse(
        status="healthy",
        timestamp=current_time,
        version="1.0.0",
        uptime_seconds=uptime,
    )


@router.get(
    "/readyz",
    response_model=ReadinessResponse,
    status_code=status.HTTP_200_OK,
    summary="Readiness Check",
    description="Returns whether the service is ready to accept traffic",
)
async def readiness_check() -> ReadinessResponse:
    """
    Readiness check endpoint for Kubernetes and orchestration systems.

    Returns:
        ReadinessResponse: Readiness status with individual check results
    """
    # Perform readiness checks
    checks = {
        "api": True,  # API is responding
        "database": True,  # Database connection (placeholder)
        "cache": True,  # Cache connection (placeholder)
    }

    return ReadinessResponse(
        ready=all(checks.values()),
        checks=checks,
    )


@router.get(
    "/livez",
    status_code=status.HTTP_200_OK,
    summary="Liveness Check",
    description="Simple liveness check - returns 200 if application is alive",
)
async def liveness_check() -> Dict[str, str]:
    """
    Liveness check endpoint for Kubernetes.

    Returns:
        dict: Simple status message
    """
    return {"status": "alive"}
