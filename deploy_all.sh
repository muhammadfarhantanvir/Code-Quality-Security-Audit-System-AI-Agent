#!/bin/bash
# Comprehensive deployment script for Code Quality & Security Audit System
# Deploys to both Docker and Vercel

set -e  # Exit on any error

echo "🚀 Starting comprehensive deployment for Code Quality & Security Audit System..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
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

print_header() {
    echo -e "${BLUE}[HEADER]${NC} $1"
}

# Parse command line arguments
DEPLOY_DOCKER=false
DEPLOY_VERCEL=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --docker)
            DEPLOY_DOCKER=true
            shift
            ;;
        --vercel)
            DEPLOY_VERCEL=true
            shift
            ;;
        --all)
            DEPLOY_DOCKER=true
            DEPLOY_VERCEL=true
            shift
            ;;
        *)
            echo "Unknown option: $1"
            echo "Usage: $0 [--docker] [--vercel] [--all]"
            exit 1
            ;;
    esac
done

# If no options provided, default to all
if [ "$DEPLOY_DOCKER" = false ] && [ "$DEPLOY_VERCEL" = false ]; then
    DEPLOY_DOCKER=true
    DEPLOY_VERCEL=true
fi

# Check prerequisites for Docker
if [ "$DEPLOY_DOCKER" = true ]; then
    print_header "Checking Docker prerequisites..."
    
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
    
    print_status "Docker prerequisites check passed!"
fi

# Check prerequisites for Vercel
if [ "$DEPLOY_VERCEL" = true ]; then
    print_header "Checking Vercel prerequisites..."
    
    if ! command -v vercel &> /dev/null; then
        print_error "Vercel CLI is not installed. Please install with: npm install -g vercel"
        exit 1
    fi
    
    print_status "Vercel CLI is available."
fi

# Docker deployment
if [ "$DEPLOY_DOCKER" = true ]; then
    print_header "Starting Docker deployment..."
    
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
        print_status "✅ Docker services are running successfully!"
        echo ""
        print_status "Docker Application is available at: http://localhost:8501"
        if [ "$DEPLOYMENT_TYPE" = "production" ]; then
            print_status "Nginx is available at: http://localhost"
        fi
        echo ""
        print_status "To view Docker logs: $DOCKER_COMPOSE_CMD -f $COMPOSE_FILE logs -f"
        print_status "To stop Docker services: $DOCKER_COMPOSE_CMD -f $COMPOSE_FILE down"
    else
        print_error "❌ Docker services failed to start properly."
        print_status "Check Docker logs with: $DOCKER_COMPOSE_CMD -f $COMPOSE_FILE logs"
        exit 1
    fi
    
    print_status "🎉 Docker deployment completed successfully!"
    echo ""
fi

# Vercel deployment
if [ "$DEPLOY_VERCEL" = true ]; then
    print_header "Starting Vercel deployment..."
    
    # Check if user is logged in to Vercel
    if ! vercel whoami &> /dev/null; then
        print_warning "Not logged in to Vercel. Initiating login..."
        vercel login
    fi
    
    # Verify vercel.json exists
    if [ ! -f "vercel.json" ]; then
        print_warning "vercel.json not found. Creating default configuration..."
        cat > vercel.json << EOF
{
  "version": 2,
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python",
      "config": { "runtime": "python3.11" }
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ],
  "env": {
    "STREAMLIT_SERVER_PORT": "3000",
    "STREAMLIT_SERVER_ADDRESS": "0.0.0.0",
    "PYTHONPATH": "."
  }
}
EOF
        print_status "Created default vercel.json configuration."
    fi
    
    # Deploy to Vercel
    print_status "Deploying to Vercel..."
    vercel --prod
    
    print_status "🎉 Vercel deployment completed successfully!"
    print_status "Your application is now live on Vercel!"
    echo ""
fi

print_header "🎉 Comprehensive deployment completed successfully!"
if [ "$DEPLOY_DOCKER" = true ]; then
    print_status "Docker: http://localhost:8501"
fi
if [ "$DEPLOY_VERCEL" = true ]; then
    print_status "Vercel: Check your Vercel dashboard for the deployment URL"
fi