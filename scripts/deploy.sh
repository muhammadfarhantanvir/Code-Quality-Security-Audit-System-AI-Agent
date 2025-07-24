#!/bin/bash

# Deployment script for Code Quality & Security Audit System

set -e

echo "🚀 Starting deployment process..."

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    echo "❌ Error: pyproject.toml not found. Please run from project root."
    exit 1
fi

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf build/ dist/ *.egg-info/

# Run tests
echo "🧪 Running tests..."
python -m pytest tests/ -v

# Build package
echo "📦 Building package..."
python -m build

# Check package
echo "🔍 Checking package..."
python -m twine check dist/*

echo "✅ Package built successfully!"
echo ""
echo "Next steps:"
echo "1. Upload to PyPI: twine upload dist/*"
echo "2. Create GitHub release: gh release create v1.0.0"
echo "3. Deploy Docker image: docker build -t code-audit-system ."
echo ""
echo "🎉 Ready for deployment!"