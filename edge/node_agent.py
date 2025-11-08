#!/usr/bin/env python3
"""
Edge Node Agent for Raspberry Pi
Handles registration, heartbeat, and local processing
"""
import asyncio
import httpx
import psutil
import socket
import os
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000/api/v1")
HEARTBEAT_INTERVAL = int(os.getenv("HEARTBEAT_INTERVAL", "30"))
NODE_HOSTNAME = socket.gethostname()


async def get_local_ip():
    """Get local IP address"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


async def register_node():
    """Register this node with the API"""
    ip_address = await get_local_ip()
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{API_BASE_URL}/nodes/register",
                json={
                    "hostname": NODE_HOSTNAME,
                    "ip_address": ip_address
                },
                timeout=10.0
            )
            response.raise_for_status()
            node_data = response.json()
            logger.info(f"Node registered: {node_data['node_id']}")
            return node_data["node_id"]
        except Exception as e:
            logger.error(f"Failed to register node: {e}")
            return None


async def send_heartbeat(node_id: str):
    """Send heartbeat with metrics"""
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_usage = psutil.virtual_memory().percent
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{API_BASE_URL}/nodes/{node_id}/heartbeat",
                params={
                    "cpu_usage": cpu_usage,
                    "memory_usage": memory_usage
                },
                timeout=10.0
            )
            response.raise_for_status()
            logger.info(f"Heartbeat sent - CPU: {cpu_usage}%, Memory: {memory_usage}%")
        except Exception as e:
            logger.error(f"Failed to send heartbeat: {e}")


async def monitor_and_report():
    """Monitor local system and report anomalies"""
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_usage = psutil.virtual_memory().percent
    
    # Simple threshold-based anomaly detection
    if cpu_usage > 90:
        logger.warning(f"High CPU usage detected: {cpu_usage}%")
    
    if memory_usage > 90:
        logger.warning(f"High memory usage detected: {memory_usage}%")


async def main():
    """Main agent loop"""
    logger.info(f"Starting edge node agent on {NODE_HOSTNAME}")
    
    # Register node
    node_id = await register_node()
    if not node_id:
        logger.error("Failed to register. Exiting.")
        return
    
    # Main loop
    try:
        while True:
            await send_heartbeat(node_id)
            await monitor_and_report()
            await asyncio.sleep(HEARTBEAT_INTERVAL)
    except KeyboardInterrupt:
        logger.info("Shutting down edge node agent")
    except Exception as e:
        logger.error(f"Agent error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
