"""
Logger configuration module
"""

import logging
from pathlib import Path
import sys

def setup_logger():
    """
    Налаштування системи логування
    """
    # Створення директорії для логів якщо її немає
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Налаштування формату
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Налаштування логера
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        handlers=[
            logging.FileHandler(log_dir / "app.log"),
            logging.StreamHandler(sys.stdout)
        ]
    )
