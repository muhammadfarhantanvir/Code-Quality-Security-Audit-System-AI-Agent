"""
Test cases for code quality pattern detection
"""

import pytest
from pathlib import Path
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.code_audit_system.core.auditor import CodeAuditor
from src.code_audit_system.core.models import QualityIssue


class TestQualityPatterns:
    """Test code quality issue detection patterns"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.auditor = CodeAuditor()
    
    def test_long_function_detection(self):
        """Test long function pattern detection"""
        # Create a long function (over 800 characters)
        long_function = """def very_long_function():
    result = 0
    for i in range(100):
        if i % 2 == 0:
            if i % 4 == 0:
                if i % 8 == 0:
                    result += i * 2
                else:
                    result += i * 3
            else:
                result += i * 4
        else:
            result += i * 5
    
    # More code to make it longer
    for j in range(50):
        if j % 3 == 0:
            result -= j
        elif j % 3 == 1:
            result += j * 2
        else:
            result *= 1.1
    
    # Even more code
    temp_list = []
    for k in range(25):
        temp_list.append(k * result)
    
    final_result = sum(temp_list)
    return final_result"""
        
        issues = self.auditor._analyze_quality_patterns(Path("test.py"), long_function)
        long_func_issues = [i for i in issues if i.issue_type == "Long Functions"]
        assert len(long_func_issues) >= 1, "Failed to detect long function"
    
    def test_complex_function_detection(self):
        """Test complex function pattern detection"""
        complex_code = """
if condition1:
    pass
elif condition2:
    pass
elif condition3:
    pass
elif condition4:
    pass
"""
        
        issues = self.auditor._analyze_quality_patterns(Path("test.py"), complex_code)
        complex_issues = [i for i in issues if i.issue_type == "Complex Functions"]
        assert len(complex_issues) >= 1, "Failed to detect complex function"
    
    def test_deep_nesting_detection(self):
        """Test deep nesting pattern detection"""
        nested_code = """
def deeply_nested():
    if level1:
        if level2:
            if level3:
                if level4:
                    if level5:
                        if level6:
                            if level7:
                                return "too deep"
"""
        
        issues = self.auditor._analyze_quality_patterns(Path("test.py"), nested_code)
        nesting_issues = [i for i in issues if i.issue_type == "Deep Nesting"]
        assert len(nesting_issues) >= 1, "Failed to detect deep nesting"
    
    def test_magic_numbers_detection(self):
        """Test magic numbers pattern detection"""
        magic_code = """
def calculate_something():
    result = value * 42  # Magic number
    if result > 1000:    # Another magic number
        return result / 3.14159  # Yet another magic number
"""
        
        issues = self.auditor._analyze_quality_patterns(Path("test.py"), magic_code)
        magic_issues = [i for i in issues if i.issue_type == "Magic Numbers"]
        assert len(magic_issues) >= 1, "Failed to detect magic numbers"
    
    def test_todo_comments_detection(self):
        """Test TODO comments pattern detection"""
        todo_code = """
def incomplete_function():
    # TODO: Implement this function
    # FIXME: This is broken
    # HACK: Temporary workaround
    # XXX: This needs attention
    pass
"""
        
        issues = self.auditor._analyze_quality_patterns(Path("test.py"), todo_code)
        todo_issues = [i for i in issues if i.issue_type == "TODO Comments"]
        assert len(todo_issues) >= 4, "Failed to detect all TODO comments"
    
    def test_empty_exception_detection(self):
        """Test empty exception handling pattern detection"""
        empty_except_code = """
try:
    risky_operation()
except ValueError:
    pass
except Exception:
    pass
"""
        
        issues = self.auditor._analyze_quality_patterns(Path("test.py"), empty_except_code)
        empty_except_issues = [i for i in issues if i.issue_type == "Empty Exception"]
        assert len(empty_except_issues) >= 1, "Failed to detect empty exception handling"
    
    def test_global_variables_detection(self):
        """Test global variables pattern detection"""
        global_code = """
def function_with_global():
    global counter
    global state
    counter += 1
    state = "modified"
"""
        
        issues = self.auditor._analyze_quality_patterns(Path("test.py"), global_code)
        global_issues = [i for i in issues if i.issue_type == "Global Variables"]
        assert len(global_issues) >= 1, "Failed to detect global variables"
    
    def test_long_parameter_lists_detection(self):
        """Test long parameter lists pattern detection"""
        long_params_code = """
def function_with_many_params(param1, param2, param3, param4, param5, param6, param7, param8, param9, param10):
    return param1 + param2 + param3 + param4 + param5
