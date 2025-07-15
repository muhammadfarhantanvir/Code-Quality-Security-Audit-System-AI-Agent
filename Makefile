# Code Quality & Security Audit System - Makefile

.PHONY: help install test lint format clean docker run dashboard audit

# Default target
help:
	@echo "🔍 Code Quality & Security Audit System"
	@echo "======================================"
	@echo ""
	@echo "Available commands:"
	@echo "  install     - Install dependencies and set up environment"
	@echo "  test        - Run test suite"
	@echo "  lint        - Run code linting"
	@echo "  format      - Format code with black"
	@echo "  clean       - Clean up temporary files"
	@echo "  docker      - Build and run Docker containers"
	@echo "  run         - Run CLI audit on sample project"
	@echo "  dashboard   - Launch Streamlit dashboard"
	@echo "  audit       - Run audit on current directory"
	@echo ""
	@echo "Examples:"
	@echo "  make install"
	@echo "  make test"
	@echo "  make audit DIR=./my-project"
	@echo "  make dashboard"

# Installation
install:
	@echo "📦 Installing dependencies..."
	python -m pip install --upgrade pip
	pip install -r requirements.txt
	@echo "✅ Installation complete!"

install-dev: install
	@echo "🛠️ Installing development dependencies..."
	pip install pytest pytest-cov black flake8 mypy pre-commit
	pre-commit install
	@echo "✅ Development environment ready!"

# Testing
test:
	@echo "🧪 Running tests..."
	pytest tests/ -v --cov=. --cov-report=term-missing

test-verbose:
	@echo "🧪 Running tests with verbose output..."
	pytest tests/ -v -s --cov=. --cov-report=html --cov-report=term-missing

# Code quality
lint:
	@echo "🔍 Running linting..."
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 . --count --exit-zero --max-complexity=10 --max-line-length=100 --statistics

format:
	@echo "🎨 Formatting code..."
	black .
	@echo "✅ Code formatted!"

format-check:
	@echo "🎨 Checking code format..."
	black --check --diff .

type-check:
	@echo "🔍 Running type checking..."
	mypy src/ main.py dashboard.py --ignore-missing-imports

# Cleaning
clean:
	@echo "🧹 Cleaning up..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type f -name ".coverage" -delete
	find . -type d -name "htmlcov" -exec rm -rf {} +
	find . -type f -name "*.log" -delete
	rm -f test_report.json
	rm -rf build/ dist/
	@echo "✅ Cleanup complete!"

# Docker
docker-build:
	@echo "🐳 Building Docker image..."
	docker build -t code-audit-system .

docker-run: docker-build
	@echo "🐳 Running Docker container..."
	docker run -p 8501:8501 -v $(PWD)/projects:/app/projects:ro code-audit-system

docker:
	@echo "🐳 Starting Docker Compose..."
	docker-compose up -d
	@echo "✅ Dashboard available at http://localhost:8501"

docker-stop:
	@echo "🐳 Stopping Docker containers..."
	docker-compose down

# Application
dashboard:
	@echo "🚀 Starting dashboard..."
	streamlit run dashboard.py

run:
	@echo "🔍 Running audit on sample project..."
	python main.py --directory assets/examples --verbose

audit:
	@echo "🔍 Running audit..."
ifdef DIR
	python main.py --directory $(DIR) --verbose
else
	python main.py --directory . --verbose
endif

audit-json:
	@echo "🔍 Running audit with JSON output..."
ifdef DIR
	python main.py --directory $(DIR) --output audit_report.json
else
	python main.py --directory . --output audit_report.json
endif
	@echo "📄 Report saved to audit_report.json"

audit-html:
	@echo "🔍 Running audit with HTML output..."
ifdef DIR
	python main.py --directory $(DIR) --export-html
else
	python main.py --directory . --export-html
endif

# Development
dev-setup: install-dev
	@echo "🛠️ Setting up development environment..."
	mkdir -p sample_project
	echo 'query = f"SELECT * FROM users WHERE id = {user_id}"' > sample_project/vulnerable.py
	echo 'password = "hardcoded_secret"' >> sample_project/vulnerable.py
	@echo "✅ Development environment ready!"

# CI/CD simulation
ci: format-check lint type-check test
	@echo "✅ All CI checks passed!"

# Release preparation
build:
	@echo "📦 Building package..."
	python -m build
	@echo "✅ Package built in dist/"

release-check: ci build
	@echo "🚀 Release checks complete!"

# Ollama management
ollama-install:
	@echo "🤖 Installing Ollama..."
	curl -fsSL https://ollama.ai/install.sh | sh

ollama-models:
	@echo "📥 Downloading AI models..."
	ollama pull deepseek-coder:6.7b &
	ollama pull deepseek-r1:1.5b &
	ollama pull deepscaler &
	wait
	@echo "✅ Models downloaded!"

ollama-start:
	@echo "🤖 Starting Ollama service..."
	ollama serve &

# Documentation
docs:
	@echo "📚 Generating documentation..."
	@echo "Available documentation:"
	@echo "  - README.md: Main documentation"
	@echo "  - GETTING_STARTED.md: Quick start guide"
	@echo "  - CONTRIBUTING.md: Contribution guidelines"
	@echo "  - CHANGELOG.md: Version history"

# Monitoring
status:
	@echo "📊 System Status:"
	@echo "Python version: $(shell python --version)"
	@echo "Pip version: $(shell pip --version)"
	@echo "Ollama status: $(shell curl -s http://localhost:11434/api/tags > /dev/null && echo 'Running' || echo 'Not running')"
	@echo "Virtual environment: $(shell echo $$VIRTUAL_ENV)"

# Performance testing
perf-test:
	@echo "⚡ Running performance tests..."
	time python main.py --directory assets/examples --no-ai
	@echo "✅ Performance test complete!"

# Security testing
security-test:
	@echo "🔒 Running security tests..."
	python -m bandit -r . -f json -o security_report.json || true
	@echo "📄 Security report saved to security_report.json"

# All-in-one commands
setup: install dev-setup ollama-models
	@echo "🎉 Complete setup finished!"

full-test: ci perf-test security-test
	@echo "🎯 Full test suite complete!"

demo: setup
	@echo "🎬 Running demo..."
	make run
	@echo "🎉 Demo complete! Try 'make dashboard' next."