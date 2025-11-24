#!/bin/bash
# Test script for HackerHardware.net

set -e

echo "🧪 Running tests..."

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Function to print colored messages
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

# Function to install Python dependency with error handling
install_dependency() {
    local package=$1
    echo "  - Installing $package..."
    if ! pip install -q "$package" 2>&1; then
        print_error "Failed to install $package"
        return 1
    fi
    return 0
}

# Function to activate virtual environment
activate_venv() {
    if [ -d "venv" ]; then
        # Try to activate venv with fallback methods
        if source venv/bin/activate 2>/dev/null; then
            return 0
        elif . venv/bin/activate 2>/dev/null; then
            return 0
        else
            print_warning "Failed to activate virtual environment"
            return 1
        fi
    else
        print_warning "Virtual environment not found"
        return 1
    fi
}

# Navigate to api directory
cd api || {
    print_error "Failed to change to api directory"
    exit 1
}

# Activate virtual environment
activate_venv || print_warning "Continuing without virtual environment..."

# Run linting
echo "Running code quality checks..."
if ! install_dependency flake8; then
    print_error "Failed to install linting dependencies"
    exit 1
fi

echo "  - Running flake8..."
if flake8 . --exclude=venv --count --select=E9,F63,F7,F82 \
    --show-source --statistics; then
    print_success "Linting passed"
else
    print_error "Linting failed"
    exit 1
fi

# Run security scan
echo "Running security scan..."
if ! install_dependency bandit; then
    print_error "Failed to install security scan dependencies"
    exit 1
fi

echo "  - Running bandit..."
if bandit -r . -lll -q --exclude ./venv; then
    print_success "Security scan passed"
else
    print_error "Security scan found issues"
    exit 1
fi

# Test API
cd .. || {
    print_error "Failed to return to root directory"
    exit 1
}

echo "Testing API endpoints..."

# Check if API is running
if ! curl -f http://localhost:8000/api/v1/health &> /dev/null; then
    print_warning "API not running, starting services..."
    if command -v docker-compose &> /dev/null; then
        docker-compose up -d
        sleep 10
    else
        print_warning "docker-compose not found, skipping API startup"
        print_warning "Please start the API manually to run endpoint tests"
        echo ""
        print_success "Code quality and security tests passed!"
        exit 0
    fi
fi

# Test health endpoint with retry
MAX_RETRIES=3
RETRY_COUNT=0
while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
    if curl -f http://localhost:8000/api/v1/health &> /dev/null; then
        print_success "Health endpoint OK"
        break
    else
        RETRY_COUNT=$((RETRY_COUNT + 1))
        if [ $RETRY_COUNT -eq $MAX_RETRIES ]; then
            print_error "Health endpoint failed after $MAX_RETRIES attempts"
            exit 1
        fi
        print_warning "Retry $RETRY_COUNT/$MAX_RETRIES..."
        sleep 2
    fi
done

# Test root endpoint
if curl -f http://localhost:8000/ &> /dev/null; then
    print_success "Root endpoint OK"
else
    print_error "Root endpoint failed"
    exit 1
fi

echo ""
print_success "🎉 All tests passed!"
