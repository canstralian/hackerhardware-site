"""
System Endpoints
System information and configuration
"""

import platform
from typing import Dict, List

from fastapi import APIRouter
from pydantic import BaseModel, Field

router = APIRouter()


class SystemInfo(BaseModel):
    """System information model."""

    platform: str = Field(..., description="Operating system platform")
    python_version: str = Field(..., description="Python version")
    architecture: str = Field(..., description="System architecture")
    hostname: str = Field(..., description="System hostname")


class FeatureFlags(BaseModel):
    """Feature flags configuration."""

    features: Dict[str, bool] = Field(..., description="Available feature flags")


@router.get(
    "/system/info",
    response_model=SystemInfo,
    summary="System Information",
    description="Returns system configuration and environment details",
)
async def get_system_info() -> SystemInfo:
    """
    Get system information.

    Returns:
        SystemInfo: System configuration details
    """
    return SystemInfo(
        platform=platform.system(),
        python_version=platform.python_version(),
        architecture=platform.machine(),
        hostname=platform.node(),
    )


@router.get(
    "/system/features",
    response_model=FeatureFlags,
    summary="Feature Flags",
    description="Returns currently enabled feature flags",
)
async def get_feature_flags() -> FeatureFlags:
    """
    Get feature flags configuration.

    Returns:
        FeatureFlags: Current feature flag states
    """
    return FeatureFlags(
        features={
            "metrics_enabled": True,
            "rate_limiting": True,
            "edge_caching": True,
            "auto_scaling": False,  # Future feature
            "ai_optimization": False,  # Future feature
        }
    )
