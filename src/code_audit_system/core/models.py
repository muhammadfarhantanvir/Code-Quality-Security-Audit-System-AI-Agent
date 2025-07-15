"""
Data models for the audit system
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional


@dataclass
class SecurityIssue:
    """Represents a security vulnerability found in code"""
    file_path: str
    line_number: int
    issue_type: str
    severity: str
    description: str
    code_snippet: str
    recommendation: str
    cwe_id: Optional[str] = None  # Common Weakness Enumeration ID
    confidence: float = 1.0  # AI confidence score
    remediation_effort: str = "MEDIUM"  # LOW/MEDIUM/HIGH


@dataclass
class QualityIssue:
    """Represents a code quality issue"""
    file_path: str
    line_number: int
    issue_type: str
    severity: str
    description: str
    code_snippet: str
    recommendation: str
    complexity_score: Optional[int] = None
    maintainability_impact: str = "MEDIUM"


@dataclass
class CodeMetrics:
    """Code quality metrics"""
    cyclomatic_complexity: int
    lines_of_code: int
    comment_ratio: float
    function_count: int
    class_count: int
    test_coverage: float
    code_duplication: float
    technical_debt_minutes: int


@dataclass
class ComplianceCheck:
    """Compliance standard check results"""
    standard: str  # PCI-DSS, SOX, GDPR, etc.
    status: str    # COMPLIANT, NON_COMPLIANT, PARTIAL
    requirements_met: int
    total_requirements: int
    violations: List[str]


@dataclass
class AuditReport:
    """Complete audit report"""
    project_path: str
    scan_date: datetime
    total_files: int
    total_lines: int
    security_issues: List[SecurityIssue]
    quality_issues: List[QualityIssue]
    risk_score: float
    recommendations: List[str]
    code_metrics: CodeMetrics
    compliance_checks: List[ComplianceCheck]
    scan_duration: float
    files_by_type: Dict[str, int]
    trend_analysis: Optional[Dict] = None