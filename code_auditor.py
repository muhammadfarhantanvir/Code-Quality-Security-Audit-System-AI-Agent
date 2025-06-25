import os
import json
import re
import ast
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional
import hashlib
import subprocess
import requests
from dataclasses import dataclass, asdict
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
import threading
from collections import defaultdict, Counter
import base64
import zipfile
import io
from concurrent.futures import ThreadPoolExecutor, as_completed
import networkx as nx
import difflib

# Advanced Security patterns with OWASP Top 10 coverage
SECURITY_PATTERNS = {
    'SQL Injection': [
        r'execute\s*\(\s*["\'].*%.*["\']',
        r'cursor\.execute\s*\(\s*["\'].*\+.*["\']',
        r'query\s*=\s*["\'].*\+.*["\']',
        r'SELECT.*FROM.*WHERE.*=.*\+',
        r'INSERT.*VALUES.*\+',
        r'UPDATE.*SET.*\+',
        r'DELETE.*WHERE.*\+',
    ],
    'XSS Vulnerability': [
        r'innerHTML\s*=\s*.*\+',
        r'document\.write\s*\(\s*.*\+',
        r'eval\s*\(\s*.*\+',
        r'dangerouslySetInnerHTML',
        r'v-html\s*=',
        r'__html:\s*{',
    ],
    'Hardcoded Secrets': [
        r'password\s*=\s*["\'][^"\']{6,}["\']',
        r'pwd\s*=\s*["\'][^"\']{6,}["\']',
        r'secret\s*=\s*["\'][^"\']{10,}["\']',
        r'api_key\s*=\s*["\'][^"\']{10,}["\']',
        r'token\s*=\s*["\'][^"\']{10,}["\']',
        r'private_key\s*=\s*["\'].*["\']',
        r'AWS_SECRET_ACCESS_KEY\s*=',
        r'STRIPE_SECRET_KEY\s*=',
    ],
    'Command Injection': [
        r'os\.system\s*\(\s*.*\+',
        r'subprocess\.call\s*\(\s*.*\+',
        r'subprocess\.run\s*\(\s*.*\+',
        r'exec\s*\(\s*.*\+',
        r'eval\s*\(\s*.*\+',
        r'shell=True',
    ],
    'Insecure Communication': [
        r'http://[^"\'\s]+',
        r'requests\.get\s*\(\s*["\']http://',
        r'urllib\.request\.urlopen\s*\(\s*["\']http://',
        r'verify=False',
        r'ssl._create_unverified_context',
    ],
    'Path Traversal': [
        r'open\s*\(\s*.*\+.*["\']\.\./',
        r'file\s*=\s*.*\+.*["\']\.\./',
        r'filename.*\.\./.*\.\.',
    ],
    'Weak Cryptography': [
        r'hashlib\.md5\(',
        r'hashlib\.sha1\(',
        r'DES\(',
        r'RC4\(',
        r'random\.random\(\)',
    ],
    'LDAP Injection': [
        r'ldap.*search.*\+',
        r'ldap.*filter.*\+',
    ],
    'XML External Entity': [
        r'XMLParser\s*\(\s*resolve_entities=True',
        r'fromstring\s*\(',
        r'parse\s*\(\s*.*\.xml',
    ],
    'Deserialization': [
        r'pickle\.loads\s*\(',
        r'yaml\.load\s*\(',
        r'eval\s*\(\s*.*\.json',
    ]
}

