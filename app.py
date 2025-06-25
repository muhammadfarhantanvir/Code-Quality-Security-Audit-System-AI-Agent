import os
import json
import re
import ast
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Any
import hashlib
import subprocess
import requests
from dataclasses import dataclass, asdict
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Security patterns to detect
SECURITY_PATTERNS = {
    'SQL Injection': [
        r'execute\s*\(\s*["\'].*%.*["\']',
        r'cursor\.execute\s*\(\s*["\'].*\+.*["\']',
        r'query\s*=\s*["\'].*\+.*["\']',
        r'SELECT.*FROM.*WHERE.*=.*\+',
    ],
    'XSS Vulnerability': [
        r'innerHTML\s*=\s*.*\+',
        r'document\.write\s*\(\s*.*\+',
        r'eval\s*\(\s*.*\+',
        r'dangerouslySetInnerHTML',
    ],
    'Hardcoded Passwords': [
        r'password\s*=\s*["\'][^"\']+["\']',
        r'pwd\s*=\s*["\'][^"\']+["\']',
        r'secret\s*=\s*["\'][^"\']+["\']',
        r'api_key\s*=\s*["\'][^"\']+["\']',
    ],
    'Command Injection': [
        r'os\.system\s*\(\s*.*\+',
        r'subprocess\.call\s*\(\s*.*\+',
        r'exec\s*\(\s*.*\+',
        r'eval\s*\(\s*.*\+',
    ],
    'Insecure HTTP': [
        r'http://[^"\'\s]+',
        r'requests\.get\s*\(\s*["\']http://',
        r'urllib\.request\.urlopen\s*\(\s*["\']http://',
    ]
}

# Code quality patterns
QUALITY_PATTERNS = {
    'Long Functions': r'def\s+\w+\s*\([^)]*\):[^def]{500,}',
    'Duplicate Code': r'(.{50,})\s*\n.*\1',
    'Magic Numbers': r'\b\d{2,}\b(?!\s*[)\]}])',
    'TODO Comments': r'#.*TODO|#.*FIXME|#.*HACK',
    'Empty Exception': r'except[^:]*:\s*pass',
    'Global Variables': r'^\s*global\s+\w+',
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

@dataclass
class QualityIssue:
    file_path: str
    line_number: int
    issue_type: str
    severity: str
    description: str
    code_snippet: str
    recommendation: str

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

class OllamaClient:
    """Client for interacting with local Ollama models"""
    
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        self.models = {
            'coder': 'deepseek-coder:6.7b',
            'reasoner': 'deepseek-r1:1.5b',
            'scaler': 'deepscaler'
        }
    
    def is_available(self) -> bool:
        """Check if Ollama service is running"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def analyze_code_security(self, code: str, file_path: str) -> str:
        """Use deepseek-coder to analyze code for security issues"""
        prompt = f"""
        Analyze this code for security vulnerabilities and provide recommendations:
        
        File: {file_path}
        Code:
        ```
        {code[:1000]}  # Limit code length
        ```
        
        Focus on:
        1. SQL injection risks
        2. XSS vulnerabilities
        3. Authentication issues
        4. Input validation problems
        5. Hardcoded secrets
        
        Provide a brief analysis with severity level (HIGH/MEDIUM/LOW) and recommendations.
        """
        
        return self._query_model('coder', prompt)
    
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
        1. Code complexity
        2. Naming conventions
        3. Function length
        4. Code duplication
        5. Error handling
        
        Provide recommendations for improvement.
        """
        
        return self._query_model('coder', prompt)
    
    def generate_recommendations(self, issues: List[str]) -> str:
        """Use deepseek-r1 for reasoning about overall recommendations"""
        prompt = f"""
        Based on these code analysis findings, provide strategic recommendations:
        
        Issues found:
        {chr(10).join(issues[:10])}
        
        Provide:
        1. Priority ranking of issues
        2. Business impact assessment
        3. Implementation roadmap
        4. Cost-benefit analysis
        """
        
        return self._query_model('reasoner', prompt)
    
    def _query_model(self, model_type: str, prompt: str) -> str:
        """Query specific Ollama model"""
        try:
            model_name = self.models.get(model_type, 'deepseek-coder:6.7b')
            payload = {
                "model": model_name,
                "prompt": prompt,
                "stream": False
            }
            
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=30
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
        
        # Supported file extensions
        supported_extensions = {'.py', '.js', '.jsx', '.ts', '.tsx', '.java', '.cpp', '.c', '.php', '.rb', '.go'}
        
        files_to_scan = []
        for ext in supported_extensions:
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
            recommendations=recommendations
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
            'Hardcoded Passwords': "Use environment variables or secure vaults",
            'Command Injection': "Validate input and use safe APIs",
            'Insecure HTTP': "Use HTTPS for all external communications"
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
            'Global Variables': "Use dependency injection or class attributes"
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