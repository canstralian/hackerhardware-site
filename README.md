# HackerHardware.net

> **Edge Autonomy Infrastructure** — A living ecosystem merging edge computing, AI, and cybersecurity into adaptive, self-healing infrastructure.

[![Deploy Status](https://img.shields.io/github/actions/workflow/status/canstralian/hackerhardware-site/deploy-pages.yml?branch=main)](https://github.com/canstralian/hackerhardware-site/actions)
[![Security Scan](https://img.shields.io/github/actions/workflow/status/canstralian/hackerhardware-site/security-scan.yml?label=security)](https://github.com/canstralian/hackerhardware-site/actions)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## Philosophy

Every node learns, adapts, and integrates seamlessly with the network. HackerHardware.net represents a new paradigm in infrastructure design: **edge autonomy** — where intelligence moves to the data, not the other way around.

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 20+
- Cloudflare account (for edge deployment)

### Local Development

```bash
# Backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn backend.main:app --reload --port 8000

# Frontend
cd frontend && python -m http.server 3000
```

See full documentation in [docs/](docs/) directory.

## Architecture

Three-tier edge-first system:
1. **Edge Layer**: Cloudflare Workers (routing, caching, WAF)
2. **Application Layer**: FastAPI backend (API, business logic)
3. **Presentation Layer**: Static frontend (HTML/CSS/JS)

Full architecture docs: [docs/architecture/system-design.md](docs/architecture/system-design.md)

## Technology Stack

- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Backend**: FastAPI, Python 3.11+, Uvicorn
- **Edge**: Cloudflare Workers
- **CI/CD**: GitHub Actions
- **Security**: Zero Trust, OWASP headers, WAF

## Links

- **API Docs**: `/api/v1/docs`
- **Security Policy**: [security/policies/zero-trust.md](security/policies/zero-trust.md)
- **Contributing**: [CONTRIBUTING.md](CONTRIBUTING.md)

---

**Built with ◢ by the HackerHardware team**
