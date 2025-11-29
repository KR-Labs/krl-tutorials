# Binder configuration for khipu-showcase
# Launch interactive notebooks directly in the browser

# Base image with JupyterHub
FROM jupyter/scipy-notebook:python-3.11

# Set environment variables
ENV DEMO_MODE=true
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Switch to root for system packages
USER root

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

# Switch back to jovyan user
USER ${NB_UID}

# Copy project files
COPY --chown=${NB_UID}:${NB_GID} . /home/jovyan/khipu-showcase

# Set working directory
WORKDIR /home/jovyan/khipu-showcase

# Install Python dependencies
RUN pip install --no-cache-dir -e ".[dev]"

# Install Jupyter extensions for better UX
RUN pip install --no-cache-dir \
    jupyterlab-git \
    jupyterlab-lsp \
    jupyter-lsp-python

# Pre-import heavy packages to speed up notebook startup
RUN python -c "import pandas; import numpy; import plotly"

# Expose JupyterLab port
EXPOSE 8888

# Default command
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser"]
