#!/bin/bash
# Setup script for HackerHardware.net

set -e

echo "🚀 Setting up HackerHardware.net..."

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check prerequisites
echo "Checking prerequisites..."

if ! command -v docker &> /dev/null; then
    echo "${YELLOW}Docker not found. Please install Docker first.${NC}"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "${YELLOW}Docker Compose not found. Please install Docker Compose first.${NC}"
    exit 1
fi

if ! command -v python3 &> /dev/null; then
    echo "${YELLOW}Python 3 not found. Please install Python 3.9+ first.${NC}"
    exit 1
fi

echo "${GREEN}✓ Prerequisites met${NC}"

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cp .env.example .env
    
    # Generate a random secret key
    SECRET_KEY=$(openssl rand -hex 32)
    sed -i "s/change-this-to-a-random-secret-key/$SECRET_KEY/" .env
    
    echo "${GREEN}✓ .env file created${NC}"
else
    echo "${YELLOW}⚠ .env file already exists${NC}"
fi

# Create certificates directory
echo "Setting up certificates directory..."
mkdir -p certs
if [ ! -f certs/server.crt ]; then
    echo "Generating self-signed certificates for development..."
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
        -keyout certs/server.key \
        -out certs/server.crt \
        -subj "/C=US/ST=State/L=City/O=HackerHardware/CN=localhost" \
        2>/dev/null
    echo "${GREEN}✓ Certificates generated${NC}"
else
    echo "${YELLOW}⚠ Certificates already exist${NC}"
fi

# Install Python dependencies for API
echo "Installing API dependencies..."
cd api
python3 -m venv venv 2>/dev/null || true
source venv/bin/activate 2>/dev/null || . venv/bin/activate 2>/dev/null || true
pip install -q --upgrade pip
pip install -q -r requirements.txt
deactivate 2>/dev/null || true
cd ..
echo "${GREEN}✓ API dependencies installed${NC}"

# Build Docker images
echo "Building Docker images..."
docker-compose build
echo "${GREEN}✓ Docker images built${NC}"

# Start services
echo "Starting services..."
docker-compose up -d
echo "${GREEN}✓ Services started${NC}"

# Wait for services to be ready
echo "Waiting for services to be ready..."
sleep 10

# Check health
if curl -f http://localhost:8000/api/v1/health &> /dev/null; then
    echo "${GREEN}✓ API is healthy${NC}"
else
    echo "${YELLOW}⚠ API health check failed${NC}"
fi

echo ""
echo "${GREEN}🎉 Setup complete!${NC}"
echo ""
echo "Services running:"
echo "  - API:        http://localhost:8000"
echo "  - Prometheus: http://localhost:9090"
echo "  - Grafana:    http://localhost:3001"
echo ""
echo "To view logs:"
echo "  docker-compose logs -f"
echo ""
echo "To stop services:"
echo "  docker-compose down"
