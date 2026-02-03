import requests
import json
import os
from typing import Optional, Dict, Any

class OllamaService:
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = os.getenv("OLLAMA_HOST", base_url)
        # Check if we are in cloud mode
        self.is_cloud = os.getenv("RENDER", False) or os.getenv("VERCEL", False)

    def analyze_code(self, code_snippet: str, issue_type: str) -> Optional[str]:
        """Provides AI analysis locally via Ollama, or Expert Knowledge Base in the cloud"""
        
        # 1. Try Local Ollama first (if not in cloud)
        if not self.is_cloud:
            try:
                prompt = f"Analyze the following code for a {issue_type} vulnerability. Provide a concise explanation and fix.\nCODE:\n{code_snippet}"
                response = requests.post(f"{self.base_url}/api/generate",
                    json={"model": "deepseek-r1:1.5b", "prompt": prompt, "stream": False},
                    timeout=5)
                if response.status_code == 200:
                    return response.json().get('response')
            except:
                pass # Fallback to Knowledge Base if Ollama is down

        # 2. Portfolio Mode: Zero-Cost Expert Knowledge Base
        kb = {
            "Hardcoded Secret": "The code contains sensitive credentials in plain text. This allows any attacker with read access to the source code to compromise your infrastructure.",
            "SQL Injection": "User input is being directly concatenated into a SQL query. This allows an attacker to manipulate your database and potentially steal all data.",
            "Weak Hashing": "The application uses MD5 or SHA1, which are cryptographically broken. Attackers can quickly reverse these hashes using rainbow tables.",
            "Command Injection": "Unsanitized user input is being passed to a system shell. This allows an attacker to execute arbitrary commands on your server.",
            "XSS Risk": "User output is being rendered directly to the HTML without escaping. This allows an attacker to inject malicious scripts into other users' browsers."
        }
        
        explanation = kb.get(issue_type, "This pattern represents a known security risk that could lead to unauthorized access or data leakage. We recommend following OWASP best practices for remediation.")
        
        return f"💡 [Expert Analysis - Cloud Mode]\n\nExplanation: {explanation}\n\nFix: Ensure you use environment variables and parameterized interfaces to handle sensitive data safely."

    def get_recommendations(self, issues: list) -> str:
        """Get strategic recommendations"""
        if not issues:
            return "Code looks clean! Continue following best practices."
            
        return "1. Implement a Secrets Management solution (Vault/Env Vars).\n2. Adopt Parameterized Queries for all database interactions.\n3. Enable strict Content Security Policy (CSP) headers."
