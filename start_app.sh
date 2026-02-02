#!/bin/bash
# Startup script for Code Quality & Security Audit System

# Set the PATH and PYTHONPATH for the application
export PATH="/root/.local/bin:/usr/local/bin:/usr/bin:/bin"
export PYTHONPATH="/app"

# Run the Streamlit application
python run_app.py