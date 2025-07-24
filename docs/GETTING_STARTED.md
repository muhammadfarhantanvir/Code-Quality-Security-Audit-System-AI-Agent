# 🚀 Getting Started with Code Quality & Security Audit System

Welcome! This guide will help you get up and running with the Code Quality & Security Audit System in just a few minutes.

## 📋 Prerequisites

Before you begin, ensure you have:
- **Python 3.9+** installed ([Download here](https://python.org))
- **Git** installed ([Download here](https://git-scm.com))
- **4GB+ RAM** (for AI models)
- **2GB+ free disk space**

## ⚡ Quick Start (5 minutes)

### Option 1: One-Command Installation

**Linux/macOS:**
```bash
curl -fsSL https://raw.githubusercontent.com/muhammadfarhantanvir/Code-Quality-Security-Audit-System-AI-Agent/main/install.sh | bash
```

**Windows (PowerShell):**
```powershell
iwr -useb https://raw.githubusercontent.com/muhammadfarhantanvir/Code-Quality-Security-Audit-System-AI-Agent/main/install.bat | iex
```

### Option 2: Docker (Recommended for beginners)

```bash
# Clone and start
git clone https://github.com/muhammadfarhantanvir/Code-Quality-Security-Audit-System-AI-Agent
cd Code-Quality-Security-Audit-System-AI-Agent
docker-compose up -d

# Open dashboard
open http://localhost:8501
```

## 🎯 Your First Audit

### 1. Create a Test Project
```bash
mkdir my-test-project
cd my-test-project

# Create a file with some vulnerabilities
cat > vulnerable_app.py << 'EOF'
import os

def unsafe_login(username, password):
    # SQL Injection vulnerability
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    
    # Hardcoded secret
    api_key = "sk-1234567890abcdef"
    
    # Command injection
    os.system(f"echo 'Login attempt: {username}'")
    
    return query

def long_function_with_issues():
    # This function is too long and complex
    result = 0
    for i in range(100):
        if i % 2 == 0:
            if i % 4 == 0:
                if i % 8 == 0:
                    result += i
                else:
                    result -= i
            else:
                result *= 2
        else:
            result += 1
    return result
EOF
```

### 2. Run Your First Audit

**Command Line:**
```bash
python code_auditor.py --directory my-test-project
```

**Web Dashboard:**
```bash
streamlit run app.py
# Then open http://localhost:8501 and enter 'my-test-project'
```

### 3. Understanding Results

You should see output like:
```
🔍 Code Quality & Security Audit System v1.0.0
==================================================
📁 Scanning directory: my-test-project

✅ Audit completed in 2.34 seconds!
📊 Files scanned: 1
📏 Total lines: 25
🔐 Security issues: 3
📊 Quality issues: 2
⚠️  Risk score: 85.5/100
🔴 HIGH RISK - Immediate attention required!
```

## 🔧 Configuration

### Basic Configuration
Create `config.yaml` in your project:
```yaml
# Scanning options
scanning:
  max_file_size: 5000
  exclude_patterns:
    - "*/node_modules/*"
    - "*/venv/*"
    - "*/.git/*"

# AI settings
ollama:
  base_url: "http://localhost:11434"
  timeout: 60

# Reporting
reporting:
  export_formats:
    - json
    - html
    - csv
```

### Environment Variables
```bash
export OLLAMA_HOST=http://localhost:11434
export AUDIT_DB_PATH=./custom_audit.db
export AUDIT_LOG_LEVEL=INFO
```

## 🎨 Dashboard Features

### Main Dashboard
- **Risk Score**: Overall security and quality assessment
- **Issue Distribution**: Visual breakdown of problems
- **File Analysis**: Per-file detailed reports
- **Historical Trends**: Track improvements over time

### Key Sections
1. **Security Issues**: Vulnerabilities with severity levels
2. **Quality Issues**: Code maintainability problems
3. **Recommendations**: Prioritized action items
4. **Compliance**: Standards adherence (PCI-DSS, SOX, etc.)

## 📊 CLI Commands Reference

### Basic Commands
```bash
# Simple audit
code-audit --directory /path/to/project

# With output file
code-audit --directory /path/to/project --output report.json

# Filter by severity
code-audit --directory /path/to/project --severity HIGH

# Multiple export formats
code-audit --directory /path/to/project --export-html --export-csv
```

### Advanced Commands
```bash
# Verbose output
code-audit --directory /path/to/project --verbose

# Security issues only
code-audit --directory /path/to/project --type security

# Disable AI (faster)
code-audit --directory /path/to/project --no-ai

# Custom Ollama server
code-audit --directory /path/to/project --ollama-url http://remote:11434
```

## 🔍 Understanding Security Issues

### Severity Levels
- **🔴 CRITICAL**: Immediate security risk (data breach potential)
- **🟠 HIGH**: Significant vulnerability (should fix within days)
- **🟡 MEDIUM**: Moderate risk (fix within weeks)
- **🟢 LOW**: Minor issue (fix when convenient)

### Common Issues Detected
1. **SQL Injection**: Unsafe database queries
2. **XSS**: Cross-site scripting vulnerabilities
3. **Hardcoded Secrets**: Passwords/keys in code
4. **Command Injection**: Unsafe system commands
5. **Path Traversal**: File access vulnerabilities

## 📈 Quality Metrics

### Code Quality Issues
- **Long Functions**: Functions over 50 lines
- **Complex Logic**: High cyclomatic complexity
- **Code Duplication**: Repeated code blocks
- **Missing Documentation**: Functions without docstrings
- **Poor Error Handling**: Empty exception blocks

### Metrics Tracked
- Lines of code
- Function count
- Complexity score
- Comment ratio
- Technical debt estimation

## 🚨 Troubleshooting

### Common Issues

**"Ollama not found"**
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh
ollama serve
```

**"Permission denied"**
```bash
chmod +x install.sh
# or run with sudo if needed
```

**"Module not found"**
```bash
# Activate virtual environment
source venv/bin/activate
pip install -r requirements.txt
```

**"Port already in use"**
```bash
# Use different port
streamlit run app.py --server.port 8502
```

### Performance Tips
- Use `--no-ai` for faster scans
- Exclude large directories (node_modules, etc.)
- Increase `max_file_size` for large files
- Use Docker for consistent performance

## 🎯 Best Practices

### For Development Teams
1. **Run audits regularly** (daily/weekly)
2. **Set up CI/CD integration** for automated checks
3. **Address HIGH severity issues** immediately
4. **Track progress** with historical reports
5. **Customize patterns** for your tech stack

### For Security Teams
1. **Focus on CRITICAL/HIGH** issues first
2. **Review AI recommendations** carefully
3. **Use compliance reports** for audits
4. **Export results** for documentation
5. **Monitor trends** over time

## 🔗 Integration Examples

### GitHub Actions
```yaml
- name: Code Security Audit
  run: |
    python code_auditor.py --directory . --output security-report.json
    # Fail if high-risk issues found
```

### Jenkins Pipeline
```groovy
stage('Security Audit') {
    steps {
        sh 'python code_auditor.py --directory . --severity HIGH'
    }
}
```

### Pre-commit Hook
```bash
#!/bin/sh
python code_auditor.py --directory . --no-ai --severity HIGH
```

## 📚 Next Steps

1. **Explore the Dashboard**: Try different visualizations
2. **Customize Patterns**: Add your own security rules
3. **Set Up CI/CD**: Automate security checks
4. **Join Community**: Contribute to the project
5. **Read Documentation**: Check README.md for advanced features

## 🆘 Getting Help

- **Documentation**: [README.md](README.md)
- **Issues**: [GitHub Issues](https://github.com/muhammadfarhantanvir/Code-Quality-Security-Audit-System-AI-Agent/issues)
- **Discussions**: [GitHub Discussions](https://github.com/muhammadfarhantanvir/Code-Quality-Security-Audit-System-AI-Agent/discussions)
- **Contributing**: [CONTRIBUTING.md](CONTRIBUTING.md)

## 🎉 Success!

You're now ready to use the Code Quality & Security Audit System! Start with small projects and gradually integrate it into your development workflow.

Happy auditing! 🔍✨