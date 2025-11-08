# HackerHardware.net

## Living Edge-Intelligence Ecosystem

HackerHardware.net is a cutting-edge digital-physical lab that merges hardware, AI, and cybersecurity into self-optimizing infrastructure. It combines Raspberry Pi clusters, FastAPI backends, and Cloudflare-routed automation under a zero-trust security perimeter.

## Architecture

### Core Components

- **Edge Computing Layer**: Raspberry Pi cluster nodes for distributed processing
- **API Layer**: FastAPI backend for AI and cybersecurity integration
- **Security Layer**: Zero-trust perimeter with continuous threat monitoring
- **Intelligence Layer**: Self-learning and adaptive defense mechanisms
- **Routing Layer**: Cloudflare-based routing and automation

### Technology Stack

- **Backend**: FastAPI (Python 3.9+)
- **Edge Devices**: Raspberry Pi 4/5 clusters
- **Container Orchestration**: Docker & Docker Compose
- **Security**: Zero-trust architecture, mTLS, JWT authentication
- **Monitoring**: Prometheus, Grafana, custom telemetry
- **CI/CD**: GitHub Actions
- **Infrastructure**: Cloudflare for routing and DDoS protection

## Project Structure

```
/
├── api/                    # FastAPI backend
├── edge/                   # Raspberry Pi cluster configs
├── security/              # Zero-trust security components
├── intelligence/          # AI and adaptive defense
├── monitoring/            # Observability and metrics
├── cloudflare/            # Cloudflare configurations
├── docker/                # Container configurations
└── docs/                  # Documentation
```

## Features

### 🔒 Zero-Trust Security
- Mutual TLS authentication
- JWT-based API authorization
- Network segmentation
- Continuous security monitoring

### 🤖 AI-Powered Intelligence
- Anomaly detection
- Threat prediction
- Self-optimization algorithms
- Network behavior analysis

### 🌐 Edge Computing
- Distributed Raspberry Pi nodes
- Local processing capabilities
- Failover and redundancy
- Resource optimization

### 🛡️ Offensive Testing & Adaptive Defense
- Continuous penetration testing
- Automated vulnerability scanning
- Real-time threat response
- Learning from network behavior

## Quick Start

### Prerequisites

- Docker & Docker Compose
- Python 3.9+
- Node.js 16+ (for Cloudflare Workers)
- Raspberry Pi devices (for edge deployment)

### Local Development

1. Clone the repository:
```bash
git clone https://github.com/canstralian/hackerhardware-site.git
cd hackerhardware-site
```

2. Start the backend:
```bash
cd api
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

3. Run with Docker Compose:
```bash
docker-compose up -d
```

### Deployment

See [docs/deployment.md](docs/deployment.md) for detailed deployment instructions.

## Security

This project implements a zero-trust security model. See [docs/security.md](docs/security.md) for details.

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT License - see [LICENSE](LICENSE) for details.