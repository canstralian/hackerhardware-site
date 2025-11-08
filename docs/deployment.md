# Deployment Guide

## Prerequisites

- Docker and Docker Compose
- Python 3.9+
- Node.js 16+ (for Cloudflare Workers)
- SSL certificates
- Domain name configured

## Local Development

### 1. Clone the Repository

```bash
git clone https://github.com/canstralian/hackerhardware-site.git
cd hackerhardware-site
```

### 2. Configure Environment

Create a `.env` file:

```bash
SECRET_KEY=your-secret-key-here
GRAFANA_PASSWORD=secure-password
ALLOWED_ORIGINS=http://localhost:3000
```

### 3. Generate SSL Certificates (Optional for local dev)

```bash
mkdir -p certs
cd certs
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout server.key -out server.crt
```

### 4. Start Services

```bash
docker-compose up -d
```

### 5. Verify Deployment

- API: http://localhost:8000
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3001

## Production Deployment

### Cloud Infrastructure

#### Option 1: Docker Swarm

```bash
# Initialize swarm
docker swarm init

# Deploy stack
docker stack deploy -c docker-compose.yml hackerhardware
```

#### Option 2: Kubernetes

```bash
# Create namespace
kubectl create namespace hackerhardware

# Apply configurations
kubectl apply -f k8s/
```

### Cloudflare Configuration

1. Install Wrangler CLI:
```bash
npm install -g wrangler
```

2. Authenticate:
```bash
wrangler login
```

3. Configure wrangler.toml with your account details

4. Deploy worker:
```bash
cd cloudflare
wrangler publish
```

### Edge Node Deployment

On each Raspberry Pi:

1. Install dependencies:
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip -y
```

2. Clone repository:
```bash
git clone https://github.com/canstralian/hackerhardware-site.git
cd hackerhardware-site/edge
```

3. Install Python packages:
```bash
pip3 install -r requirements.txt
```

4. Configure systemd service:
```bash
sudo cp hackerhardware-node.service /etc/systemd/system/
sudo systemctl enable hackerhardware-node
sudo systemctl start hackerhardware-node
```

## Security Configuration

### Zero-Trust Setup

1. Generate certificates for mutual TLS:
```bash
./scripts/generate-certs.sh
```

2. Distribute certificates to edge nodes

3. Enable mTLS in configuration

### Firewall Rules

```bash
# Allow only necessary ports
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw enable
```

## Monitoring Setup

### Prometheus

Access Prometheus at http://your-domain:9090

Configure targets in `monitoring/prometheus.yml`

### Grafana

1. Access Grafana at http://your-domain:3001
2. Login with admin credentials
3. Add Prometheus as data source
4. Import dashboards from `monitoring/grafana/dashboards/`

## Troubleshooting

### API Not Starting

```bash
docker-compose logs api
```

### Edge Node Connection Issues

```bash
# Check logs
journalctl -u hackerhardware-node -f

# Verify connectivity
curl https://your-api-domain.com/api/v1/health
```

### Certificate Issues

```bash
# Verify certificate validity
openssl x509 -in certs/server.crt -text -noout
```

## Scaling

### Horizontal Scaling

Add more edge nodes:
```bash
# On new Raspberry Pi
curl -sSL https://get.docker.com | sh
sudo usermod -aG docker $USER
```

### API Scaling

```bash
docker-compose up -d --scale api=3
```

## Backup and Recovery

### Database Backup

```bash
docker exec redis redis-cli SAVE
docker cp redis:/data/dump.rdb ./backup/
```

### Configuration Backup

```bash
tar -czf backup-$(date +%Y%m%d).tar.gz \
  api/ edge/ security/ monitoring/ cloudflare/
```

## Updates

### Rolling Update

```bash
git pull
docker-compose build
docker-compose up -d --no-deps --build api
```

### Zero-Downtime Deployment

Use blue-green deployment strategy with load balancer.
