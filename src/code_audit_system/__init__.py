"""
Code Quality & Security Audit System

A comprehensive AI-powered tool for analyzing code quality and security vulnerabilities.
"""

__version__ = "1.0.0"
__author__ = "Muhammad Farhan Tanvir"
__email__ = "your.email@example.com"

from .core.auditor import CodeAuditor
from .core.models import SecurityIssue, QualityIssue, AuditReport
from .ai.ollama_client import OllamaClient

__all__ = [
    "CodeAuditor",
    "SecurityIssue", 
    "QualityIssue",
    "AuditReport",
    "OllamaClient",
]