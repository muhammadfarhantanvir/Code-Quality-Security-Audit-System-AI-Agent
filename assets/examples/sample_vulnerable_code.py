"""
Sample vulnerable code for testing the audit system
This file contains intentional security vulnerabilities and code quality issues
"""

import os
import sqlite3
import hashlib

# Security Issues Examples

def vulnerable_sql_query(user_id):
    """SQL Injection vulnerability example"""
    # BAD: String concatenation in SQL query
    query = f"SELECT * FROM users WHERE id = {user_id}"
    return query

def hardcoded_credentials():
    """Hardcoded secrets example"""
    # BAD: Hardcoded API key
    api_key = "sk-1234567890abcdefghijklmnopqrstuvwxyz"
    database_password = "super_secret_password_123"
    return api_key, database_password

def command_injection_vulnerability(filename):
    """Command injection example"""
    # BAD: User input directly in system command
    os.system(f"cat {filename}")
    
def xss_vulnerability(user_input):
    """XSS vulnerability example"""
    # BAD: Unescaped user input in HTML
    return f"<div>Welcome {user_input}!</div>"

def weak_cryptography(password):
    """Weak cryptography example"""
    # BAD: Using MD5 for password hashing
    return hashlib.md5(password.encode()).hexdigest()

def insecure_http_request():
    """Insecure communication example"""
    import requests
    # BAD: Using HTTP instead of HTTPS
    response = requests.get("http://api.example.com/sensitive-data")
    return response

# Code Quality Issues Examples

def very_long_function_with_many_issues(param1, param2, param3, param4, param5, param6, param7, param8):
    """This function has multiple quality issues"""
    # TODO: This function is too long and complex
    result = 0
    
    # Magic numbers everywhere
    for i in range(100):
        if i % 2 == 0:
            if i % 4 == 0:
                if i % 8 == 0:
                    if i % 16 == 0:
                        if i % 32 == 0:
                            # Deep nesting issue
                            result += i * param1 * 42
                        else:
                            result += i * param2 * 13
                    else:
                        result += i * param3 * 7
                else:
                    result += i * param4 * 3
            else:
                result += i * param5 * 2
        else:
            result += i * param6 * 1
    
    # Duplicate code block
    if result > 1000:
        print("Result is large")
        result = result / 2
        print(f"Adjusted result: {result}")
    
    # Duplicate code block (again)
    if result > 1000:
        print("Result is large")
        result = result / 2
        print(f"Adjusted result: {result}")
    
    # Empty exception handling
    try:
        risky_operation = 10 / 0
    except:
        pass
    
    return result

# Global variable (bad practice)
GLOBAL_COUNTER = 0

def function_without_docstring(x, y, z):
    # Missing docstring
    return x + y + z

def bare_except_example():
    try:
        dangerous_operation()
    except:  # BAD: Bare except clause
        return None

def complex_lambda_example():
    # BAD: Overly complex lambda
    complex_func = lambda x, y, z: x + y if x > 0 else y + z if y > 0 else z if z > 0 else 0
    return complex_func

# More security issues

def path_traversal_vulnerability(user_file):
    """Path traversal example"""
    # BAD: User input in file path
    with open(f"../../../etc/passwd/{user_file}", 'r') as f:
        return f.read()

def ldap_injection_example(username):
    """LDAP injection example"""
    # BAD: User input in LDAP filter
    ldap_filter = f"(uid={username})"
    return ldap_filter

def xml_external_entity_example():
    """XXE vulnerability example"""
    import xml.etree.ElementTree as ET
    # BAD: XML parsing with external entities enabled
    parser = ET.XMLParser(resolve_entities=True)
    return parser

def insecure_deserialization_example(data):
    """Insecure deserialization example"""
    import pickle
    # BAD: Deserializing untrusted data
    return pickle.loads(data)

# Additional quality issues

class ClassWithoutDocstring:
    # Missing class docstring
    def __init__(self):
        self.value = 42  # Magic number

    def method_with_too_many_parameters(self, a, b, c, d, e, f, g, h, i, j):
        # Too many parameters
        return a + b + c + d + e + f + g + h + i + j

# Unused import (if this were a real file)
import json  # This import is never used

# Complex regex pattern
import re
COMPLEX_REGEX = r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'

def dangerous_operation():
    """Function that might raise an exception"""
    raise ValueError("Something went wrong!")

if __name__ == "__main__":
    # This code would trigger various security and quality issues
    print("Running vulnerable code examples...")
    
    # These calls would be flagged by the audit system
    print(vulnerable_sql_query("1 OR 1=1"))
    print(hardcoded_credentials())
    print(weak_cryptography("password123"))
    print(very_long_function_with_many_issues(1, 2, 3, 4, 5, 6, 7, 8))