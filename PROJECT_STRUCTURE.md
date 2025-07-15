# 📁 Project Structure Overview

This document provides a comprehensive overview of the Code Quality & Security Audit System project structure.

## 🏗️ Directory Structure

```
Code-Quality-Security-Audit-System-AI-Agent/
├── 📁 src/                                 # Source code (main package)
│   └── 📁 code_audit_system/              # Main application package
│       ├── 📄 __init__.py                 # Package initialization
│       ├── 📁 core/                       # Core functionality
│       │   ├── 📄 __init__.py             # Core package init
│       │   ├── 📄 auditor.py              # Main auditor class
│       │   ├── 📄 models.py               # Data models & dataclasses
│       │   └── 📄 patterns.py             # Security & quality patterns
│       ├── 📁 ai/                         # AI integration
│       │   ├── 📄 __init__.py             # AI package init
│       │   └── 📄 ollama_client.py        # Ollama AI client
│       ├── 📁 dashboard/                  # Web interface
│       │   ├── 📄 __init__.py             # Dashboard package init
│       │   └── 📄 streamlit_app.py        # Streamlit dashboard
│       └── 📁 cli/                        # Command-line interface
│           ├── 📄 __init__.py             # CLI package init
│           └── 📄 main.py                 # CLI implementation
├── 📁 config/                             # Configuration files
│   └── 📄 config.yaml                    # Main configuration
├── 📁 docs/                              # Documentation
│   ├── 📄 README.md                      # Detailed documentation
│   ├── 📄 GETTING_STARTED.md             # Quick start guide
│   ├── 📄 CONTRIBUTING.md                # Contribution guidelines
│   └── 📄 CHANGELOG.md                   # Version history
├── 📁 scripts/                           # Installation & utility scripts
│   ├── 📄 install.sh                     # Linux/macOS installer
│   └── 📄 install.bat                    # Windows installer
├── 📁 docker/                            # Docker configuration
│   ├── 📄 Dockerfile                     # Container definition
│   └── 📄 docker-compose.yml             # Multi-container setup
├── 📁 tests/                             # Test suite
│   ├── 📄 __init__.py                    # Test package init
│   ├── 📄 test_security_patterns.py      # Security pattern tests
│   └── 📄 test_quality_patterns.py       # Quality pattern tests
├── 📁 assets/                            # Static assets
│   ├── 📁 images/                        # Screenshots & diagrams
│   │   ├── 📄 code quality.png           # Dashboard screenshot
│   │   └── 📄 code_quality_2.png         # Additional screenshot
│   └── 📁 examples/                      # Example code
│       └── 📄 sample_vulnerable_code.py   # Test vulnerable code
├── 📁 .github/                           # GitHub configuration
│   └── 📁 workflows/                     # CI/CD workflows
│       └── 📄 ci.yml                     # GitHub Actions workflow
├── 📄 main.py                            # CLI entry point
├── 📄 dashboard.py                       # Dashboard entry point
├── 📄 requirements.txt                   # Python dependencies
├── 📄 setup.py                           # Package setup (legacy)
├── 📄 pyproject.toml                     # Modern package configuration
├── 📄 Makefile                           # Project management commands
├── 📄 README.md                          # Main project documentation
├── 📄 LICENSE                            # MIT license
├── 📄 CITATION.cff                       # Academic citation format
├── 📄 .gitignore                         # Git ignore rules
└── 📄 PROJECT_STRUCTURE.md               # This file
```

## 🎯 Key Components

### 📦 Core Package (`src/code_audit_system/`)

The main application package following Python best practices:

- **Modular Design**: Separated into logical components (core, ai, dashboard, cli)
- **Clean Architecture**: Clear separation of concerns
- **Extensible**: Easy to add new features and patterns
- **Testable**: Well-structured for unit testing

### 🧠 Core Module (`src/code_audit_system/core/`)

Contains the main business logic:

- `auditor.py`: Main `CodeAuditor` class that orchestrates the analysis
- `models.py`: Data models using Python dataclasses for type safety
- `patterns.py`: Security and quality patterns with recommendations

