# Multi-stage build for Code Audit System
FROM python:3.11-slim as builder

LABEL maintainer="Muhammad Farhan Tanvir <your.email@example.com>"
LABEL description="AI-powered code quality and security audit system"
LABEL version="1.0.0"

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Production stage
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy Python packages from builder
COPY --from=builder /root/.local /root/.local

# Copy application code
COPY . .

# Make sure scripts are executable
RUN chmod +x app.py dashboard.py main.py run_app.py start_app.sh

# Set environment variables
ENV PATH=/root/.local/bin:/usr/local/bin:/usr/bin:/bin
ENV PYTHONPATH=/app

# Optional: Create non-root user (commented out for now to ensure app runs)
# RUN useradd --create-home --shell /bin/bash audit
# RUN chown -R audit:audit /app
# USER audit

# Expose port for Streamlit
EXPOSE 8501

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Default command
CMD ["bash", "start_app.sh"]