# Advanced Code quality patterns with metrics
QUALITY_PATTERNS = {
    'Long Functions': r'def\s+\w+\s*\([^)]*\):[^def]{800,}',  # Increased threshold
    'Complex Functions': r'if.*elif.*elif.*elif',  # Multiple elif chains
    'Deep Nesting': r'(\s{4,}){6,}',  # 6+ levels of indentation
    'Duplicate Code': r'(.{50,})\s*\n.*\1',
    'Magic Numbers': r'\b\d{2,}\b(?!\s*[)\]}])',
    'TODO Comments': r'#.*TODO|#.*FIXME|#.*HACK|#.*XXX',
    'Empty Exception': r'except[^:]*:\s*pass',
    'Global Variables': r'^\s*global\s+\w+',
    'Long Parameter Lists': r'def\s+\w+\s*\([^)]{80,}\)',
    'Unused Imports': r'import\s+\w+\s*',
    'Missing Docstrings': r'def\s+\w+\s*\([^)]*\):\s*\n\s*(?!""")',
    'Overly Complex Regex': r'r["\'].*[{}\[\]().*+?^$|\\]{10,}.*["\']',
    'Bare Except': r'except:\s*',
    'Lambda Complexity': r'lambda.*:.*if.*else.*if.*else',
}

@dataclass
class SecurityIssue:
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
    standard: str  # PCI-DSS, SOX, GDPR, etc.
    status: str    # COMPLIANT, NON_COMPLIANT, PARTIAL
    requirements_met: int
    total_requirements: int
    violations: List[str]

@dataclass
class AuditReport:
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

