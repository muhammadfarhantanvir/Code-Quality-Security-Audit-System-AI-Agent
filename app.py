#!/usr/bin/env python3
"""
🔍 Code Quality & Security Audit System - Live Demo
Production deployment optimized for cloud platforms
"""

import os
import sys
import streamlit as st
import tempfile
import shutil
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.code_audit_system.core.auditor import CodeAuditor
from src.code_audit_system.dashboard.streamlit_app import create_streamlit_dashboard

# Configure for production deployment
st.set_page_config(
    page_title="Code Quality & Security Audit System - Live Demo",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

def analyze_github_repository(github_url, github_analyzer, auditor):
    """Analyze a GitHub repository"""
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # Step 1: Clone repository
        status_text.text("🔄 Cloning repository...")
        progress_bar.progress(20)
        
        temp_dir, error = github_analyzer.clone_repository(github_url, max_size_mb=50)
        
        if error:
            st.error(f"❌ {error}")
            return
        
        # Step 2: Get repository stats
        status_text.text("📊 Analyzing repository structure...")
        progress_bar.progress(40)
        
        repo_stats = github_analyzer.get_repo_stats(temp_dir)
        repo_info = github_analyzer.get_repo_info(github_url)
        
        # Step 3: Run security and quality analysis
        status_text.text("🔍 Scanning for security and quality issues...")
        progress_bar.progress(60)
        
        report = auditor.scan_directory(temp_dir, use_ai=False)  # Disable AI for public demo
        
        # Step 4: Store results
        progress_bar.progress(80)
        
        st.session_state['current_report'] = report
        st.session_state['repo_info'] = repo_info
        st.session_state['repo_stats'] = repo_stats
        st.session_state['github_url'] = github_url
        
        # Step 5: Cleanup
        status_text.text("🧹 Cleaning up...")
        progress_bar.progress(100)
        
        github_analyzer.cleanup_temp_dir(temp_dir)
        
        # Clear progress indicators
        progress_bar.empty()
        status_text.empty()
        
        st.success(f"✅ Analysis completed for {repo_info['full_name']}!")
        
    except Exception as e:
        st.error(f"❌ Analysis failed: {str(e)}")
        progress_bar.empty()
        status_text.empty()

def create_demo_files():
    """Create demo files for users to test"""
    demo_dir = Path("demo_project")
    demo_dir.mkdir(exist_ok=True)
    
    # Create a sample vulnerable file
    vulnerable_code = '''
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
'''
    
    with open(demo_dir / "vulnerable_app.py", "w") as f:
        f.write(vulnerable_code)
    
    return str(demo_dir)

def main():
    """Main application with GitHub repository analysis"""
    st.title("🔍 Code Quality & Security Audit System")
    st.markdown("### Analyze Any GitHub Repository for Security & Quality Issues")
    
    # Add demo notice
    st.info("🎯 **Live Demo**: Analyze any public GitHub repository instantly! For private repos and advanced features, install locally.")
    
    # Import GitHub analyzer
    from src.code_audit_system.core.github_analyzer import GitHubAnalyzer
    
    # Initialize components
    auditor = CodeAuditor()
    github_analyzer = GitHubAnalyzer()
    
    # Sidebar
    st.sidebar.header("🚀 Analyze Repository")
    
    # Analysis mode selection
    analysis_mode = st.sidebar.radio(
        "Choose Analysis Mode:",
        ["🌐 GitHub Repository", "📁 Demo Code"],
        index=0
    )
    
    if analysis_mode == "🌐 GitHub Repository":
        # GitHub URL input
        st.sidebar.markdown("**Enter GitHub Repository URL:**")
        github_url = st.sidebar.text_input(
            "Repository URL",
            placeholder="https://github.com/owner/repository",
            help="Enter the full GitHub repository URL"
        )
        
        # Examples
        with st.sidebar.expander("📋 Example URLs"):
            st.code("https://github.com/django/django")
            st.code("https://github.com/pallets/flask")
            st.code("https://github.com/fastapi/fastapi")
            st.code("https://github.com/microsoft/vscode")
        
        # Validate URL
        if github_url:
            if github_analyzer.is_valid_github_url(github_url):
                st.sidebar.success("✅ Valid GitHub URL")
                
                # Get repository info
                with st.spinner("Getting repository info..."):
                    repo_info = github_analyzer.get_repo_info(github_url)
                
                if repo_info:
                    st.sidebar.markdown("**Repository Info:**")
                    st.sidebar.markdown(f"📦 **{repo_info['full_name']}**")
                    if repo_info['description']:
                        st.sidebar.markdown(f"📝 {repo_info['description'][:100]}...")
                    st.sidebar.markdown(f"⭐ {repo_info['stars']} stars")
                    st.sidebar.markdown(f"🍴 {repo_info['forks']} forks")
                    st.sidebar.markdown(f"💾 {repo_info['size']/1024:.1f} MB")
                    if repo_info['language']:
                        st.sidebar.markdown(f"🔤 {repo_info['language']}")
                    
                    # Analyze button
                    if st.sidebar.button("🔍 Analyze Repository", type="primary"):
                        analyze_github_repository(github_url, github_analyzer, auditor)
                else:
                    st.sidebar.error("❌ Repository not found or not accessible")
            else:
                st.sidebar.error("❌ Invalid GitHub URL format")
    
    else:  # Demo mode
        st.sidebar.markdown("**Quick Demo:**")
        st.sidebar.markdown("1. Click 'Run Demo Audit' below")
        st.sidebar.markdown("2. See security & quality issues")
        st.sidebar.markdown("3. Get actionable recommendations")
        
        # Create demo files
        demo_path = create_demo_files()
        
        # Demo button
        if st.sidebar.button("🎯 Run Demo Audit", type="primary"):
            with st.spinner("🔍 Analyzing demo code..."):
                try:
                    report = auditor.scan_directory(demo_path, use_ai=False)  # Disable AI for demo
                    st.session_state['current_report'] = report
                    st.session_state['repo_info'] = {
                        'name': 'Demo Project',
                        'full_name': 'demo/vulnerable-code',
                        'description': 'Sample vulnerable code for demonstration'
                    }
                    st.success("✅ Demo audit completed!")
                except Exception as e:
                    st.error(f"❌ Demo error: {str(e)}")
    
    # Installation instructions
    with st.sidebar.expander("📦 Install Locally"):
        st.code("""
# Option 1: One-command install
curl -fsSL https://raw.githubusercontent.com/muhammadfarhantanvir/Code-Quality-Security-Audit-System-AI-Agent/main/scripts/install.sh | bash

# Option 2: Docker
docker run -p 8501:8501 \\
  muhammadfarhantanvir/code-audit-system

# Option 3: Python package
pip install code-audit-system
code-audit --directory /path/to/project
        """)
    
    # GitHub link
    st.sidebar.markdown("---")
    st.sidebar.markdown("⭐ **[Star on GitHub](https://github.com/muhammadfarhantanvir/Code-Quality-Security-Audit-System-AI-Agent)**")
    st.sidebar.markdown("📖 **[Documentation](https://github.com/muhammadfarhantanvir/Code-Quality-Security-Audit-System-AI-Agent/blob/main/docs/README.md)**")
    
    # Display results if available
    if 'current_report' in st.session_state:
        report = st.session_state['current_report']
        repo_info = st.session_state.get('repo_info', {})
        repo_stats = st.session_state.get('repo_stats', {})
        github_url = st.session_state.get('github_url', '')
        
        # Repository header
        if repo_info:
            st.markdown(f"## 📦 Analysis Results: [{repo_info['full_name']}]({github_url})")
            if repo_info.get('description'):
                st.markdown(f"*{repo_info['description']}*")
            
            # Repository stats
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                st.metric("⭐ Stars", repo_info.get('stars', 0))
            with col2:
                st.metric("🍴 Forks", repo_info.get('forks', 0))
            with col3:
                st.metric("💾 Size", f"{repo_info.get('size', 0)/1024:.1f} MB")
            with col4:
                st.metric("🔤 Language", repo_info.get('language', 'Mixed'))
            with col5:
                st.metric("📁 Files", repo_stats.get('supported_files', report.total_files))
        
        st.markdown("---")
        
        # Analysis metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            risk_color = "🔴" if report.risk_score > 70 else "🟡" if report.risk_score > 30 else "🟢"
            st.metric("Risk Score", f"{report.risk_score}/100", delta=None)
        
        with col2:
            st.metric("Security Issues", len(report.security_issues))
        
        with col3:
            st.metric("Quality Issues", len(report.quality_issues))
        
        with col4:
            st.metric("Lines Analyzed", f"{report.total_lines:,}")
        
        # Risk assessment
        risk_level = "HIGH" if report.risk_score > 70 else "MEDIUM" if report.risk_score > 30 else "LOW"
        risk_color = "red" if risk_level == "HIGH" else "orange" if risk_level == "MEDIUM" else "green"
        
        st.markdown(f"### Risk Assessment: <span style='color:{risk_color}'>{risk_level}</span>", unsafe_allow_html=True)
        
        # Show issues in tabs
        tab1, tab2, tab3 = st.tabs(["🔐 Security Issues", "📊 Quality Issues", "💡 Recommendations"])
        
        with tab1:
            if report.security_issues:
                st.subheader(f"Found {len(report.security_issues)} Security Issues")
                for i, issue in enumerate(report.security_issues[:10], 1):  # Limit to 10 for demo
                    severity_color = "🔴" if issue.severity == "HIGH" else "🟡"
                    with st.expander(f"{severity_color} {issue.issue_type} - Line {issue.line_number}"):
                        st.markdown(f"**Severity:** {issue.severity}")
                        st.markdown(f"**Description:** {issue.description}")
                        st.code(issue.code_snippet, language="python")
                        st.markdown(f"**Recommendation:** {issue.recommendation}")
            else:
                st.success("✅ No security issues found!")
        
        with tab2:
            if report.quality_issues:
                st.subheader(f"Found {len(report.quality_issues)} Quality Issues")
                for i, issue in enumerate(report.quality_issues[:10], 1):  # Limit to 10 for demo
                    severity_color = "🟡" if issue.severity == "MEDIUM" else "🟢"
                    with st.expander(f"{severity_color} {issue.issue_type} - Line {issue.line_number}"):
                        st.markdown(f"**Severity:** {issue.severity}")
                        st.markdown(f"**Description:** {issue.description}")
                        st.code(issue.code_snippet[:200] + "..." if len(issue.code_snippet) > 200 else issue.code_snippet, language="python")
                        st.markdown(f"**Recommendation:** {issue.recommendation}")
            else:
                st.success("✅ No quality issues found!")
        
        with tab3:
            st.subheader("💡 Strategic Recommendations")
            for i, rec in enumerate(report.recommendations, 1):
                priority = "🔴 HIGH" if "URGENT" in rec else "🟡 MEDIUM"
                st.markdown(f"{i}. {priority} - {rec}")
    
    else:
        # Welcome message
        st.markdown("""
        ## 🎯 What This Tool Does
        
        **🌐 Analyze Any GitHub Repository Instantly!**
        
        Simply paste a GitHub URL and get a comprehensive analysis of:
        
        This AI-powered system analyzes your code for:
        
        ### 🔒 Security Issues
        - SQL Injection vulnerabilities
        - Cross-Site Scripting (XSS)
        - Hardcoded secrets and passwords
        - Command injection flaws
        - Weak cryptography usage
        - And more OWASP Top 10 issues...
        
        ### 📊 Code Quality Issues
        - Long and complex functions
        - Code duplication
        - Missing documentation
        - Poor error handling
        - Magic numbers and deep nesting
        - And more maintainability issues...
        
        ### 🤖 AI-Powered Analysis
        - Local Ollama integration for advanced insights
        - Strategic recommendations
        - Technical debt estimation
        - Compliance gap analysis
        
        **👈 Click "Run Demo Audit" in the sidebar to see it in action!**
        """)
        
        # Features showcase
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ### ✨ Key Features
            - **Multi-language support** (Python, JS, Java, C++, etc.)
            - **Real-time analysis** with instant feedback
            - **Export reports** in JSON, CSV, HTML formats
            - **Historical tracking** of code quality trends
            - **CI/CD integration** ready
            """)
        
        with col2:
            st.markdown("""
            ### 🚀 Installation Options
            - **One-command install** for Linux/macOS/Windows
            - **Docker container** for consistent deployment
            - **Python package** via pip install
            - **Web dashboard** (this demo)
            - **CLI tool** for automation
            """)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>🔍 Code Quality & Security Audit System v1.0.0</p>
        <p>Made with ❤️ by Muhammad Farhan Tanvir | 
        <a href="https://github.com/muhammadfarhantanvir/Code-Quality-Security-Audit-System-AI-Agent">GitHub</a> | 
        <a href="https://github.com/muhammadfarhantanvir/Code-Quality-Security-Audit-System-AI-Agent/blob/main/docs/GETTING_STARTED.md">Documentation</a>
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()