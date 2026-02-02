#!/bin/bash
# Vercel deployment script for Code Quality & Security Audit System

set -e  # Exit on any error

echo "🚀 Starting Vercel deployment..."

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

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    print_error "Vercel CLI is not installed. Installing now..."
    npm install -g vercel
fi

print_status "Vercel CLI is available."

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