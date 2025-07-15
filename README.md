# 🔍 Code Quality & Security Audit System

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![Version](https://img.shields.io/badge/version-1.0.0-green.svg)

An AI-powered code quality and security audit system that combines pattern-based analysis with local AI models to identify vulnerabilities, code quality issues, and provide actionable recommendations.

![Code Quality Dashboard](assets/images/code%20quality.png)

## ✨ Features

- 🔒 **Security Analysis**: OWASP Top 10 vulnerability detection
- 📊 **Code Quality**: Maintainability and complexity analysis  
- 🤖 **AI-Powered**: Local Ollama integration for advanced insights
- 🌐 **Web Dashboard**: Interactive Streamlit interface
- 💻 **CLI Tool**: Comprehensive command-line interface
- 📈 **Historical Tracking**: Trend analysis and reporting
- 🐳 **Docker Ready**: Containerized deployment
- 🔧 **Configurable**: Customizable patterns and thresholds

## 🚀 Quick Start

### Option 1: One-Command Installation

**Linux/macOS:**
```bash
curl -fsSL https://raw.githubusercontent.com/muhammadfarhantanvir/Code-Quality-Security-Audit-System-AI-Agent/main/scripts/install.sh | bash
```

**Windows:**
```powershell
iwr -useb https://raw.githubusercontent.com/muhammadfarhantanvir/Code-Quality-Security-Audit-System-AI-Agent/main/scripts/install.bat | iex
```

### Option 2: Docker (Recommended)

```bash
git clone https://github.com/muhammadfarhantanvir/Code-Quality-Security-Audit-System-AI-Agent
cd Code-Quality-Security-Audit-System-AI-Agent
docker-compose -f docker/docker-compose.yml up -d
```

Open http://localhost:8501 in your browser.

### Option 3: Manual Installation

```bash
# Clone repository
git clone https://github.com/muhammadfarhantanvir/Code-Quality-Security-Audit-System-AI-Agent
cd Code-Quality-Security-Audit-System-AI-Agent

# Install dependencies
pip install -r requirements.txt

# Run CLI audit
python main.py --directory /path/to/your/project

# Launch dashboard
streamlit run dashboard.py
```

## 💻 Usage

### Command Line Interface

```bash
# Basic audit
python main.py --directory ./my-project

# Generate reports
python main.py --directory ./my-project --output report.json --export-html

# Filter by severity
python main.py --directory ./my-project --severity HIGH --verbose

# Disable AI for faster scanning
python main.py --directory ./my-project --no-ai
```

### Web Dashboard

```bash
streamlit run dashboard.py
```

Then open http://localhost:8501 and enter your project path.

### Using Make Commands

```bash
# Setup everything
make setup

# Run audit on current directory
make audit

# Launch dashboard
make dashboard

# Run tests
make test

# See all commands
make help
```

## 📁 Project Structure

```
Code-Quality-Security-Audit-System-AI-Agent/
├── src/code_audit_system/          # Main package
│   ├── core/                       # Core functionality
│   │   ├── auditor.py             # Main auditor class
│   │   ├── models.py              # Data models
│   │   └── patterns.py            # Security/quality patterns
│   ├── ai/                        # AI integration
│   │   └── ollama_client.py       # Ollama client
│   ├── dashboard/                 # Web interface
│   │   └── streamlit_app.py       # Streamlit dashboard
│   └── cli/                       # Command-line interface
│       └── main.py                # CLI implementation
├── config/                        # Configuration files
├── docs/                          # Documentation
├── scripts/                       # Installation scripts
├── docker/                        # Docker configuration
├── tests/                         # Test suite
├── assets/                        # Images and examples
├── main.py                        # CLI entry point
├── dashboard.py                   # Dashboard entry point
└── Makefile                       # Project management
```

## 🔍 What It Detects

### Security Issues
- SQL Injection vulnerabilities
- Cross-Site Scripting (XSS)
- Hardcoded secrets and passwords
- Command injection flaws
- Insecure communication (HTTP)
- Path traversal vulnerabilities
- Weak cryptography usage
- And more OWASP Top 10 issues...

### Code Quality Issues
- Long and complex functions
- Code duplication
- Missing documentation
- Poor error handling
- Magic numbers
- Deep nesting
- And more maintainability issues...

## 🤖 AI Integration

The system integrates with local Ollama models for advanced analysis:

- **DeepSeek Coder**: Code security analysis
- **DeepSeek R1**: Strategic recommendations
- **DeepScaler**: Technical debt prediction

Install Ollama and pull models:
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull models
ollama pull deepseek-coder:6.7b
ollama pull deepseek-r1:1.5b
ollama pull deepscaler
```

## 📊 Supported Languages

- Python (.py)
- JavaScript/TypeScript (.js, .jsx, .ts, .tsx)
- Java (.java)
- C/C++ (.c, .cpp)
- PHP (.php)
- Ruby (.rb)
- Go (.go)
- Rust (.rs)
- C# (.cs)
- Swift (.swift)

## 🔧 Configuration

Customize the system via `config/config.yaml`:

```yaml
# Scanning options
scanning:
  max_file_size: 2000
  exclude_patterns:
    - "*/node_modules/*"
    - "*/venv/*"

# AI settings
ollama:
  base_url: "http://localhost:11434"
  timeout: 60

# Security patterns (customizable)
security:
  severity_weights:
    CRITICAL: 15
    HIGH: 10
    MEDIUM: 5
```

## 📈 Example Output

```bash
🔍 Code Quality & Security Audit System v1.0.0
==================================================
📁 Scanning directory: ./my-project

✅ Audit completed in 3.45 seconds!
📊 Files scanned: 25
📏 Total lines: 2,847
🔐 Security issues: 3
📊 Quality issues: 12
⚠️  Risk score: 45.2/100
🟡 MEDIUM RISK - Review and address issues

🔴 Top Security Issues:
  1. HIGH - SQL Injection in database.py:42
  2. MEDIUM - Hardcoded Secret in config.py:15
  3. MEDIUM - XSS Vulnerability in views.py:128

💡 Recommendations:
  1. URGENT: Address 1 high-severity security vulnerabilities immediately
  2. Implement security code review process
  3. Refactor code to improve maintainability
```

## 🧪 Testing

```bash
# Run all tests
make test

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific tests
pytest tests/test_security_patterns.py -v
```

## 🤝 Contributing

We welcome contributions! See [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md) for guidelines.

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📚 Documentation

- [Getting Started Guide](docs/GETTING_STARTED.md) - Comprehensive setup guide
- [Contributing Guidelines](docs/CONTRIBUTING.md) - How to contribute
- [Changelog](docs/CHANGELOG.md) - Version history
- [Configuration Reference](config/config.yaml) - All configuration options

## 🐳 Docker Deployment

```bash
# Build and run
docker-compose -f docker/docker-compose.yml up -d

# Scale services
docker-compose -f docker/docker-compose.yml up -d --scale code-audit-system=3

# View logs
docker-compose -f docker/docker-compose.yml logs -f
```

## 🔒 Security

This tool runs entirely locally - no data is sent to external services. AI analysis uses local Ollama models for privacy and security.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OWASP for security vulnerability classifications
- The Ollama team for local AI model infrastructure
- The open-source security community

## 📞 Support

- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/muhammadfarhantanvir/Code-Quality-Security-Audit-System-AI-Agent/issues)
- 💡 **Feature Requests**: [GitHub Discussions](https://github.com/muhammadfarhantanvir/Code-Quality-Security-Audit-System-AI-Agent/discussions)
- 📖 **Documentation**: [Getting Started Guide](docs/GETTING_STARTED.md)

---

<div align="center">
  <p><strong>Made with ❤️ for the developer community</strong></p>
  <p>⭐ Star this repo if you find it useful!</p>
</div>