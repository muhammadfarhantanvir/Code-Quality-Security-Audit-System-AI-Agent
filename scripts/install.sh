#!/bin/bash

# Code Quality & Security Audit System - Installation Script
# This script automates the installation process

set -e  # Exit on any error

echo "🔍 Code Quality & Security Audit System - Installation"
echo "=================================================="

# Check Python version
python_version=$(python3 --version 2>&1 | grep -oP '\d+\.\d+' | head -1)
required_version="3.9"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Python 3.9+ is required. Found: $python_version"
    exit 1
fi

echo "✅ Python version check passed: $python_version"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📥 Installing Python dependencies..."
pip install -r requirements.txt

# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo "🤖 Ollama not found. Installing Ollama..."
    
    # Detect OS and install Ollama
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        curl -fsSL https://ollama.ai/install.sh | sh
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "Please install Ollama manually from https://ollama.ai/download"
        echo "Or use: brew install ollama"
    else
        echo "Please install Ollama manually from https://ollama.ai/download"
    fi
else
    echo "✅ Ollama is already installed"
fi

# Start Ollama service (Linux)
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "🚀 Starting Ollama service..."
    systemctl --user enable ollama
    systemctl --user start ollama
fi

# Wait for Ollama to be ready
echo "⏳ Waiting for Ollama to be ready..."
timeout=60
while ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; do
    sleep 2
    timeout=$((timeout - 2))
    if [ $timeout -le 0 ]; then
        echo "⚠️  Ollama service not responding. You may need to start it manually:"
        echo "   ollama serve"
        break
    fi
done

if [ $timeout -gt 0 ]; then
    echo "✅ Ollama service is running"
    
    # Pull required models
    echo "📥 Downloading AI models (this may take a while)..."
    ollama pull deepseek-coder:6.7b &
    ollama pull deepseek-r1:1.5b &
    ollama pull deepscaler &
    wait
    
    echo "✅ AI models downloaded successfully"
fi

# Create sample project for testing
echo "📁 Creating sample project..."
mkdir -p sample_project
cat > sample_project/vulnerable_app.py << 'EOF'
import os
import sqlite3

# Vulnerable code examples for testing
def unsafe_query(user_id):
    # SQL Injection vulnerability
    query = f"SELECT * FROM users WHERE id = {user_id}"
    return query

def hardcoded_secret():
    # Hardcoded secret
    api_key = "sk-1234567890abcdef"
    return api_key

def command_injection(filename):
    # Command injection vulnerability
    os.system(f"cat {filename}")

def xss_vulnerability(user_input):
    # XSS vulnerability
    return f"<div>{user_input}</div>"

# Quality issues
def very_long_function_with_many_parameters(param1, param2, param3, param4, param5, param6, param7, param8):
    # TODO: Refactor this function
    result = 0
    for i in range(100):
        if i % 2 == 0:
            if i % 4 == 0:
                if i % 8 == 0:
                    result += i * param1
                else:
                    result += i * param2
            else:
                result += i * param3
        else:
            result += i * param4
    return result
EOF

echo "✅ Sample project created"

# Test installation
echo "🧪 Testing installation..."
python3 code_auditor.py --directory sample_project --output test_report.json

if [ -f "test_report.json" ]; then
    echo "✅ Installation test passed!"
    rm test_report.json
else
    echo "❌ Installation test failed"
    exit 1
fi

echo ""
echo "🎉 Installation completed successfully!"
echo ""
echo "Quick Start:"
echo "1. Activate virtual environment: source venv/bin/activate"
echo "2. Run CLI audit: python3 code_auditor.py --directory /path/to/your/project"
echo "3. Launch dashboard: streamlit run app.py"
echo "4. Open browser: http://localhost:8501"
echo ""
echo "For Docker users:"
echo "1. docker-compose up -d"
echo "2. Open browser: http://localhost:8501"
echo ""
echo "Documentation: README.md"
echo "Support: https://github.com/muhammadfarhantanvir/Code-Quality-Security-Audit-System-AI-Agent/issues"