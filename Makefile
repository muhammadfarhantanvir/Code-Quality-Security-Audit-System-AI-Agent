.PHONY: help setup install deps audit dashboard test clean docker docker-prod vercel deploy-all

# Default target
help:
	@echo "🤖 Code Quality & Security Audit System - Make Commands"
	@echo ""
	@echo "Usage:"
	@echo "  make setup          - Setup development environment"
	@echo "  make install        - Install dependencies"
	@echo "  make deps           - Install dependencies (alias for install)"
	@echo "  make audit          - Run code audit on current directory"
	@echo "  make dashboard      - Launch web dashboard"
	@echo "  make test           - Run tests"
	@echo "  make clean          - Clean temporary files"
	@echo "  make docker         - Build and run with Docker"
	@echo "  make docker-prod    - Build and run production Docker setup"
	@echo "  make vercel         - Prepare for Vercel deployment"
	@echo "  make deploy-all     - Deploy to all platforms (Docker + Vercel)"
	@echo ""

# Setup development environment
setup: install
	@echo "🔧 Setting up development environment..."
	pip install -e .

# Install dependencies
install deps:
	@echo "📦 Installing dependencies..."
	pip install -r requirements.txt

# Run code audit
audit:
	@echo "🔍 Running code audit on current directory..."
	python main.py --directory . --verbose

# Launch dashboard
dashboard:
	@echo "🎨 Launching dashboard..."
	streamlit run app.py

# Run tests
test:
	@echo "🧪 Running tests..."
	pytest tests/ -v

# Clean temporary files
clean:
	@echo "🧹 Cleaning temporary files..."
	rm -rf __pycache__/
	rm -rf *.pyc
	rm -rf */__pycache__/
	rm -rf */*.pyc
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/

# Docker commands
docker:
	@echo "🐳 Building and running with Docker..."
	docker-compose up -d

docker-prod:
	@echo "🐳 Building and running production Docker setup..."
	docker-compose -f docker-compose.prod.yml up -d

docker-build:
	@echo "🐳 Building Docker image..."
	docker build -t code-audit-system .

docker-build-prod:
	@echo "🐳 Building production Docker image..."
	docker build -f Dockerfile.prod -t code-audit-system .

# Vercel commands
vercel:
	@echo "🌐 Preparing for Vercel deployment..."
	@if [ ! -f "vercel.json" ]; then \
		echo '{"version": 2, "builds": [{"src": "app.py", "use": "@vercel/python", "config": {"runtime": "python3.11"}}], "routes": [{"src": "/(.*)", "dest": "app.py"}], "env": {"STREAMLIT_SERVER_PORT": "3000", "STREAMLIT_SERVER_ADDRESS": "0.0.0.0", "PYTHONPATH": "."}}' > vercel.json; \
	fi
	@echo "Vercel configuration created. Run 'vercel --prod' to deploy."

# Deploy to all platforms
deploy-all: docker vercel
	@echo "🚀 Deployment to all platforms completed!"
	@echo "Docker: http://localhost:8501"
	@echo "Vercel: Deploy with 'vercel --prod'"