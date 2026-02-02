#!/usr/bin/env python3
"""
Runner script for the Code Quality & Security Audit System
"""

import subprocess
import sys

def run_streamlit():
    """Run the Streamlit application"""
    try:
        # Run streamlit programmatically
        import streamlit.web.bootstrap as bootstrap
        import streamlit.runtime.secrets as secrets
        
        # Set up the Streamlit command line arguments
        sys.argv = ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
        
        # Import and run the Streamlit app
        from streamlit.web import cli as stcli
        sys.exit(stcli.main())
    except ImportError:
        # Fallback: try to run using subprocess
        try:
            result = subprocess.run([
                sys.executable, "-m", "streamlit", "run", "app.py",
                "--server.port", "8501",
                "--server.address", "0.0.0.0"
            ], check=True)
        except subprocess.CalledProcessError:
            print("Error: Could not start Streamlit application")
            sys.exit(1)

if __name__ == "__main__":
    run_streamlit()