# Contributing to Code Quality & Security Audit System

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## 🚀 Quick Start

1. **Fork the repository**
2. **Clone your fork**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/Code-Quality-Security-Audit-System-AI-Agent.git
   cd Code-Quality-Security-Audit-System-AI-Agent
   ```
3. **Set up development environment**:
   ```bash
   # Linux/macOS
   ./install.sh
   
   # Windows
   install.bat
   ```

## 🛠️ Development Setup

### Prerequisites
- Python 3.9+
- Ollama (for AI features)
- Git

### Environment Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate.bat  # Windows

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest black flake8 mypy pre-commit
```

### Pre-commit Hooks
```bash
pre-commit install
```

## 📝 Code Style

We follow Python PEP 8 standards with some modifications:

- **Line length**: 100 characters
- **Imports**: Use absolute imports
- **Docstrings**: Google style
- **Type hints**: Required for all public functions

### Formatting
```bash
# Format code
black .

# Check linting
flake8 .

# Type checking
mypy .
```

## 🧪 Testing

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_security_patterns.py
```

### Writing Tests
- Place tests in the `tests/` directory
- Use descriptive test names: `test_should_detect_sql_injection_when_query_concatenated`
- Include both positive and negative test cases
- Mock external dependencies (Ollama API calls)

Example test:
```python
def test_should_detect_sql_injection():
    auditor = CodeAuditor()
    code = 'query = f"SELECT * FROM users WHERE id = {user_id}"'
    issues = auditor._analyze_security_patterns(Path("test.py"), code)
    
    assert len(issues) == 1
    assert issues[0].issue_type == "SQL Injection"
    assert issues[0].severity == "HIGH"
```

## 🔍 Adding New Security Patterns

1. **Add pattern to `SECURITY_PATTERNS`**:
   ```python
   'New Vulnerability': [
       r'pattern1',
       r'pattern2',
   ]
   ```

2. **Add CWE mapping**:
   ```python
   self.cwe_mappings = {
       'New Vulnerability': 'CWE-XXX',
   }
   ```

3. **Add recommendation**:
   ```python
   def _get_security_recommendation(self, issue_type: str) -> str:
       recommendations = {
           'New Vulnerability': "Specific recommendation",
       }
   ```

4. **Write tests**:
   ```python
   def test_should_detect_new_vulnerability():
       # Test implementation
   ```

## 📊 Adding New Quality Patterns

Similar process as security patterns but in `QUALITY_PATTERNS`.

## 🤖 AI Model Integration

### Adding New Models
1. Update `OllamaClient.models` dictionary
2. Add model-specific prompt templates
3. Test with various code samples
4. Document model capabilities

### Prompt Engineering
- Keep prompts focused and specific
- Include examples when possible
- Test with edge cases
- Consider token limits

## 📚 Documentation

### Code Documentation
- All public functions must have docstrings
- Include parameter types and return types
- Provide usage examples for complex functions

### README Updates
- Update feature lists when adding new capabilities
- Include new installation steps if needed
- Add examples for new functionality

## 🐛 Bug Reports

When reporting bugs, include:

1. **Environment details**:
   - OS and version
   - Python version
   - Ollama version (if applicable)

2. **Steps to reproduce**
3. **Expected vs actual behavior**
4. **Code samples** (if applicable)
5. **Error messages** (full stack trace)

## ✨ Feature Requests

For new features:

1. **Check existing issues** first
2. **Describe the use case** clearly
3. **Provide examples** of how it would work
4. **Consider backwards compatibility**

## 🔄 Pull Request Process

1. **Create feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make changes**:
   - Follow code style guidelines
   - Add tests for new functionality
   - Update documentation

3. **Test thoroughly**:
   ```bash
   pytest
   black --check .
   flake8 .
   mypy .
   ```

4. **Commit with clear messages**:
   ```bash
   git commit -m "feat: add new security pattern for LDAP injection"
   ```

5. **Push and create PR**:
   ```bash
   git push origin feature/your-feature-name
   ```

### PR Requirements
- [ ] Tests pass
- [ ] Code is formatted (black)
- [ ] No linting errors (flake8)
- [ ] Type checking passes (mypy)
- [ ] Documentation updated
- [ ] CHANGELOG.md updated (for significant changes)

## 🏷️ Commit Message Format

We use conventional commits:

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes
- `refactor:` Code refactoring
- `test:` Test additions/changes
- `chore:` Maintenance tasks

Examples:
```
feat: add support for Rust file analysis
fix: resolve false positive in XSS detection
docs: update installation instructions for Windows
```

## 🎯 Areas for Contribution

### High Priority
- [ ] Additional security patterns (OWASP Top 10)
- [ ] Support for more programming languages
- [ ] Performance optimizations
- [ ] Better AI prompt engineering

### Medium Priority
- [ ] Web interface improvements
- [ ] Export format options (PDF, SARIF)
- [ ] Integration with CI/CD platforms
- [ ] Custom rule configuration

### Low Priority
- [ ] Mobile-responsive dashboard
- [ ] Plugin system
- [ ] Advanced reporting features
- [ ] Multi-language support

## 🤝 Community Guidelines

- **Be respectful** and inclusive
- **Help others** learn and contribute
- **Share knowledge** and best practices
- **Give constructive feedback**
- **Follow the code of conduct**

## 📞 Getting Help

- **GitHub Issues**: For bugs and feature requests
- **Discussions**: For questions and general discussion
- **Discord**: [Link to Discord server] (if available)
- **Email**: [maintainer email] for security issues

## 🏆 Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Given credit in documentation

Thank you for contributing to making code more secure and maintainable! 🚀