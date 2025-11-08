"""
Health check endpoints
"""
from fastapi import APIRouter
from datetime import datetime
import psutil

router = APIRouter()


@router.get("/health")
async def health_check():
    """System health check"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "system": {
            "cpu_percent": psutil.cpu_percent(interval=1),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_percent": psutil.disk_usage('/').percent
        }
    }


@router.get("/readiness")
async def readiness_check():
    """Readiness probe for orchestration"""
    return {
        "ready": True,
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/liveness")
async def liveness_check():
    """Liveness probe for orchestration"""
    return {
        "alive": True,
        "timestamp": datetime.utcnow().isoformat()
    }
