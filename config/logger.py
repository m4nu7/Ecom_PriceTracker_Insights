"""
Shared logging setup.

Every module should call get_logger(__name__) instead of
configuring its own logging, so all output is consistent and
goes to both the console and the log file.
"""

import logging
import os
from config import settings


def get_logger(name:str) -> logging.Logger:
    """
    Return a configured logger for the given module name.

    Usage:
        from config.logger import get_logger
        logger = get_logger(__name__)
    """

    logger = logging.getLogger(name)

    if not logger.handlers:
        logger.setLevel(settings.LOG_LEVEL.upper())

        os.makedirs(settings.LOG_DIR, exist_ok=True)
        log_path = os.path.join(settings.LOG_DIR, settings.LOG_FILE)

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(threadName)s | %(message)s"
        )

        file_handler = logging.FileHandler(log_path)
        file_handler.setFormatter(formatter)


        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger