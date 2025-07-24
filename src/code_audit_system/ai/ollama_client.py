"""
Ollama AI client for advanced code analysis
"""

import json
import hashlib
import re
from typing import Dict, List
import requests


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