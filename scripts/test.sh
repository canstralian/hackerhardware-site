#!/bin/bash
# Test script for HackerHardware.net

set -e

echo "🧪 Running tests..."

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Activate virtual environment
cd api
if [ -d "venv" ]; then
    source venv/bin/activate 2>/dev/null || . venv/bin/activate 2>/dev/null
fi

# Run linting
echo "Running code quality checks..."
echo "  - flake8"
pip install -q flake8
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics || {
    echo "${RED}✗ Linting failed${NC}"
    exit 1
}
echo "${GREEN}✓ Linting passed${NC}"

# Run security scan
echo "Running security scan..."
echo "  - bandit"
pip install -q bandit
bandit -r . -ll -q || {
    echo "${RED}✗ Security scan found issues${NC}"
    exit 1
}
echo "${GREEN}✓ Security scan passed${NC}"

# Test API
cd ..
echo "Testing API endpoints..."

if ! curl -f http://localhost:8000/api/v1/health &> /dev/null; then
    echo "${YELLOW}⚠ API not running, starting services...${NC}"
    docker-compose up -d
    sleep 10
fi

# Test health endpoint
if curl -f http://localhost:8000/api/v1/health &> /dev/null; then
    echo "${GREEN}✓ Health endpoint OK${NC}"
else
    echo "${RED}✗ Health endpoint failed${NC}"
    exit 1
fi

# Test root endpoint
if curl -f http://localhost:8000/ &> /dev/null; then
    echo "${GREEN}✓ Root endpoint OK${NC}"
else
    echo "${RED}✗ Root endpoint failed${NC}"
    exit 1
fi

echo ""
echo "${GREEN}🎉 All tests passed!${NC}"
