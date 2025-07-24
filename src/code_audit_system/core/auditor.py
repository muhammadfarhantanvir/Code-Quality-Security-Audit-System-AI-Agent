"""
Main code auditor class
"""

import os
import json
import re
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import time

from .models import SecurityIssue, QualityIssue, AuditReport, CodeMetrics, ComplianceCheck
from .patterns import (
    SECURITY_PATTERNS, QUALITY_PATTERNS, CWE_MAPPINGS,
    SECURITY_RECOMMENDATIONS, QUALITY_RECOMMENDATIONS
)
from ..ai.ollama_client import OllamaClient


class CodeAuditor:
    """Main code auditing engine"""
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.ollama = OllamaClient(
            base_url=self.config.get('ollama', {}).get('base_url', 'http://localhost:11434')
        )
        self.db_path = self.config.get('database_path', "audit_results.db")
        self._init_database()
        
        self.supported_extensions = {
            '.py': 'python', '.js': 'javascript', '.jsx': 'javascript',
            '.ts': 'typescript', '.tsx': 'typescript', '.java': 'java',
            '.cpp': 'cpp', '.c': 'c', '.php': 'php', '.rb': 'ruby',
            '.go': 'go', '.rs': 'rust', '.cs': 'csharp', '.swift': 'swift'
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
                cwe_id TEXT,
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
        
        # Migrate existing database if needed
        self._migrate_database(cursor)
        
        conn.commit()
        conn.close()
    
    def _migrate_database(self, cursor):
        """Migrate existing database to new schema"""
        try:
            # Check if cwe_id column exists in security_issues table
            cursor.execute("PRAGMA table_info(security_issues)")
            columns = [column[1] for column in cursor.fetchall()]
            
            if 'cwe_id' not in columns:
                print("🔄 Migrating database schema...")
                cursor.execute("ALTER TABLE security_issues ADD COLUMN cwe_id TEXT")
                print("✅ Database migration completed!")
                
        except Exception as e:
            print(f"⚠️ Database migration warning: {e}")
            # Continue without migration if there's an issue
    
    def scan_directory(self, directory_path: str, use_ai: bool = True) -> AuditReport:
        """Scan entire directory for code issues"""
        start_time = time.time()
        directory_path = Path(directory_path)
        
        if not directory_path.exists():
            raise ValueError(f"Directory {directory_path} does not exist")
        
        # Get files to scan
        files_to_scan = []
        for ext in self.supported_extensions:
            files_to_scan.extend(directory_path.glob(f"**/*{ext}"))
        
        # Filter out excluded patterns
        exclude_patterns = self.config.get('scanning', {}).get('exclude_patterns', [])
        if exclude_patterns:
            filtered_files = []
            for file_path in files_to_scan:
                if not any(pattern in str(file_path) for pattern in exclude_patterns):
                    filtered_files.append(file_path)
            files_to_scan = filtered_files
        
        security_issues = []
        quality_issues = []
        total_lines = 0
        files_by_type = {}
        
        print(f"Scanning {len(files_to_scan)} files...")
        
        for file_path in files_to_scan:
            try:
                # Count files by type
                ext = file_path.suffix
                files_by_type[ext] = files_by_type.get(ext, 0) + 1
                
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    lines = content.split('\n')
                    total_lines += len(lines)
                
                # Pattern-based analysis
                sec_issues = self._analyze_security_patterns(file_path, content)
                qual_issues = self._analyze_quality_patterns(file_path, content)
                
                security_issues.extend(sec_issues)
                quality_issues.extend(qual_issues)
                
                # AI-based analysis (if enabled and available)
                max_file_size = self.config.get('scanning', {}).get('max_file_size', 2000)
                if use_ai and self.ollama.is_available() and len(content) < max_file_size:
                    ai_security = self.ollama.analyze_code_security(content, str(file_path))
                    
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
        
        # Calculate metrics
        scan_duration = time.time() - start_time
        risk_score = self._calculate_risk_score(security_issues, quality_issues)
        recommendations = self._generate_recommendations(security_issues, quality_issues)
        
        # Create code metrics (placeholder implementation)
        code_metrics = CodeMetrics(
            cyclomatic_complexity=0,
            lines_of_code=total_lines,
            comment_ratio=0.0,
            function_count=0,
            class_count=0,
            test_coverage=0.0,
            code_duplication=0.0,
            technical_debt_minutes=len(security_issues) * 30 + len(quality_issues) * 15
        )
        
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
            code_metrics=code_metrics,
            compliance_checks=[],  # Placeholder
            scan_duration=scan_duration,
            files_by_type=files_by_type
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
                            recommendation=SECURITY_RECOMMENDATIONS.get(issue_type, "Review security best practices"),
                            cwe_id=CWE_MAPPINGS.get(issue_type)
                        ))
        
        return issues
    
    def _analyze_quality_patterns(self, file_path: Path, content: str) -> List[QualityIssue]:
        """Analyze file for quality patterns"""
        issues = []
        
        for issue_type, pattern in QUALITY_PATTERNS.items():
            matches = list(re.finditer(pattern, content, re.MULTILINE))
            for match in matches:
                line_num = content[:match.start()].count('\n') + 1
                severity = "MEDIUM" if issue_type in ["Long Functions", "Complex Functions"] else "LOW"
                
                issues.append(QualityIssue(
                    file_path=str(file_path),
                    line_number=line_num,
                    issue_type=issue_type,
                    severity=severity,
                    description=f"{issue_type} detected",
                    code_snippet=match.group()[:100],
                    recommendation=QUALITY_RECOMMENDATIONS.get(issue_type, "Follow coding best practices")
                ))
        
        return issues
    
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
            json.dumps(report.__dict__, default=str)
        ))
        
        report_id = cursor.lastrowid
        
        # Insert security issues
        for issue in report.security_issues:
            cursor.execute('''
                INSERT INTO security_issues (report_id, file_path, line_number, issue_type, severity, description, code_snippet, recommendation, cwe_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (report_id, issue.file_path, issue.line_number, issue.issue_type, 
                  issue.severity, issue.description, issue.code_snippet, issue.recommendation, issue.cwe_id))
        
        # Insert quality issues
        for issue in report.quality_issues:
            cursor.execute('''
                INSERT INTO quality_issues (report_id, file_path, line_number, issue_type, severity, description, code_snippet, recommendation)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (report_id, issue.file_path, issue.line_number, issue.issue_type, 
                  issue.severity, issue.description, issue.code_snippet, issue.recommendation))
        
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