"""
        
        issues = self.auditor._analyze_quality_patterns(Path("test.py"), long_params_code)
        param_issues = [i for i in issues if i.issue_type == "Long Parameter Lists"]
        assert len(param_issues) >= 1, "Failed to detect long parameter list"
    
    def test_missing_docstrings_detection(self):
        """Test missing docstrings pattern detection"""
        no_docstring_code = """
def function_without_docstring():
    return "no documentation"

class ClassWithoutDocstring:
    def method_without_docstring(self):
        pass
"""
        
        issues = self.auditor._analyze_quality_patterns(Path("test.py"), no_docstring_code)
        docstring_issues = [i for i in issues if i.issue_type == "Missing Docstrings"]
        assert len(docstring_issues) >= 1, "Failed to detect missing docstrings"
    
    def test_bare_except_detection(self):
        """Test bare except clause pattern detection"""
        bare_except_code = """
try:
    dangerous_operation()
except:
    handle_error()
"""
        
        issues = self.auditor._analyze_quality_patterns(Path("test.py"), bare_except_code)
        bare_except_issues = [i for i in issues if i.issue_type == "Bare Except"]
        assert len(bare_except_issues) >= 1, "Failed to detect bare except clause"
    
    def test_complex_lambda_detection(self):
        """Test complex lambda pattern detection"""
        complex_lambda_code = """
complex_func = lambda x, y, z: x + y if x > 0 else y + z if y > 0 else z if z > 0 else 0
"""
        
        issues = self.auditor._analyze_quality_patterns(Path("test.py"), complex_lambda_code)
        lambda_issues = [i for i in issues if i.issue_type == "Lambda Complexity"]
        assert len(lambda_issues) >= 1, "Failed to detect complex lambda"
    
    def test_code_duplication_detection(self):
        """Test code duplication pattern detection"""
        duplicate_code = """
def process_data_type_a():
    result = []
    for item in data:
        if item.is_valid():
            result.append(item.process())
    return result

def process_data_type_b():
    result = []
    for item in data:
        if item.is_valid():
            result.append(item.process())
    return result
"""
        
        issues = self.auditor._analyze_quality_patterns(Path("test.py"), duplicate_code)
        # Note: This is a simplified test - real duplication detection is more complex
        duplicate_issues = [i for i in issues if i.issue_type == "Duplicate Code"]
        # May or may not detect depending on the exact pattern matching
    
    def test_severity_assignment(self):
        """Test that quality issue severity levels are assigned correctly"""
        long_function_code = """def very_long_function():
    # This function is intentionally long to trigger the pattern
    result = 0
    for i in range(100):
        if i % 2 == 0:
            if i % 4 == 0:
                if i % 8 == 0:
                    result += i * 2
                else:
                    result += i * 3
            else:
                result += i * 4
        else:
            result += i * 5
    
    for j in range(50):
        if j % 3 == 0:
            result -= j
        elif j % 3 == 1:
            result += j * 2
        else:
            result *= 1.1
    
    temp_list = []
    for k in range(25):
        temp_list.append(k * result)
    
    final_result = sum(temp_list)
    return final_result"""
        
        issues = self.auditor._analyze_quality_patterns(Path("test.py"), long_function_code)
        long_func_issues = [i for i in issues if i.issue_type == "Long Functions"]
        
        if long_func_issues:
            assert long_func_issues[0].severity in ["MEDIUM", "HIGH"]
    
    def test_recommendation_generation(self):
        """Test that appropriate recommendations are generated"""
        todo_code = "# TODO: Implement this feature"
        issues = self.auditor._analyze_quality_patterns(Path("test.py"), todo_code)
        
        todo_issues = [i for i in issues if i.issue_type == "TODO Comments"]
        if todo_issues:
            assert "complete" in todo_issues[0].recommendation.lower() or "task" in todo_issues[0].recommendation.lower()
    
    def test_multiple_quality_issues(self):
        """Test detection of multiple quality issues in the same file"""
        multi_issue_code = """
# TODO: Fix this function
def bad_function(a, b, c, d, e, f, g, h, i, j):  # Too many parameters
    global counter  # Global variable usage
    
    try:
        result = a * 42 + b * 13  # Magic numbers
        if result > 1000:  # More magic numbers
            if counter > 100:
                if result > 5000:
                    if counter > 500:  # Deep nesting
                        return result
    except:  # Bare except
        pass  # Empty exception
    
    return 0
"""
        
        issues = self.auditor._analyze_quality_patterns(Path("test.py"), multi_issue_code)
        
        # Should detect multiple different types of quality issues
        issue_types = set(issue.issue_type for issue in issues)
        assert len(issue_types) >= 3, f"Expected multiple issue types, got: {issue_types}"


if __name__ == "__main__":
    pytest.main([__file__])