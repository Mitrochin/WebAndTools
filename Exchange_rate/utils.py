import logging
from pathlib import Path


def ensure_log_directory():
    log_dir = Path('logs')
    log_dir.mkdir(parents=True, exist_ok=True)
    print("Log directory")