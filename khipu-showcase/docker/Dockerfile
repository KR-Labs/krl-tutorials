# Docker configuration for local development
# Also used as base for Voilà deployment

# Use official Python slim image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEMO_MODE=true \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Create non-root user
RUN groupadd --gid 1000 khipu && \
    useradd --uid 1000 --gid 1000 --create-home --shell /bin/bash khipu

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set up working directory
WORKDIR /app

# Copy dependency files first (for better caching)
COPY pyproject.toml README.md ./

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -e . && \
    pip install voila

# Copy source code
COPY src/ ./src/
COPY notebooks/ ./notebooks/
COPY templates/ ./templates/
COPY docs/ ./docs/

# Change ownership to non-root user
RUN chown -R khipu:khipu /app

# Switch to non-root user
USER khipu

# Expose ports
# 8888 - JupyterLab
# 8866 - Voilà
EXPOSE 8888 8866

# Default command (JupyterLab)
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser"]
