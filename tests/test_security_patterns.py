"""
Test cases for security pattern detection
"""

import pytest
from pathlib import Path
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.code_audit_system.core.auditor import CodeAuditor
from src.code_audit_system.core.models import SecurityIssue


class TestSecurityPatterns:
    """Test security vulnerability detection patterns"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.auditor = CodeAuditor()
    
    def test_sql_injection_detection(self):
        """Test SQL injection pattern detection"""
        test_cases = [
            'query = f"SELECT * FROM users WHERE id = {user_id}"',
            'cursor.execute("SELECT * FROM users WHERE name = " + user_name)',
            'db.execute(f"INSERT INTO logs VALUES ({data})")',
            'SELECT * FROM products WHERE category = " + category',
        ]
        
        for code in test_cases:
            issues = self.auditor._analyze_security_patterns(Path("test.py"), code)
            sql_issues = [i for i in issues if i.issue_type == "SQL Injection"]
            assert len(sql_issues) >= 1, f"Failed to detect SQL injection in: {code}"
            assert sql_issues[0].severity == "HIGH"
    
    def test_xss_vulnerability_detection(self):
        """Test XSS vulnerability pattern detection"""
        test_cases = [
            'element.innerHTML = user_input + " welcome"',
            'document.write("Hello " + username)',
            'eval("alert(" + message + ")")',
            '<div dangerouslySetInnerHTML={{__html: userContent}} />',
        ]
        
        for code in test_cases:
            issues = self.auditor._analyze_security_patterns(Path("test.js"), code)
            xss_issues = [i for i in issues if i.issue_type == "XSS Vulnerability"]
            assert len(xss_issues) >= 1, f"Failed to detect XSS in: {code}"
    
    def test_hardcoded_secrets_detection(self):
        """Test hardcoded secrets pattern detection"""
        test_cases = [
            'password = "mySecretPassword123"',
            'api_key = "sk-1234567890abcdef"',
            'secret = "super_secret_key_here"',
            'AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"',
        ]
        
        for code in test_cases:
            issues = self.auditor._analyze_security_patterns(Path("test.py"), code)
            secret_issues = [i for i in issues if i.issue_type == "Hardcoded Secrets"]
            assert len(secret_issues) >= 1, f"Failed to detect hardcoded secret in: {code}"
    
    def test_command_injection_detection(self):
        """Test command injection pattern detection"""
        test_cases = [
            'os.system("rm -rf " + user_input)',
            'subprocess.call("ls " + directory)',
            'exec("print(" + user_code + ")")',
            'subprocess.run(["cat", filename], shell=True)',
        ]
        
        for code in test_cases:
            issues = self.auditor._analyze_security_patterns(Path("test.py"), code)
            cmd_issues = [i for i in issues if i.issue_type == "Command Injection"]
            assert len(cmd_issues) >= 1, f"Failed to detect command injection in: {code}"
    
    def test_insecure_communication_detection(self):
        """Test insecure communication pattern detection"""
        test_cases = [
            'url = "http://api.example.com/data"',
            'requests.get("http://insecure-site.com")',
            'urllib.request.urlopen("http://example.com")',
            'requests.post(url, verify=False)',
        ]
        
        for code in test_cases:
            issues = self.auditor._analyze_security_patterns(Path("test.py"), code)
            comm_issues = [i for i in issues if i.issue_type == "Insecure Communication"]
            assert len(comm_issues) >= 1, f"Failed to detect insecure communication in: {code}"
    
    def test_path_traversal_detection(self):
        """Test path traversal pattern detection"""
        test_cases = [
            'open(user_path + "../../../etc/passwd")',
            'file = base_dir + "../" + filename',
            'filename = "../../sensitive/file.txt"',
        ]
        
        for code in test_cases:
            issues = self.auditor._analyze_security_patterns(Path("test.py"), code)
            path_issues = [i for i in issues if i.issue_type == "Path Traversal"]
            assert len(path_issues) >= 1, f"Failed to detect path traversal in: {code}"
    
    def test_weak_cryptography_detection(self):
        """Test weak cryptography pattern detection"""
        test_cases = [
            'hashlib.md5(password.encode())',
            'hashlib.sha1(data)',
            'cipher = DES.new(key)',
            'random.random()',
        ]
        
        for code in test_cases:
            issues = self.auditor._analyze_security_patterns(Path("test.py"), code)
            crypto_issues = [i for i in issues if i.issue_type == "Weak Cryptography"]
            assert len(crypto_issues) >= 1, f"Failed to detect weak cryptography in: {code}"
    
    def test_false_positives(self):
        """Test that safe code doesn't trigger false positives"""
        safe_code_samples = [
            'query = "SELECT * FROM users WHERE id = ?"',  # Parameterized query
            'element.textContent = user_input',  # Safe DOM manipulation
            'password = os.environ.get("PASSWORD")',  # Environment variable
            'subprocess.run(["ls", "-la"], shell=False)',  # Safe subprocess
            'url = "https://api.example.com/data"',  # HTTPS
            'hashlib.sha256(password.encode())',  # Strong hash
        ]
        
        for code in safe_code_samples:
            issues = self.auditor._analyze_security_patterns(Path("test.py"), code)
            # Should have no high-severity issues for safe code
            high_issues = [i for i in issues if i.severity == "HIGH"]
            assert len(high_issues) == 0, f"False positive detected in safe code: {code}"
    
    def test_severity_assignment(self):
        """Test that severity levels are assigned correctly"""
        high_severity_code = 'query = f"DELETE FROM users WHERE id = {user_id}"'
        issues = self.auditor._analyze_security_patterns(Path("test.py"), high_severity_code)
        
        sql_issues = [i for i in issues if i.issue_type == "SQL Injection"]
        assert len(sql_issues) > 0
        assert sql_issues[0].severity == "HIGH"
    
    def test_recommendation_generation(self):
        """Test that appropriate recommendations are generated"""
        code = 'query = f"SELECT * FROM users WHERE id = {user_id}"'
        issues = self.auditor._analyze_security_patterns(Path("test.py"), code)
        
        sql_issues = [i for i in issues if i.issue_type == "SQL Injection"]
        assert len(sql_issues) > 0
        assert "parameterized" in sql_issues[0].recommendation.lower()
    
    def test_line_number_accuracy(self):
        """Test that line numbers are reported accurately"""
        code = """def safe_function():
    return "Hello World"

def vulnerable_function():
    query = f"SELECT * FROM users WHERE id = {user_id}"
    return query"""
        
        issues = self.auditor._analyze_security_patterns(Path("test.py"), code)
        sql_issues = [i for i in issues if i.issue_type == "SQL Injection"]
        
        assert len(sql_issues) > 0
        assert sql_issues[0].line_number == 5  # The vulnerable line
    
    def test_multiple_issues_same_file(self):
        """Test detection of multiple issues in the same file"""
        code = """
password = "hardcoded_secret"
query = f"SELECT * FROM users WHERE id = {user_id}"
os.system("rm " + filename)
"""
        
        issues = self.auditor._analyze_security_patterns(Path("test.py"), code)
        
        # Should detect at least 3 different types of issues
        issue_types = set(issue.issue_type for issue in issues)
        assert len(issue_types) >= 3
        
        # Verify specific issues are detected
        assert any(i.issue_type == "Hardcoded Secrets" for i in issues)
        assert any(i.issue_type == "SQL Injection" for i in issues)
        assert any(i.issue_type == "Command Injection" for i in issues)


if __name__ == "__main__":
    pytest.main([__file__])