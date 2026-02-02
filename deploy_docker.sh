#!/bin/bash
# Docker deployment script for Code Quality & Security Audit System

set -e  # Exit on any error

echo "🚀 Starting Docker deployment for Code Quality & Security Audit System..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if docker-compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "⚠️  Docker Compose is not installed. Using 'docker compose' instead..."
    DOCKER_COMPOSE_CMD="docker compose"
else
    DOCKER_COMPOSE_CMD="docker-compose"
fi

# Build and start the services
echo "🔨 Building Docker images..."
$DOCKER_COMPOSE_CMD build

echo "🐳 Starting services..."
$DOCKER_COMPOSE_CMD up -d

echo "✅ Deployment completed!"
echo "🌐 Access the application at http://localhost:8501"
echo "🔧 Ollama API is available at http://localhost:11434"

# Wait a bit for services to start
sleep 10

# Show service status
echo "📈 Service status:"
$DOCKER_COMPOSE_CMD ps

echo ""
echo "📝 To view logs: $DOCKER_COMPOSE_CMD logs -f"
echo "🛑 To stop services: $DOCKER_COMPOSE_CMD down"