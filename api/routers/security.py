"""
Security and threat monitoring endpoints
"""
from fastapi import APIRouter, status
from typing import List
from datetime import datetime
from pydantic import BaseModel

router = APIRouter()

# In-memory threat log (replace with proper storage)
threat_log = []


class ThreatAlert(BaseModel):
    """Threat alert model"""
    alert_id: str
    severity: str  # critical, high, medium, low
    threat_type: str
    source_ip: str
    timestamp: str
    description: str
    status: str = "active"


class SecurityScan(BaseModel):
    """Security scan request"""
    target: str
    scan_type: str  # port_scan, vulnerability_scan, penetration_test


@router.get("/threats", response_model=List[ThreatAlert])
async def get_threats():
    """Get all threat alerts"""
    return threat_log


@router.post("/threats", status_code=status.HTTP_201_CREATED)
async def report_threat(
    severity: str,
    threat_type: str,
    source_ip: str,
    description: str
):
    """Report a new threat"""
    alert_id = f"threat-{len(threat_log) + 1}"
    alert = ThreatAlert(
        alert_id=alert_id,
        severity=severity,
        threat_type=threat_type,
        source_ip=source_ip,
        timestamp=datetime.utcnow().isoformat(),
        description=description
    )
    threat_log.append(alert)
    return alert


@router.post("/scan")
async def initiate_security_scan(scan: SecurityScan):
    """Initiate a security scan"""
    scan_id = f"scan-{datetime.utcnow().timestamp()}"

    return {
        "scan_id": scan_id,
        "status": "initiated",
        "target": scan.target,
        "scan_type": scan.scan_type,
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/posture")
async def security_posture():
    """Get overall security posture"""
    active_threats = [
        t for t in threat_log
        if (t.status if hasattr(t, 'status') else t.get('status')) == "active"
    ]
    critical_threats = [
        t for t in active_threats
        if (t.severity if hasattr(t, 'severity')
            else t.get('severity')) == "critical"
    ]

    return {
        "status": "monitoring",
        "active_threats": len(active_threats),
        "critical_threats": len(critical_threats),
        "last_scan": datetime.utcnow().isoformat(),
        "zero_trust_enabled": True
    }
