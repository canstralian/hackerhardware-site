"""
Metrics Endpoints
Provides system metrics and telemetry data
"""

import time
from typing import Dict

from fastapi import APIRouter
from pydantic import BaseModel, Field

router = APIRouter()


class MetricsResponse(BaseModel):
    """Metrics response model."""

    nodes: int = Field(..., description="Number of active nodes")
    uptime: float = Field(..., description="System uptime in seconds")
    requests_per_second: float = Field(..., description="Current request rate")
    cpu_percent: float = Field(..., description="CPU usage percentage")
    memory_percent: float = Field(..., description="Memory usage percentage")
    active_connections: int = Field(..., description="Number of active connections")


# Simulated metrics (replace with actual monitoring in production)
_metrics_start_time = time.time()
_request_count = 0


@router.get(
    "/metrics",
    response_model=MetricsResponse,
    summary="System Metrics",
    description="Returns current system metrics and performance data",
)
async def get_metrics() -> MetricsResponse:
    """
    Get current system metrics.

    Returns:
        MetricsResponse: System performance metrics
    """
    global _request_count
    _request_count += 1

    uptime = time.time() - _metrics_start_time
    rps = _request_count / uptime if uptime > 0 else 0

    return MetricsResponse(
        nodes=3,  # Placeholder: replace with actual node count
        uptime=uptime,
        requests_per_second=round(rps, 2),
        cpu_percent=23.5,  # Placeholder: integrate with psutil
        memory_percent=45.2,  # Placeholder: integrate with psutil
        active_connections=12,  # Placeholder: track actual connections
    )


@router.get(
    "/metrics/prometheus",
    summary="Prometheus Metrics",
    description="Returns metrics in Prometheus format",
)
async def prometheus_metrics() -> str:
    """
    Export metrics in Prometheus format.

    Returns:
        str: Metrics in Prometheus exposition format
    """
    uptime = time.time() - _metrics_start_time

    return f"""# HELP hackerhardware_uptime_seconds Application uptime in seconds
# TYPE hackerhardware_uptime_seconds counter
hackerhardware_uptime_seconds {uptime}

# HELP hackerhardware_requests_total Total number of requests
# TYPE hackerhardware_requests_total counter
hackerhardware_requests_total {_request_count}

# HELP hackerhardware_nodes_active Number of active nodes
# TYPE hackerhardware_nodes_active gauge
hackerhardware_nodes_active 3

# HELP hackerhardware_cpu_usage_percent CPU usage percentage
# TYPE hackerhardware_cpu_usage_percent gauge
hackerhardware_cpu_usage_percent 23.5

# HELP hackerhardware_memory_usage_percent Memory usage percentage
# TYPE hackerhardware_memory_usage_percent gauge
hackerhardware_memory_usage_percent 45.2
"""
