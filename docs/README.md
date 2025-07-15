# Code Quality & Security Audit System

![Code Quality](code%20quality.png)

![Code Quality 2](code_quality_2.png)
## Overview

The Code Quality & Security Audit System is a Python-based tool designed to analyze codebases for security vulnerabilities and quality issues. It combines pattern-based analysis with AI-driven insights using local Ollama models to identify potential risks, such as OWASP Top 10 vulnerabilities, and code quality problems, such as long functions or missing docstrings. The system generates detailed audit reports, stores results in a SQLite database, and provides a Streamlit-based dashboard for visualizing findings.

### Key Features
- **Security Analysis**: Detects vulnerabilities like SQL injection, XSS, hardcoded secrets, and more using regex patterns and AI analysis.
- **Code Quality Checks**: Identifies issues like code duplication, complex functions, and missing docstrings.
- **AI Integration**: Leverages local Ollama models (`deepseek-coder:6.7b`, `deepseek-r1:1.5b`, `deepscaler`) for advanced analysis.
- **Database Storage**: Saves audit reports and issues in a SQLite database for historical tracking.
- **Interactive Dashboard**: Visualizes results using Streamlit and Plotly for easy interpretation.
- **Compliance Reporting**: Supports standards like PCI-DSS, SOX, GDPR, HIPAA, and ISO 27001 (placeholder implementation).
- **CLI and GUI Support**: Run audits via command-line interface or interactive web dashboard.

## Requirements

 ```bash
   pip install -r requirements.txt
   ```

- **Python**: 3.9 or higher
- **Dependencies**:
  - `requests`
  - `pandas`
  - `streamlit`
  - `plotly`
- **Ollama**: Local Ollama server running at `http://localhost:11434` with models:
  - `deepseek-coder:6.7b`
  - `deepseek-r1:1.5b`
  - `deepscaler`
- **Operating System**: Linux, macOS, or Windows
- **Optional**: SQLite for persistent storage (included with Python)

## 🚀 Quick Start

### Option 1: Automated Installation (Recommended)

**Linux/macOS:**
```bash
git clone https://github.com/muhammadfarhantanvir/Code-Quality-Security-Audit-System-AI-Agent
cd Code-Quality-Security-Audit-System-AI-Agent
chmod +x install.sh
./install.sh
```

**Windows:**
```cmd
git clone https://github.com/muhammadfarhantanvir/Code-Quality-Security-Audit-System-AI-Agent
cd Code-Quality-Security-Audit-System-AI-Agent
install.bat
```

### Option 2: Docker (Easiest)

```bash
git clone https://github.com/muhammadfarhantanvir/Code-Quality-Security-Audit-System-AI-Agent
cd Code-Quality-Security-Audit-System-AI-Agent
docker-compose up -d
```

Then open http://localhost:8501 in your browser.

### Option 3: Manual Installation

