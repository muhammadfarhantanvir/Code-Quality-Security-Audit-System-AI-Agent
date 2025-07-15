#!/usr/bin/env python3
"""
Setup script for Code Quality & Security Audit System
"""

from setuptools import setup, find_packages
import os

# Read README for long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="code-audit-system",
    version="1.0.0",
    author="Muhammad Farhan Tanvir",
    author_email="tanvirf07@gmail.com",
    description="AI-powered code quality and security audit system",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/muhammadfarhantanvir/Code-Quality-Security-Audit-System-AI-Agent",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Security",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "code-audit=src.code_audit_system.cli.main:main",
            "code-audit-dashboard=src.code_audit_system.dashboard.streamlit_app:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.md", "*.txt", "*.yml", "*.yaml"],
    },
)