### 🤖 AI Module (`src/code_audit_system/ai/`)

Handles AI integration:

- `ollama_client.py`: Client for local Ollama AI models
- Supports multiple models for different analysis types
- Caching and error handling for robust AI integration

### 🌐 Dashboard Module (`src/code_audit_system/dashboard/`)

Web interface using Streamlit:

- Interactive dashboard with charts and visualizations
- Real-time analysis and reporting
- Historical trend analysis
- Export capabilities

### 💻 CLI Module (`src/code_audit_system/cli/`)

Command-line interface:

- Comprehensive argument parsing
- Multiple output formats (JSON, CSV, HTML)
- Filtering and configuration options
- Exit codes for CI/CD integration

## 🔧 Configuration & Setup

### Configuration (`config/`)

- `config.yaml`: Main configuration file
- Customizable patterns, thresholds, and AI settings
- Environment-specific configurations

### Installation (`scripts/`)

- `install.sh`: Automated Linux/macOS installation
- `install.bat`: Automated Windows installation
- Handles dependencies, AI models, and setup verification

### Docker (`docker/`)

- `Dockerfile`: Multi-stage container build
- `docker-compose.yml`: Complete stack with Ollama
- Production-ready containerization

## 📚 Documentation (`docs/`)

Comprehensive documentation suite:

- `README.md`: Detailed project documentation
- `GETTING_STARTED.md`: Step-by-step setup guide
- `CONTRIBUTING.md`: Development and contribution guidelines
- `CHANGELOG.md`: Version history and release notes

## 🧪 Testing (`tests/`)

Comprehensive test suite:

- `test_security_patterns.py`: Security vulnerability detection tests
- `test_quality_patterns.py`: Code quality issue detection tests
- Pattern validation and edge case testing
- CI/CD integration with GitHub Actions

## 🎨 Assets (`assets/`)

Supporting files:

- `images/`: Screenshots and diagrams for documentation
- `examples/`: Sample vulnerable code for testing and demos

## 🚀 Entry Points

### CLI Usage
```bash
python main.py --directory /path/to/project
```

### Dashboard Usage
```bash
streamlit run dashboard.py
```

### Package Installation
```bash
pip install -e .
code-audit --directory /path/to/project
```

## 🛠️ Development Workflow

### Setup Development Environment
```bash
make dev-setup
```

### Run Tests
```bash
make test
```

### Code Quality Checks
```bash
make ci  # Runs formatting, linting, type checking, and tests
```

### Build and Deploy
```bash
make build
make docker
```

## 📈 Scalability & Extensibility

### Adding New Security Patterns
1. Add patterns to `src/code_audit_system/core/patterns.py`
2. Add tests to `tests/test_security_patterns.py`
3. Update documentation

### Adding New Languages
1. Extend `supported_extensions` in `auditor.py`
2. Add language-specific patterns
3. Update configuration

### Adding New AI Models
1. Update `ollama_client.py` with new model configurations
2. Add model-specific prompt templates
3. Test and document capabilities

## 🔒 Security Considerations

- **Local Processing**: All analysis runs locally, no data sent externally
- **AI Privacy**: Uses local Ollama models for privacy
- **Secure Defaults**: Conservative security pattern matching
- **Input Validation**: Proper handling of file paths and user input

## 📊 Performance Characteristics

- **Concurrent Processing**: Multi-threaded file analysis
- **Memory Efficient**: Streaming file processing for large codebases
- **Caching**: AI response caching for improved performance
- **Configurable Limits**: Adjustable file size and processing limits

## 🎯 Best Practices Implemented

- **PEP 8 Compliance**: Python coding standards
- **Type Hints**: Full type annotation for better IDE support
- **Documentation**: Comprehensive docstrings and comments
- **Error Handling**: Robust error handling and logging
- **Testing**: High test coverage with meaningful test cases
- **CI/CD**: Automated testing and deployment pipelines

This structure provides a solid foundation for a professional, maintainable, and extensible code analysis tool that can grow with user needs and community contributions.