1. **Prerequisites**:
   - Python 3.9+ ([Download](https://python.org))
   - Git ([Download](https://git-scm.com))

2. **Clone Repository**:
   ```bash
   git clone https://github.com/muhammadfarhantanvir/Code-Quality-Security-Audit-System-AI-Agent
   cd Code-Quality-Security-Audit-System-AI-Agent
   ```

3. **Set Up Python Environment**:
   ```bash
   python -m venv venv
   
   # Activate virtual environment
   # Linux/macOS:
   source venv/bin/activate
   # Windows:
   venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   ```

4. **Install Ollama (for AI features)**:
   - **Linux**: `curl -fsSL https://ollama.ai/install.sh | sh`
   - **macOS**: `brew install ollama` or download from [ollama.ai](https://ollama.ai)
   - **Windows**: Download installer from [ollama.ai](https://ollama.ai)

5. **Download AI Models**:
   ```bash
   ollama serve  # Start Ollama service
   
   # In another terminal:
   ollama pull deepseek-coder:6.7b
   ollama pull deepseek-r1:1.5b
   ollama pull deepscaler
   ```

6. **Verify Installation**:
   ```bash
   python code_auditor.py --help
   ```

## 📋 Installation

## 💻 Usage

### Command-Line Interface (CLI)

**Basic Usage:**
```bash
# Quick scan
python code_auditor.py --directory /path/to/your/project

# Save detailed report
python code_auditor.py --directory /path/to/your/project --output report.json

# Filter by severity
python code_auditor.py --directory /path/to/your/project --severity HIGH

# Export multiple formats
python code_auditor.py --directory /path/to/your/project --export-html --export-csv

# Disable AI analysis (faster, pattern-only)
python code_auditor.py --directory /path/to/your/project --no-ai
```

**Advanced Options:**
```bash
# Show all available options
python code_auditor.py --help

# Verbose output with detailed findings
python code_auditor.py --directory /path/to/your/project --verbose

# Filter by issue type
python code_auditor.py --directory /path/to/your/project --type security

# Custom Ollama server
python code_auditor.py --directory /path/to/your/project --ollama-url http://remote-server:11434
```

### Streamlit Dashboard
1. Start the dashboard:
   ```bash
   streamlit run code_auditor.py
   ```
2. Open your browser to `http://localhost:8501`.
3. Enter the project directory path and click "Start Audit" to scan and view results.

### Supported File Types
The tool scans files with the following extensions:
- Python: `.py`
- JavaScript/TypeScript: `.js`, `.jsx`, `.ts`, `.tsx`
- Java: `.java`
- C/C++: `.c`, `.cpp`
- PHP: `.php`
- Ruby: `.rb`
- Go: `.go`

## Project Structure

```
code-audit-system/
├── code_auditor.py         # Main script
├── audit_results.db        # SQLite database for storing audit reports
├── venv/                   # Virtual environment (after setup)
├── README.md               # This file
└── sample_project/         # Example project directory for testing
```

## Configuration

- **Ollama Server**: Configure the base URL in `OllamaClient` if your Ollama server runs on a different host or port (default: `http://localhost:11434`).
- **Database**: Audit reports are stored in `audit_results.db`. Modify `db_path` in `CodeAuditor` to change the database location.
- **File Size Limit**: AI analysis is limited to files under 2000 characters for performance. Adjust this in the `scan_directory` method if needed.

## Output

- **CLI Output**: Summary of files scanned, total lines, security/quality issues, and risk score. Detailed reports can be saved as JSON.
- **Dashboard Output**: Interactive visualizations including:
  - Risk score and issue counts
  - Bar charts for security issues by type
  - Pie charts for quality issue distribution
  - Detailed issue lists with code snippets and recommendations
  - Historical trend analysis of risk scores

## Example

```bash
python code_auditor.py --directory ./sample_project --output audit_report.json
```

Sample JSON report output:
```json
{
  "project_path": "./sample_project",
  "scan_date": "2025-06-25T16:25:00",
  "total_files": 10,
  "total_lines": 1000,
  "security_issues": [
    {
      "file_path": "app.py",
      "line_number": 42,
      "issue_type": "SQL Injection",
      "severity": "HIGH",
      "description": "Potential SQL injection vulnerability detected",
      "code_snippet": "cursor.execute(f'SELECT * FROM users WHERE id = {user_id}')",
      "recommendation": "Use parameterized queries or ORM methods"
    }
  ],
  "quality_issues": [
    {
      "file_path": "app.py",
      "line_number": 100,
      "issue_type": "Long Functions",
      "severity": "MEDIUM",
      "description": "Long Functions detected",
      "code_snippet": "def process_data(...): ...",
      "recommendation": "Break down into smaller, focused functions"
    }
  ],
  "risk_score": 75.5,
  "recommendations": ["URGENT: Address 1 high-severity security vulnerabilities immediately","Implement security code review process"],
  "code_metrics": {...},
  "compliance_checks": [...],
  "scan_duration": 12.34,
  "files_by_type": {".py": 8, ".js": 2}
}
```

## Limitations

- **Ollama Dependency**: Requires a running Ollama server with specific models. Without it, only pattern-based analysis is performed.
- **Placeholder Metrics**: `CodeMetrics` and `ComplianceCheck` fields are currently placeholders and need implementation for full functionality.
- **File Size**: Large files (>2000 characters) skip AI analysis to maintain performance.
- **Language Support**: Limited to specified file extensions; additional languages require pattern updates.

## Contributing

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/new-feature`).
3. Commit changes (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature/new-feature`).
5. Open a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/muhammadfarhantanvir/Code-Quality-Security-Audit-System-AI-Agent/blob/main/LICENSE) file for details.

## Contact

For issues or feature requests, please open an issue on the [GitHub repository](https://github.com/muhammadfarhantanvir/Code-Quality-Security-Audit-System-AI-Agent).

