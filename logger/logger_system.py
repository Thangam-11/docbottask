"""
Logging system for DocIntel Bot (UTF-8 Safe)
"""
import logging
import sys
from pathlib import Path
from logger.config_manager import ConfigManager


def setup_logger(name: str = "docintel") -> logging.Logger:
    """Setup and configure logger (handles Windows UTF-8 issue)"""

    config = ConfigManager()
    log_level = config.get('logging.level', 'INFO')
    log_file = config.get('logging.file', 'logs/docintel.log')

    # Create logs directory
    log_path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))
    logger.handlers.clear()

    # Formatters
    detailed_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
    )
    simple_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    )

    # File handler (UTF-8 safe)
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(detailed_formatter)
    logger.addHandler(file_handler)

    # Console handler (UTF-8 safe)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(simple_formatter)

    # ✅ Prevent UnicodeEncodeError on Windows
    try:
        console_handler.stream.reconfigure(encoding='utf-8')
    except Exception:
        pass

    logger.addHandler(console_handler)

    return logger


def get_logger(name: str = "docintel") -> logging.Logger:
    """Get existing logger or create new one"""
    logger = logging.getLogger(name)
    if not logger.handlers:
        return setup_logger(name)
    return logger
