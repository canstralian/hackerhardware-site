# Edge Node Configuration

This directory contains configuration and scripts for Raspberry Pi edge nodes.

## Setup

### Prerequisites
- Raspberry Pi 4 or 5
- Raspberry Pi OS (64-bit recommended)
- Python 3.9+
- Network connectivity

### Installation

1. Update the system:
```bash
sudo apt update && sudo apt upgrade -y
```

2. Install Python dependencies:
```bash
cd edge
pip3 install -r requirements.txt
```

3. Configure environment:
```bash
export API_BASE_URL="https://your-api-domain.com/api/v1"
export HEARTBEAT_INTERVAL=30
```

4. Run the node agent:
```bash
python3 node_agent.py
```

### Auto-start on Boot

Create a systemd service:

```bash
sudo nano /etc/systemd/system/hackerhardware-node.service
```

Add:
```ini
[Unit]
Description=HackerHardware Edge Node Agent
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/hackerhardware-site/edge
Environment="API_BASE_URL=https://your-api-domain.com/api/v1"
ExecStart=/usr/bin/python3 /home/pi/hackerhardware-site/edge/node_agent.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable hackerhardware-node
sudo systemctl start hackerhardware-node
sudo systemctl status hackerhardware-node
```

## Features

- Automatic node registration
- Periodic heartbeat with metrics
- Local anomaly detection
- Self-healing capabilities
- Resource monitoring

## Security

- All communications use HTTPS
- JWT authentication for API calls
- Local certificate validation
- Network isolation options
