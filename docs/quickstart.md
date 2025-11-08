# Quick Start Guide

Get HackerHardware.net up and running in minutes!

## Prerequisites

Before you begin, ensure you have:

- **Docker** (20.10+) and **Docker Compose** (2.0+)
- **Python** 3.9 or higher
- **Git** for version control
- At least 2GB of RAM available
- 10GB of free disk space

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/canstralian/hackerhardware-site.git
cd hackerhardware-site
```

### 2. Quick Setup with Script

For the fastest setup, use our automated script:

```bash
chmod +x scripts/setup.sh
./scripts/setup.sh
```

This script will:
- Check prerequisites
- Create environment configuration
- Generate SSL certificates
- Install dependencies
- Build and start all services

### 3. Manual Setup (Alternative)

If you prefer manual setup:

```bash
# Create environment file
cp .env.example .env

# Generate secret key
SECRET_KEY=$(openssl rand -hex 32)
sed -i "s/change-this-to-a-random-secret-key/$SECRET_KEY/" .env

# Start services with Docker Compose
docker-compose up -d
```

## Verify Installation

Once the services are running, verify everything is working:

### 1. Check Service Health

```bash
# API Health
curl http://localhost:8000/api/v1/health

# Expected response:
# {
#   "status": "healthy",
#   "timestamp": "...",
#   "system": {...}
# }
```

### 2. Access Services

- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs (Interactive Swagger UI)
- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3001 (default: admin/admin)

## First Steps

### Register an Edge Node

```bash
curl -X POST http://localhost:8000/api/v1/nodes/register \
  -H "Content-Type: application/json" \
  -d '{
    "hostname": "my-first-node",
    "ip_address": "192.168.1.100"
  }'
```

### Check Security Posture

```bash
curl http://localhost:8000/api/v1/security/posture
```

### Get AI Predictions

```bash
curl http://localhost:8000/api/v1/intelligence/predict
```

## Development Mode

For local development with hot-reload:

```bash
cd api
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Deploying Edge Nodes

On your Raspberry Pi or edge device:

```bash
# Clone repository
git clone https://github.com/canstralian/hackerhardware-site.git
cd hackerhardware-site/edge

# Install dependencies
pip3 install -r requirements.txt

# Configure API endpoint
export API_BASE_URL="http://your-api-server:8000/api/v1"

# Run the edge agent
python3 node_agent.py
```

## Common Commands

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f api
```

### Restart Services

```bash
# All services
docker-compose restart

# Specific service
docker-compose restart api
```

### Stop Services

```bash
docker-compose down
```

### Update and Rebuild

```bash
git pull
docker-compose down
docker-compose build
docker-compose up -d
```

## Troubleshooting

### Port Already in Use

If ports 8000, 9090, or 3001 are already in use, edit `docker-compose.yml` to change the port mappings:

```yaml
ports:
  - "8080:8000"  # Change 8000 to 8080 or any available port
```

### API Not Starting

Check the logs:
```bash
docker-compose logs api
```

Common issues:
- Missing environment variables (check `.env` file)
- Insufficient permissions
- Port conflicts

### Edge Node Can't Connect

Verify:
1. API is accessible from the edge device
2. Firewall allows connections on port 8000
3. `API_BASE_URL` is correctly configured
4. Network connectivity is stable

### Docker Permission Denied

Add your user to the docker group:
```bash
sudo usermod -aG docker $USER
newgrp docker
```

## Next Steps

Now that you have HackerHardware.net running:

1. **[Read the Architecture](architecture.md)** - Understand the system design
2. **[Configure Security](security.md)** - Set up zero-trust policies
3. **[Deploy to Production](deployment.md)** - Scale your infrastructure
4. **[API Documentation](api.md)** - Explore all endpoints
5. **[Contributing](../CONTRIBUTING.md)** - Join the community

## Getting Help

- **Documentation**: [docs/](.)
- **Issues**: [GitHub Issues](https://github.com/canstralian/hackerhardware-site/issues)
- **Discussions**: [GitHub Discussions](https://github.com/canstralian/hackerhardware-site/discussions)

## What's Next?

Explore these features:

- **Threat Detection**: Run security scans on your network
- **Anomaly Detection**: Let AI monitor your infrastructure
- **Adaptive Defense**: Learn from security incidents
- **Edge Computing**: Deploy more Raspberry Pi nodes
- **Cloudflare Integration**: Add global routing and DDoS protection

Happy hacking! 🚀
