#!/bin/bash
# Automated Docker deployment script for Code Quality & Security Audit System

set -e  # Exit on any error

echo "🚀 Starting automated Docker deployment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check prerequisites
print_status "Checking prerequisites..."

if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    print_warning "Docker Compose is not installed. Trying 'docker compose' instead..."
    if ! docker compose version &> /dev/null; then
        print_error "Neither 'docker-compose' nor 'docker compose' is available."
        exit 1
    fi
    DOCKER_COMPOSE_CMD="docker compose"
else
    DOCKER_COMPOSE_CMD="docker-compose"
fi

print_status "Prerequisites check passed!"

# Build the Docker image
print_status "Building Docker image..."
if [ -f "Dockerfile.prod" ]; then
    $DOCKER_COMPOSE_CMD -f docker-compose.prod.yml build
    DEPLOYMENT_TYPE="production"
    COMPOSE_FILE="docker-compose.prod.yml"
else
    $DOCKER_COMPOSE_CMD build
    DEPLOYMENT_TYPE="development"
    COMPOSE_FILE="docker-compose.yml"
fi

# Start the services
print_status "Starting $DEPLOYMENT_TYPE services..."
$DOCKER_COMPOSE_CMD -f $COMPOSE_FILE up -d

# Wait for services to be ready
print_status "Waiting for services to start..."
sleep 15

# Check if the main service is running
if $DOCKER_COMPOSE_CMD -f $COMPOSE_FILE ps | grep -q "Up"; then
    print_status "✅ Services are running successfully!"
    echo ""
    print_status "Application is available at: http://localhost:8501"
    if [ "$DEPLOYMENT_TYPE" = "production" ]; then
        print_status "Nginx is available at: http://localhost"
    fi
    echo ""
    print_status "To view logs: $DOCKER_COMPOSE_CMD -f $COMPOSE_FILE logs -f"
    print_status "To stop services: $DOCKER_COMPOSE_CMD -f $COMPOSE_FILE down"
else
    print_error "❌ Services failed to start properly."
    print_status "Check logs with: $DOCKER_COMPOSE_CMD -f $COMPOSE_FILE logs"
    exit 1
fi

print_status "🎉 Docker deployment completed successfully!"