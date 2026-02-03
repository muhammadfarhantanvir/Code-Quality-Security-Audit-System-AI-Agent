import re
from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class AuditPattern:
    id: str
    name: str
    description: str
    pattern: str
    severity: str  # CRITICAL, HIGH, MEDIUM, LOW
    category: str  # security, quality
    recommendation: str
    owasp_tag: Optional[str] = None
    compliance: List[str] = field(default_factory=list)

SECURITY_PATTERNS = [
    AuditPattern(
        id="SEC001",
        name="SQL Injection (String Formatting)",
        description="Possible SQL injection through string formatting in query.",
        pattern=r"(execute|query)\s*\(\s*f?['\"].*\{.*\}",
        severity="HIGH",
        category="security",
        recommendation="Use parameterized queries instead of string formatting.",
        owasp_tag="A03:2021-Injection",
        compliance=["PCI-DSS", "HIPAA", "ISO27001"]
    ),
    AuditPattern(
        id="SEC002",
        name="Hardcoded Secret",
        description="Potential hardcoded API key, token, or password detected.",
        pattern=r"(api_key|secret|password|token|credential|access_key|aws_key)\s*=\s*['\"][a-zA-Z0-9_\-\.]{16,}['\"]",
        severity="CRITICAL",
        category="security",
        recommendation="Use environment variables or a secret management service.",
        owasp_tag="A07:2021-Identification and Authentication Failures",
        compliance=["PCI-DSS", "GDPR", "SOX"]
    ),
    AuditPattern(
        id="SEC003",
        name="Insecure OS Command",
        description="Execution of OS commands using unsanitized input.",
        pattern=r"os\.(system|popen)|subprocess\.(run|call|Popen)\s*\(\s*f?['\"].*\{.*\}",
        severity="HIGH",
        category="security",
        recommendation="Use safer alternatives or ensure inputs are properly escaped.",
        owasp_tag="A03:2021-Injection",
        compliance=["ISO27001"]
    ),
    AuditPattern(
        id="SEC005",
        name="Cross-Site Scripting (XSS)",
        description="Unsafe rendering of user input in HTML.",
        pattern=r"dangerouslySetInnerHTML|\.innerHTML\s*=|format_html\(.*\)",
        severity="HIGH",
        category="security",
        recommendation="Sanitize all user input before rendering or use template engines with auto-escaping.",
        owasp_tag="A03:2021-Injection",
        compliance=["PCI-DSS", "GDPR"]
    ),
]

QUALITY_PATTERNS = [
    AuditPattern(
        id="QUAL001",
        name="Deep Nesting",
        description="Function has excessively deep nesting levels.",
        pattern=r"(?m)(?:^\s+if\b.*?\n){4,}",
        severity="MEDIUM",
        category="quality",
        recommendation="Refactor code to reduce nesting using early returns or helper functions."
    ),
    AuditPattern(
        id="QUAL004",
        name="Complex Function",
        description="Function has high cyclomatic complexity (many branch points).",
        pattern=r"(if|elif|for|while|try|except|and|or).*", # Simple heuristic
        severity="MEDIUM",
        category="quality",
        recommendation="Break down complex functions into smaller, more focused units."
    ),
    AuditPattern(
        id="QUAL005",
        name="Missing Docstring",
        description="Public function or class is missing documentation.",
        pattern=r"(def|class)\s+\w+\(.*\):\s*(?!\s*['\"]{3})",
        severity="LOW",
        category="quality",
        recommendation="Add docstrings to all public API elements for better maintainability."
    ),
]

def get_all_patterns() -> List[AuditPattern]:
    return SECURITY_PATTERNS + QUALITY_PATTERNS
