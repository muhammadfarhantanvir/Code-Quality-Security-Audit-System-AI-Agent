
# Sample vulnerable code for demonstration
import os
import hashlib

def login_user(username, password):
    # SQL Injection vulnerability
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    
    # Hardcoded secret
    api_key = "sk-1234567890abcdef"
    
    # Weak cryptography
    password_hash = hashlib.md5(password.encode()).hexdigest()
    
    # Command injection
    os.system(f"echo 'Login attempt: {username}'")
    
    return query

def process_data():
    # TODO: Implement this function
    result = 0
    for i in range(100):  # Magic number
        if i % 2 == 0:
            if i % 4 == 0:
                if i % 8 == 0:  # Deep nesting
                    result += i
    return result

# Global variable
counter = 0

def bad_function():
    try:
        risky_operation()
    except:  # Bare except
        pass
