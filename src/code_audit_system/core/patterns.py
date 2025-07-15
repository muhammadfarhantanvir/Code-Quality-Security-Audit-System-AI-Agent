"""
Security and quality patterns for code analysis
"""

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

# CWE (Common Weakness Enumeration) mappings
CWE_MAPPINGS = {
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

# Security recommendations
SECURITY_RECOMMENDATIONS = {
    'SQL Injection': "Use parameterized queries or ORM methods",
    'XSS Vulnerability': "Sanitize user input and use safe rendering methods",
    'Hardcoded Secrets': "Use environment variables or secure vaults",
    'Command Injection': "Validate input and use safe APIs",
    'Insecure Communication': "Use HTTPS for all external communications",
    'Path Traversal': "Validate and sanitize file paths",
    'Weak Cryptography': "Use strong cryptographic algorithms (SHA-256+)",
    'LDAP Injection': "Use parameterized LDAP queries",
    'XML External Entity': "Disable external entity processing",
    'Deserialization': "Avoid deserializing untrusted data"
}

# Quality recommendations
QUALITY_RECOMMENDATIONS = {
    'Long Functions': "Break down into smaller, focused functions",
    'Complex Functions': "Simplify conditional logic and reduce complexity",
    'Deep Nesting': "Reduce nesting levels using early returns",
    'Duplicate Code': "Extract common code into reusable functions",
    'Magic Numbers': "Define constants with descriptive names",
    'TODO Comments': "Complete pending tasks or create tickets",
    'Empty Exception': "Add proper error handling and logging",
    'Global Variables': "Use dependency injection or class attributes",
    'Long Parameter Lists': "Use parameter objects or reduce parameters",
    'Unused Imports': "Remove unused import statements",
    'Missing Docstrings': "Add docstrings to functions and classes",
    'Overly Complex Regex': "Simplify complex regular expressions",
    'Bare Except': "Specify exception types in except clauses",
    'Lambda Complexity': "Replace complex lambdas with named functions"
}