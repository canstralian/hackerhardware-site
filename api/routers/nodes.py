"""
Edge node management endpoints
"""
from fastapi import APIRouter, HTTPException, status
from typing import List
from datetime import datetime
from pydantic import BaseModel

router = APIRouter()

# In-memory storage (replace with database in production)
edge_nodes = {}


class EdgeNode(BaseModel):
    """Edge node model"""
    node_id: str
    hostname: str
    ip_address: str
    status: str = "active"
    cpu_usage: float = 0.0
    memory_usage: float = 0.0
    last_heartbeat: str = None


class NodeRegistration(BaseModel):
    """Node registration request"""
    hostname: str
    ip_address: str


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_node(node: NodeRegistration):
    """Register a new edge node"""
    node_id = f"node-{len(edge_nodes) + 1}"
    new_node = EdgeNode(
        node_id=node_id,
        hostname=node.hostname,
        ip_address=node.ip_address,
        last_heartbeat=datetime.utcnow().isoformat()
    )
    edge_nodes[node_id] = new_node
    return new_node


@router.get("/", response_model=List[EdgeNode])
async def list_nodes():
    """List all registered edge nodes"""
    return list(edge_nodes.values())


@router.get("/{node_id}", response_model=EdgeNode)
async def get_node(node_id: str):
    """Get specific edge node details"""
    if node_id not in edge_nodes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Node not found"
        )
    return edge_nodes[node_id]


@router.post("/{node_id}/heartbeat")
async def node_heartbeat(node_id: str, cpu_usage: float, memory_usage: float):
    """Update node heartbeat and metrics"""
    if node_id not in edge_nodes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Node not found"
        )

    node = edge_nodes[node_id]
    node.cpu_usage = cpu_usage
    node.memory_usage = memory_usage
    node.last_heartbeat = datetime.utcnow().isoformat()
    node.status = "active"

    return {"status": "ok", "node_id": node_id}


@router.delete("/{node_id}")
async def deregister_node(node_id: str):
    """Deregister an edge node"""
    if node_id not in edge_nodes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Node not found"
        )

    del edge_nodes[node_id]
    return {"status": "deleted", "node_id": node_id}