class OllamaClient:
    """Advanced client for interacting with local Ollama models"""
    
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        self.models = {
            'coder': 'deepseek-coder:6.7b',
            'reasoner': 'deepseek-r1:1.5b',
            'scaler': 'deepscaler'
        }
        self.response_cache = {}  # Simple response caching
    
    def is_available(self) -> bool:
        """Check if Ollama service is running"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def get_model_performance(self) -> Dict:
        """Get performance metrics for each model"""
        try:
            response = requests.get(f"{self.base_url}/api/ps")
            if response.status_code == 200:
                return response.json()
        except:
            pass
        return {}
    
    def analyze_code_security_advanced(self, code: str, file_path: str, context: Dict = None) -> Dict:
        """Advanced security analysis with context awareness"""
        prompt = f"""
        Perform a comprehensive security analysis of this code:
        
        File: {file_path}
        Context: {context or {}}
        Code:
        ```
        {code[:1500]}
        ```
        
        Analyze for OWASP Top 10 vulnerabilities:
        1. Injection flaws (SQL, NoSQL, LDAP, OS command)
        2. Broken authentication and session management
        3. Sensitive data exposure
        4. XML External Entities (XXE)
        5. Broken access control
        6. Security misconfiguration
        7. Cross-Site Scripting (XSS)
        8. Insecure deserialization
        9. Using components with known vulnerabilities
        10. Insufficient logging and monitoring
        
        For each finding, provide:
        - CWE ID (Common Weakness Enumeration)
        - Severity (CRITICAL/HIGH/MEDIUM/LOW)
        - Confidence score (0.0-1.0)
        - Remediation effort (LOW/MEDIUM/HIGH)
        - Specific fix recommendations
        
        Format as JSON with structure:
        {{
            "findings": [
                {{
                    "type": "vulnerability_type",
                    "cwe_id": "CWE-XXX",
                    "severity": "HIGH",
                    "confidence": 0.9,
                    "line": 10,
                    "description": "detailed description",
                    "recommendation": "specific fix",
                    "remediation_effort": "MEDIUM"
                }}
            ],
            "overall_risk": "HIGH|MEDIUM|LOW",
            "compliance_impact": ["PCI-DSS", "SOX"]
        }}
        """
        
        return self._query_model_json('coder', prompt)
    
    def analyze_architecture_patterns(self, file_structure: Dict) -> Dict:
        """Analyze architecture patterns and design issues"""
        prompt = f"""
        Analyze this project structure for architecture and design patterns:
        
        File Structure:
        {json.dumps(file_structure, indent=2)}
        
        Evaluate:
        1. Architecture patterns (MVC, Microservices, Layered, etc.)
        2. Design pattern usage
        3. Separation of concerns
        4. Coupling and cohesion
        5. Scalability issues
        6. Maintainability concerns
        
        Provide recommendations for:
        - Refactoring opportunities
        - Performance optimizations
        - Security improvements
        - Code organization
        
        Format as JSON.
        """
        
        return self._query_model_json('reasoner', prompt)
    
    def generate_compliance_report(self, issues: List[Dict], standard: str) -> Dict:
        """Generate compliance report for specific standards"""
        prompt = f"""
        Generate a {standard} compliance report based on these security findings:
        
        Findings: {json.dumps(issues[:10], indent=2)}
        
        For {standard} compliance, analyze:
        1. Which requirements are violated
        2. Risk assessment for each violation
        3. Remediation priorities
        4. Compliance score (0-100)
        5. Action plan with timelines
        
        Standards to consider:
        - PCI-DSS (Payment Card Industry)
        - SOX (Sarbanes-Oxley)
        - GDPR (Data Protection)
        - HIPAA (Healthcare)
        - ISO 27001 (Information Security)
        
        Format as structured JSON report.
        """
        
        return self._query_model_json('reasoner', prompt)
    
    def predict_technical_debt(self, code_metrics: Dict) -> Dict:
        """Predict technical debt and maintenance costs"""
        prompt = f"""
        Analyze these code metrics to predict technical debt:
        
        Metrics: {json.dumps(code_metrics, indent=2)}
        
        Calculate:
        1. Technical debt in hours/days
        2. Maintenance cost prediction
        3. Refactoring priorities
        4. Risk of bugs/failures
        5. Developer productivity impact
        
        Provide recommendations for:
        - Immediate fixes (< 1 day)
        - Short-term improvements (< 1 week)
        - Long-term refactoring (> 1 week)
        
        Format as JSON with cost estimates.
        """
        
        return self._query_model_json('scaler', prompt)
    
    def _query_model_json(self, model_type: str, prompt: str) -> Dict:
        """Query model and parse JSON response"""
        cache_key = hashlib.md5(f"{model_type}:{prompt}".encode()).hexdigest()
        
        if cache_key in self.response_cache:
            return self.response_cache[cache_key]
        
        try:
            response = self._query_model(model_type, prompt)
            
            # Try to extract JSON from response
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group())
                self.response_cache[cache_key] = result
                return result
            else:
                # Fallback to structured text parsing
                return self._parse_text_response(response)
        except Exception as e:
            return {"error": str(e), "raw_response": response if 'response' in locals() else ""}
    
    def _parse_text_response(self, text: str) -> Dict:
        """Parse text response into structured format"""
        return {
            "findings": [],
            "summary": text[:500],
            "recommendations": [text[i:i+100] for i in range(0, min(len(text), 300), 100)]
        }
    
    def analyze_code_security(self, code: str, file_path: str) -> str:
        """Original method for backward compatibility"""
        result = self.analyze_code_security_advanced(code, file_path)
        return json.dumps(result, indent=2) if isinstance(result, dict) else str(result)
    
    def analyze_code_quality(self, code: str, file_path: str) -> str:
        """Use deepseek-coder to analyze code quality"""
        prompt = f"""
        Analyze this code for quality issues and best practices:
        
        File: {file_path}
        Code:
        ```
        {code[:1000]}
        ```
        
        Check for:
        1. Code complexity (cyclomatic complexity)
        2. Naming conventions
        3. Function length and parameters
        4. Code duplication
        5. Error handling patterns
        6. Documentation quality
        7. Test coverage implications
        8. Performance concerns
        
        Provide maintainability score (0-100) and specific recommendations.
        """
        
        return self._query_model('coder', prompt)
    
    def generate_recommendations(self, issues: List[str]) -> str:
        """Use deepseek-r1 for reasoning about overall recommendations"""
        prompt = f"""
        Based on these code analysis findings, provide strategic recommendations:
        
        Issues found:
        {chr(10).join(issues[:10])}
        
        Provide:
        1. Priority ranking of issues (P0/P1/P2)
        2. Business impact assessment
        3. Implementation roadmap with timelines
        4. Cost-benefit analysis
        5. Risk mitigation strategies
        6. Team training recommendations
        
        Consider:
        - Developer productivity
        - Security posture
        - Maintenance costs
        - Customer impact
        - Regulatory compliance
        """
        
        return self._query_model('reasoner', prompt)
    
    def _query_model(self, model_type: str, prompt: str) -> str:
        """Query specific Ollama model"""
        try:
            model_name = self.models.get(model_type, 'deepseek-coder:6.7b')
            payload = {
                "model": model_name,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.1,  # Lower temperature for more consistent results
                    "top_p": 0.9,
                    "num_predict": 2000  # Increased token limit
                }
            }
            
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=60  # Increased timeout
            )
            
            if response.status_code == 200:
                return response.json().get('response', 'No response generated')
            else:
                return f"Error: {response.status_code}"
        except Exception as e:
            return f"Model unavailable: {str(e)}"

class CodeAuditor:
    """Main code auditing engine"""
    
    def __init__(self):
        self.ollama = OllamaClient()
        self.db_path = "audit_results.db"
        self._init_database()
        self.supported_extensions = {
            '.py': 'python', '.js': 'javascript', '.jsx': 'javascript',
            '.ts': 'typescript', '.tsx': 'typescript', '.java': 'java',
            '.cpp': 'cpp', '.c': 'c', '.php': 'php', '.rb': 'ruby',
            '.go': 'go', '.rs': 'rust', '.cs': 'csharp', '.swift': 'swift'
        }
        
        # CWE (Common Weakness Enumeration) mappings
        self.cwe_mappings = {
            'SQL Injection': 'CWE-89',
            'XSS Vulnerability': 'CWE-79',
            'Hardcoded Secrets': 'CWE-798',
            'Command Injection': 'CWE-78',
            'Path Traversal': 'CWE-22',
            'Weak Cryptography': 'CWE-327',
            'LDAP Injection': 'CWE-90',
            'XML External Entity': 'CWE-611',
            'Deserialization': 'CWE-502'
        }
    
    def _init_database(self):
        """Initialize SQLite database for storing results"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS audit_reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_path TEXT,
                scan_date TEXT,
                total_files INTEGER,
                total_lines INTEGER,
                risk_score REAL,
                report_data TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS security_issues (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                report_id INTEGER,
                file_path TEXT,
                line_number INTEGER,
                issue_type TEXT,
                severity TEXT,
                description TEXT,
                code_snippet TEXT,
                recommendation TEXT,
                FOREIGN KEY (report_id) REFERENCES audit_reports (id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS quality_issues (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                report_id INTEGER,
                file_path TEXT,
                line_number INTEGER,
                issue_type TEXT,
                severity TEXT,
                description TEXT,
                code_snippet TEXT,
                recommendation TEXT,
                FOREIGN KEY (report_id) REFERENCES audit_reports (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def scan_directory(self, directory_path: str) -> AuditReport:
        """Scan entire directory for code issues"""
        directory_path = Path(directory_path)
        
        if not directory_path.exists():
            raise ValueError(f"Directory {directory_path} does not exist")
        
        files_to_scan = []
        for ext in self.supported_extensions:
            files_to_scan.extend(directory_path.glob(f"**/*{ext}"))
        
        security_issues = []
        quality_issues = []
        total_lines = 0
        
        print(f"Scanning {len(files_to_scan)} files...")
        
        for file_path in files_to_scan:
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    lines = content.split('\n')
                    total_lines += len(lines)
                
                # Pattern-based analysis
                sec_issues = self._analyze_security_patterns(file_path, content)
                qual_issues = self._analyze_quality_patterns(file_path, content)
                
                security_issues.extend(sec_issues)
                quality_issues.extend(qual_issues)
                
                # AI-based analysis (if Ollama is available)
                if self.ollama.is_available() and len(content) < 2000:  # Limit for performance
                    ai_security = self.ollama.analyze_code_security(content, str(file_path))
                    ai_quality = self.ollama.analyze_code_quality(content, str(file_path))
                    
                    # Parse AI responses and add to issues (simplified)
                    if "HIGH" in ai_security or "CRITICAL" in ai_security:
                        security_issues.append(SecurityIssue(
                            file_path=str(file_path),
                            line_number=1,
                            issue_type="AI Analysis",
                            severity="HIGH",
                            description=ai_security[:200],
                            code_snippet=content[:100],
                            recommendation="Review AI analysis for detailed recommendations"
                        ))
                
            except Exception as e:
                print(f"Error scanning {file_path}: {e}")
                continue
        
        # Calculate risk score
        risk_score = self._calculate_risk_score(security_issues, quality_issues)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(security_issues, quality_issues)
        
        # Create report
        report = AuditReport(
            project_path=str(directory_path),
            scan_date=datetime.now(),
            total_files=len(files_to_scan),
            total_lines=total_lines,
            security_issues=security_issues,
            quality_issues=quality_issues,
            risk_score=risk_score,
            recommendations=recommendations,
            code_metrics=CodeMetrics(
                cyclomatic_complexity=0,
                lines_of_code=total_lines,
                comment_ratio=0.0,
                function_count=0,
                class_count=0,
                test_coverage=0.0,
                code_duplication=0.0,
                technical_debt_minutes=0
            ),
            compliance_checks=[],
            scan_duration=0.0,
            files_by_type={ext: len(list(directory_path.glob(f"**/*{ext}"))) for ext in self.supported_extensions},
            trend_analysis=None
        )
        
        # Save to database
        self._save_report(report)
        
        return report
    
    def _analyze_security_patterns(self, file_path: Path, content: str) -> List[SecurityIssue]:
        """Analyze file for security patterns"""
        issues = []
        lines = content.split('\n')
        
        for issue_type, patterns in SECURITY_PATTERNS.items():
            for pattern in patterns:
                for line_num, line in enumerate(lines, 1):
                    if re.search(pattern, line, re.IGNORECASE):
                        severity = "HIGH" if issue_type in ["SQL Injection", "Command Injection"] else "MEDIUM"
                        
                        issues.append(SecurityIssue(
                            file_path=str(file_path),
                            line_number=line_num,
                            issue_type=issue_type,
                            severity=severity,
                            description=f"Potential {issue_type.lower()} vulnerability detected",
                            code_snippet=line.strip(),
                            recommendation=self._get_security_recommendation(issue_type)
                        ))
        
        return issues
    
    def _analyze_quality_patterns(self, file_path: Path, content: str) -> List[QualityIssue]:
        """Analyze file for quality patterns"""
        issues = []
        lines = content.split('\n')
        
        for issue_type, pattern in QUALITY_PATTERNS.items():
            matches = list(re.finditer(pattern, content, re.MULTILINE))
            for match in matches:
                line_num = content[:match.start()].count('\n') + 1
                issues.append(QualityIssue(
                    file_path=str(file_path),
                    line_number=line_num,
                    issue_type=issue_type,
                    severity="MEDIUM" if issue_type in ["Long Functions", "Duplicate Code"] else "LOW",
                    description=f"{issue_type} detected",
                    code_snippet=match.group()[:100],
                    recommendation=self._get_quality_recommendation(issue_type)
                ))
        
        return issues
    
    def _get_security_recommendation(self, issue_type: str) -> str:
        """Get recommendation for security issue type"""
        recommendations = {
            'SQL Injection': "Use parameterized queries or ORM methods",
            'XSS Vulnerability': "Sanitize user input and use safe rendering methods",
            'Hardcoded Secrets': "Use environment variables or secure vaults",
            'Command Injection': "Validate input and use safe APIs",
            'Insecure Communication': "Use HTTPS for all external communications"
        }
        return recommendations.get(issue_type, "Review security best practices")
    
    def _get_quality_recommendation(self, issue_type: str) -> str:
        """Get recommendation for quality issue type"""
        recommendations = {
            'Long Functions': "Break down into smaller, focused functions",
            'Duplicate Code': "Extract common code into reusable functions",
            'Magic Numbers': "Define constants with descriptive names",
            'TODO Comments': "Complete pending tasks or create tickets",
            'Empty Exception': "Add proper error handling and logging",
            'Global Variables': "Use dependency injection or class attributes",
            'Missing Docstrings': "Add docstrings to functions",
            'Overly Complex Regex': "Simplify complex regular expressions",
            'Bare Except': "Specify exception types in except clauses",
            'Lambda Complexity': "Simplify complex lambda functions"
        }
        return recommendations.get(issue_type, "Follow coding best practices")
    
    def _calculate_risk_score(self, security_issues: List[SecurityIssue], quality_issues: List[QualityIssue]) -> float:
        """Calculate overall risk score (0-100)"""
        security_weight = 0.7
        quality_weight = 0.3
        
        # Security score
        high_security = len([i for i in security_issues if i.severity == "HIGH"])
        medium_security = len([i for i in security_issues if i.severity == "MEDIUM"])
        security_score = min(100, (high_security * 10 + medium_security * 5))
        
        # Quality score
        high_quality = len([i for i in quality_issues if i.severity == "HIGH"])
        medium_quality = len([i for i in quality_issues if i.severity == "MEDIUM"])
        quality_score = min(100, (high_quality * 5 + medium_quality * 2))
        
        return round(security_score * security_weight + quality_score * quality_weight, 2)
    
    def _generate_recommendations(self, security_issues: List[SecurityIssue], quality_issues: List[QualityIssue]) -> List[str]:
        """Generate high-level recommendations"""
        recommendations = []
        
        if security_issues:
            high_sec = len([i for i in security_issues if i.severity == "HIGH"])
            if high_sec > 0:
                recommendations.append(f"URGENT: Address {high_sec} high-severity security vulnerabilities immediately")
            
            recommendations.append("Implement security code review process")
            recommendations.append("Add automated security scanning to CI/CD pipeline")
        
        if quality_issues:
            recommendations.append("Refactor code to improve maintainability")
            recommendations.append("Establish coding standards and enforcement")
            recommendations.append("Add unit tests for complex functions")
        
        if not security_issues and not quality_issues:
            recommendations.append("Code quality is good - maintain current standards")
        
        return recommendations
    
    def _save_report(self, report: AuditReport):
        """Save audit report to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Insert report
        cursor.execute('''
            INSERT INTO audit_reports (project_path, scan_date, total_files, total_lines, risk_score, report_data)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            report.project_path,
            report.scan_date.isoformat(),
            report.total_files,
            report.total_lines,
            report.risk_score,
            json.dumps(asdict(report), default=str)
        ))
        
        report_id = cursor.lastrowid
        
        # Insert security issues
        for issue in report.security_issues:
            cursor.execute('''
                INSERT INTO security_issues (report_id, file_path, line_number, issue_type, severity, description, code_snippet, recommendation)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (report_id, issue.file_path, issue.line_number, issue.issue_type, issue.severity, issue.description, issue.code_snippet, issue.recommendation))
        
        # Insert quality issues
        for issue in report.quality_issues:
            cursor.execute('''
                INSERT INTO quality_issues (report_id, file_path, line_number, issue_type, severity, description, code_snippet, recommendation)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (report_id, issue.file_path, issue.line_number, issue.issue_type, issue.severity, issue.description, issue.code_snippet, issue.recommendation))
        
        conn.commit()
        conn.close()
    
    def get_historical_reports(self) -> List[Dict]:
        """Get all historical audit reports"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, project_path, scan_date, total_files, total_lines, risk_score
            FROM audit_reports
            ORDER BY scan_date DESC
        ''')
        
        reports = []
        for row in cursor.fetchall():
            reports.append({
                'id': row[0],
                'project_path': row[1],
                'scan_date': row[2],
                'total_files': row[3],
                'total_lines': row[4],
                'risk_score': row[5]
            })
        
        conn.close()
        return reports

def create_streamlit_dashboard():
    """Create Streamlit dashboard for the audit system"""
    st.set_page_config(
        page_title="Code Quality & Security Audit System",
        page_icon="🔍",
        layout="wide"
    )
    
    st.title("🔍 Code Quality & Security Audit System")
    st.markdown("### Automated Code Analysis with Local AI Models")
    
    # Initialize auditor
    auditor = CodeAuditor()
    
    # Sidebar
    st.sidebar.header("Audit Configuration")
    
    # Check Ollama status
    ollama_status = auditor.ollama.is_available()
    status_color = "🟢" if ollama_status else "🔴"
    st.sidebar.markdown(f"**Ollama Status:** {status_color} {'Connected' if ollama_status else 'Disconnected'}")
    
    if not ollama_status:
        st.sidebar.warning("Ollama is not running. Only pattern-based analysis will be available.")
    
    # Directory input
    directory_path = st.sidebar.text_input(
        "Project Directory Path",
        value="./sample_project",
        help="Enter the path to your project directory"
    )
    
    # Scan button
    if st.sidebar.button("🚀 Start Audit", type="primary"):
        if not os.path.exists(directory_path):
            st.error(f"Directory '{directory_path}' does not exist!")
        else:
            with st.spinner("Scanning project... This may take a few minutes."):
                try:
                    report = auditor.scan_directory(directory_path)
                    st.session_state['current_report'] = report
                    st.success("Audit completed successfully!")
                except Exception as e:
                    st.error(f"Error during audit: {str(e)}")
    
    # Display results
    if 'current_report' in st.session_state:
        report = st.session_state['current_report']
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Risk Score", f"{report.risk_score}/100")
        
        with col2:
            st.metric("Security Issues", len(report.security_issues))
        
        with col3:
            st.metric("Quality Issues", len(report.quality_issues))
        
        with col4:
            st.metric("Files Scanned", report.total_files)
        
        # Risk assessment
        risk_level = "HIGH" if report.risk_score > 70 else "MEDIUM" if report.risk_score > 30 else "LOW"
        risk_color = "red" if risk_level == "HIGH" else "orange" if risk_level == "MEDIUM" else "green"
        
        st.markdown(f"### Risk Assessment: <span style='color:{risk_color}'>{risk_level}</span>", unsafe_allow_html=True)
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Security issues by type
            if report.security_issues:
                sec_df = pd.DataFrame([asdict(issue) for issue in report.security_issues])
                fig = px.bar(
                    sec_df.groupby(['issue_type', 'severity']).size().reset_index(name='count'),
                    x='issue_type',
                    y='count',
                    color='severity',
                    title="Security Issues by Type"
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.success("✅ No security issues found!")
        
        with col2:
            # Quality issues by type
            if report.quality_issues:
                qual_df = pd.DataFrame([asdict(issue) for issue in report.quality_issues])
                fig = px.pie(
                    qual_df.groupby('issue_type').size().reset_index(name='count'),
                    values='count',
                    names='issue_type',
                    title="Quality Issues Distribution"
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.success("✅ No quality issues found!")
        
        # Detailed issues
        tab1, tab2, tab3 = st.tabs(["🔐 Security Issues", "📊 Quality Issues", "💡 Recommendations"])
        
        with tab1:
            if report.security_issues:
                for issue in report.security_issues:
                    severity_color = "🔴" if issue.severity == "HIGH" else "🟡"
                    with st.expander(f"{severity_color} {issue.issue_type} - {issue.file_path}:{issue.line_number}"):
                        st.markdown(f"**Severity:** {issue.severity}")
                        st.markdown(f"**Description:** {issue.description}")
                        st.code(issue.code_snippet, language="python")
                        st.markdown(f"**Recommendation:** {issue.recommendation}")
            else:
                st.success("No security issues detected!")
        
        with tab2:
            if report.quality_issues:
                for issue in report.quality_issues:
                    severity_color = "🟡" if issue.severity == "MEDIUM" else "🟢"
                    with st.expander(f"{severity_color} {issue.issue_type} - {issue.file_path}:{issue.line_number}"):
                        st.markdown(f"**Severity:** {issue.severity}")
                        st.markdown(f"**Description:** {issue.description}")
                        st.code(issue.code_snippet, language="python")
                        st.markdown(f"**Recommendation:** {issue.recommendation}")
            else:
                st.success("No quality issues detected!")
        
        with tab3:
            st.markdown("### 💡 Strategic Recommendations")
            for i, rec in enumerate(report.recommendations, 1):
                st.markdown(f"{i}. {rec}")
            
            # Cost-benefit analysis
            st.markdown("### 💰 Business Impact")
            
            # Calculate potential savings
            high_issues = len([i for i in report.security_issues if i.severity == "HIGH"])
            medium_issues = len([i for i in report.security_issues + report.quality_issues if i.severity == "MEDIUM"])
            
            potential_breach_cost = high_issues * 500000  # $500K per high-severity issue
            maintenance_savings = medium_issues * 5000    # $5K per medium issue
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Potential Breach Cost Avoided", f"${potential_breach_cost:,}")
            with col2:
                st.metric("Annual Maintenance Savings", f"${maintenance_savings:,}")
    
    # Historical reports
    st.markdown("### 📈 Historical Reports")
    historical_reports = auditor.get_historical_reports()
    
    if historical_reports:
        df = pd.DataFrame(historical_reports)
        df['scan_date'] = pd.to_datetime(df['scan_date'])
        
        fig = px.line(
            df,
            x='scan_date',
            y='risk_score',
            title="Risk Score Trend Over Time",
            markers=True
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Table of reports
        st.dataframe(df[['project_path', 'scan_date', 'total_files', 'risk_score']], use_container_width=True)
    else:
        st.info("No historical reports found. Run your first audit to see trends.")

# CLI interface
def main():
    """Main CLI interface"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Code Quality & Security Audit System")
    parser.add_argument("--directory", "-d", required=True, help="Directory to scan")
    parser.add_argument("--output", "-o", help="Output file for report (JSON)")
    parser.add_argument("--dashboard", action="store_true", help="Launch Streamlit dashboard")
    
    args = parser.parse_args()
    
    if args.dashboard:
        # Launch Streamlit dashboard
        import subprocess
        subprocess.run(["streamlit", "run", __file__])
        return
    
    auditor = CodeAuditor()
    
    print("🔍 Starting Code Quality & Security Audit...")
    print(f"Scanning directory: {args.directory}")
    
    try:
        report = auditor.scan_directory(args.directory)
        
        print(f"\n✅ Audit completed!")
        print(f"📊 Files scanned: {report.total_files}")
        print(f"📏 Total lines: {report.total_lines}")
        print(f"🔐 Security issues: {len(report.security_issues)}")
        print(f"📊 Quality issues: {len(report.quality_issues)}")
        print(f"⚠️  Risk score: {report.risk_score}/100")
        
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(asdict(report), f, indent=2, default=str)
            print(f"📄 Report saved to: {args.output}")
        
        # Print top issues
        if report.security_issues:
            print(f"\n🔴 Top Security Issues:")
            for issue in report.security_issues[:5]:
                print(f"  - {issue.issue_type} in {issue.file_path}:{issue.line_number}")
        
        if report.quality_issues:
            print(f"\n🟡 Top Quality Issues:")
            for issue in report.quality_issues[:5]:
                print(f"  - {issue.issue_type} in {issue.file_path}:{issue.line_number}")
    
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    # Check if running with Streamlit
    try:
        # This will be set when running with streamlit
        import streamlit as st
        create_streamlit_dashboard()
    except ImportError:
        # Running as CLI
        main()