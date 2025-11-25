"""
Configuration management for Event DB module.
"""

import os
from pathlib import Path
from typing import Optional

# Database Configuration
DATABASE_CONFIG = {
    "host": os.getenv("POSTGRES_HOST", "localhost"),
    "port": int(os.getenv("POSTGRES_PORT", "5432")),
    "database": os.getenv("POSTGRES_DB", "gdelt_events"),
    "user": os.getenv("POSTGRES_USER", "postgres"),
    "password": os.getenv("POSTGRES_PASSWORD", ""),
}

# GDELT Configuration
GDELT_CONFIG = {
    "base_url": "http://data.gdeltproject.org/gdeltv2/",
    "timeout": 60,  # seconds
    "max_retries": 3,
    "retry_delay": 5,  # seconds
}

# Ingestion Configuration
INGESTION_CONFIG = {
    "batch_size": 1000,  # rows per insert
    "parallel_workers": 4,  # for parallel processing
    "chunk_size": 10000,  # rows per chunk
}

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
LOGS_DIR = PROJECT_ROOT / "logs"

# Ensure directories exist
DATA_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

# Logging Configuration
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "standard",
            "stream": "ext://sys.stdout",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "DEBUG",
            "formatter": "standard",
            "filename": str(LOGS_DIR / "event_db.log"),
            "maxBytes": 10485760,  # 10MB
            "backupCount": 5,
        },
    },
    "loggers": {
        "": {  # root logger
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": False,
        }
    },
}


def get_database_url() -> str:
    """Get SQLAlchemy database URL."""
    cfg = DATABASE_CONFIG
    password_part = f":{cfg['password']}" if cfg['password'] else ""
    return f"postgresql://{cfg['user']}{password_part}@{cfg['host']}:{cfg['port']}/{cfg['database']}"


def get_cameo_codes_path() -> Path:
    """Get path to CAMEO codes JSON file."""
    return DATA_DIR / "cameo_codes.json"
