import requests
import json
import os
from typing import Optional, Dict, Any

class OllamaService:
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = os.getenv("OLLAMA_HOST", base_url)
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        
        if self.groq_api_key:
            try:
                from groq import Groq
                self.client = Groq(api_key=self.groq_api_key)
                print("[INFO] Cloud Mode: Using Groq AI Engine")
            except ImportError:
                print("[WARN] groq package not installed. Falling back to Ollama.")
                self.client = None
        else:
            self.client = None
            print("[INFO] Local Mode: Using Ollama AI Engine")

    def analyze_code(self, code_snippet: str, issue_type: str) -> Optional[str]:
        """Use Groq or Ollama to provide deeper insight into a detected issue"""
        prompt = f"""
        Analyze the following code for a {issue_type} vulnerability. 
        Provide a concise explanation of the risk and a corrected version of the code.
        
        CODE:
        {code_snippet}
        
        FORMAT:
        Explanation: [Brief explanation]
        Fix: [Code block]
        """
        
        # Try Groq first if key exists
        if self.client:
            try:
                completion = self.client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=1024
                )
                return completion.choices[0].message.content
            except Exception as e:
                print(f"Groq API error: {e}")

        # Fallback to Ollama
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": "deepseek-r1:1.5b",
                    "prompt": prompt,
                    "stream": False
                },
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json().get('response')
        except Exception as e:
            print(f"Ollama error: {e}")
            
        return None

    def get_recommendations(self, issues: list) -> str:
        """Get strategic recommendations based on all found issues"""
        if not issues:
            return "Code looks clean! Continue following best practices."
            
        summary = "\n".join([f"- {i['name']} in {i['file']}" for i in issues[:10]])
        
        prompt = f"""
        Given the following security and quality issues found in a codebase, provide 3 high-level strategic recommendations for the development team:
        {summary}
        """
        
        if self.client:
            try:
                completion = self.client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=1024
                )
                return completion.choices[0].message.content
            except Exception as e:
                print(f"Groq recommendation error: {e}")

        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": "deepseek-r1:1.5b",
                    "prompt": prompt,
                    "stream": False
                },
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json().get('response')
        except Exception as e:
            print(f"Ollama recommendation error: {e}")
            
        return "Focus on addressing high-severity security issues first."
