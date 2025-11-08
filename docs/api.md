# API Documentation

## Base URL

```
http://localhost:8000/api/v1
```

## Authentication

Most endpoints require JWT authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your-token>
```

## Endpoints

### Health & Status

#### GET /health
Check API health status.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-11-08T10:00:00.000000",
  "system": {
    "cpu_percent": 25.5,
    "memory_percent": 45.2,
    "disk_percent": 60.1
  }
}
```

#### GET /readiness
Kubernetes readiness probe.

**Response:**
```json
{
  "ready": true,
  "timestamp": "2024-11-08T10:00:00.000000"
}
```

#### GET /liveness
Kubernetes liveness probe.

**Response:**
```json
{
  "alive": true,
  "timestamp": "2024-11-08T10:00:00.000000"
}
```

### Edge Nodes

#### POST /nodes/register
Register a new edge node.

**Request:**
```json
{
  "hostname": "rpi-node-01",
  "ip_address": "192.168.1.100"
}
```

**Response:**
```json
{
  "node_id": "node-1",
  "hostname": "rpi-node-01",
  "ip_address": "192.168.1.100",
  "status": "active",
  "cpu_usage": 0.0,
  "memory_usage": 0.0,
  "last_heartbeat": "2024-11-08T10:00:00.000000"
}
```

#### GET /nodes/
List all registered edge nodes.

**Response:**
```json
[
  {
    "node_id": "node-1",
    "hostname": "rpi-node-01",
    "ip_address": "192.168.1.100",
    "status": "active",
    "cpu_usage": 25.5,
    "memory_usage": 45.2,
    "last_heartbeat": "2024-11-08T10:00:00.000000"
  }
]
```

#### GET /nodes/{node_id}
Get specific node details.

**Response:**
```json
{
  "node_id": "node-1",
  "hostname": "rpi-node-01",
  "ip_address": "192.168.1.100",
  "status": "active",
  "cpu_usage": 25.5,
  "memory_usage": 45.2,
  "last_heartbeat": "2024-11-08T10:00:00.000000"
}
```

#### POST /nodes/{node_id}/heartbeat
Update node heartbeat and metrics.

**Query Parameters:**
- `cpu_usage` (float): CPU usage percentage
- `memory_usage` (float): Memory usage percentage

**Response:**
```json
{
  "status": "ok",
  "node_id": "node-1"
}
```

#### DELETE /nodes/{node_id}
Deregister an edge node.

**Response:**
```json
{
  "status": "deleted",
  "node_id": "node-1"
}
```

### Security

#### GET /security/threats
List all threat alerts.

**Response:**
```json
[
  {
    "alert_id": "threat-1",
    "severity": "high",
    "threat_type": "port_scan",
    "source_ip": "192.168.1.200",
    "timestamp": "2024-11-08T10:00:00.000000",
    "description": "Suspicious port scanning detected",
    "status": "active"
  }
]
```

#### POST /security/threats
Report a new threat.

**Request:**
```json
{
  "severity": "high",
  "threat_type": "intrusion_attempt",
  "source_ip": "192.168.1.200",
  "description": "Multiple failed authentication attempts"
}
```

**Response:**
```json
{
  "alert_id": "threat-2",
  "severity": "high",
  "threat_type": "intrusion_attempt",
  "source_ip": "192.168.1.200",
  "timestamp": "2024-11-08T10:00:00.000000",
  "description": "Multiple failed authentication attempts",
  "status": "active"
}
```

#### POST /security/scan
Initiate a security scan.

**Request:**
```json
{
  "target": "192.168.1.100",
  "scan_type": "port_scan"
}
```

**Response:**
```json
{
  "scan_id": "scan-1699437600.123",
  "status": "initiated",
  "target": "192.168.1.100",
  "scan_type": "port_scan",
  "timestamp": "2024-11-08T10:00:00.000000"
}
```

#### GET /security/posture
Get overall security posture.

**Response:**
```json
{
  "status": "monitoring",
  "active_threats": 2,
  "critical_threats": 0,
  "last_scan": "2024-11-08T10:00:00.000000",
  "zero_trust_enabled": true
}
```

### Intelligence

#### GET /intelligence/anomalies
Detect anomalies across the network.

**Response:**
```json
[]
```

#### GET /intelligence/predict
Predict potential threats using AI.

**Response:**
```json
{
  "prediction_type": "threat_analysis",
  "confidence": 0.85,
  "threat_level": "low",
  "timestamp": "2024-11-08T10:00:00.000000",
  "recommendations": [
    "Continue monitoring",
    "Update security policies",
    "Review access logs"
  ]
}
```

#### GET /intelligence/optimize
Get network optimization recommendations.

**Response:**
```json
{
  "optimization_id": "opt-1699437600.123",
  "recommendations": [
    {
      "type": "resource_allocation",
      "target": "edge_nodes",
      "action": "rebalance_load",
      "priority": "medium"
    }
  ],
  "timestamp": "2024-11-08T10:00:00.000000"
}
```

#### POST /intelligence/learn
Submit data for AI learning.

**Request:**
```json
{
  "event_type": "security_incident",
  "data": {
    "source": "node-1",
    "severity": "medium",
    "action_taken": "blocked"
  }
}
```

**Response:**
```json
{
  "status": "accepted",
  "message": "Data submitted for analysis",
  "events_collected": 42
}
```

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Invalid request parameters"
}
```

### 401 Unauthorized
```json
{
  "detail": "Could not validate credentials"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

## Rate Limiting

- Default: 100 requests per minute per IP
- Exceeded: HTTP 429 Too Many Requests

## Pagination

For endpoints that return lists, use query parameters:
- `page`: Page number (default: 1)
- `perPage`: Items per page (default: 20, max: 100)

Example:
```
GET /api/v1/nodes?page=2&perPage=50
```

## WebSocket Support (Future)

Real-time updates will be available via WebSocket:

```javascript
const ws = new WebSocket('ws://localhost:8000/ws/updates');
```

## SDK Examples

### Python

```python
import httpx

async with httpx.AsyncClient() as client:
    response = await client.get("http://localhost:8000/api/v1/health")
    print(response.json())
```

### JavaScript

```javascript
const response = await fetch('http://localhost:8000/api/v1/health');
const data = await response.json();
console.log(data);
```

### cURL

```bash
curl -X GET http://localhost:8000/api/v1/health
```
